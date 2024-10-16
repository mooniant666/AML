import streamlit as st
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load your dataset (replace this with your actual file path)
@st.cache
def load_data():
    filepath = './Big_Black_Money_Dataset.csv'  # Update with actual path
    df = pd.read_csv(filepath)
    return df

# Function to train Random Forest model
def train_model(df):
    # Check the actual column names
    print(df.columns)

    # Select relevant features (Update this based on actual column names)
    X = df[['Amount (USD)', 'Transaction Type', 'Source of Money', 'Country', 'Destination Country']]
    
    # Convert categorical variables to numerical (one-hot encoding)
    X = pd.get_dummies(X, drop_first=True)
    
    # Define target variable
    y = df['Money Laundering Risk Score'].apply(lambda x: 1 if x >= 8 else 0)  # 1 for high-risk, 0 for low-risk
    
    # Train the Random Forest model
    rf = RandomForestClassifier(n_estimators=100, random_state=1)
    rf.fit(X, y)
    
    return rf, X.columns  # Return model and feature names

# Function to make predictions
def predict_risk(model, input_data):
    prediction = model.predict(input_data)
    return prediction

# Streamlit app
st.title("High-Risk Transaction Prediction App")

# Load the dataset
df = load_data()

# Train the model
model, feature_columns = train_model(df)

# User inputs for the features
st.header("Input Features for Transaction")

amount_usd = st.number_input("Transaction Amount (USD)", min_value=1000, max_value=100000000, value=10000)

# Categorical inputs (encoded as strings initially)
transaction_type = st.selectbox("Transaction Type", df['Transaction Type'].unique())
source_of_money = st.selectbox("Source of Money", df['Source of Money'].unique())
country = st.selectbox("Origin Country", df['Country'].unique())
destination_country = st.selectbox("Destination Country", df['Destination Country'].unique())

# Prepare the input data for prediction
input_data = pd.DataFrame([[amount_usd, transaction_type, source_of_money, country, destination_country]], 
                          columns=['Amount (USD)', 'Transaction Type', 'Source of Money', 'Country', 'Destination Country'])

# Encode the input data using the same encoding as the training data
input_data_encoded = pd.get_dummies(input_data)
input_data_encoded = input_data_encoded.reindex(columns=feature_columns, fill_value=0)  # Ensure same feature columns

# Predict high-risk when the button is clicked
if st.button("Predict Risk"):
    prediction = predict_risk(model, input_data_encoded)
    if prediction[0] == 1:
        st.error("The transaction is likely high-risk.")
    else:
        st.success("The transaction is likely low-risk.")
