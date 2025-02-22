import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Example: Use a simple random forest classifier to identify malicious emails
def train_model():
    # Placeholder for email dataset
    data = pd.read_csv('emails.csv')  # Ensure you have a CSV with labeled data
    X = data.drop('label', axis=1)
    y = data['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    joblib.dump(model, 'email_model.pkl')
    print("Model trained and saved as email_model.pkl")

def predict_email_status(email_data):
    model = joblib.load('email_model.pkl')
    prediction = model.predict(email_data)
    return "Malicious" if prediction == 1 else "Safe"
