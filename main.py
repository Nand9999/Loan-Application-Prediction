from flask import Flask, request, render_template
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("datasets/Loan_Prediction_Dataset.csv")

# Preprocessing the dataset
# Fill missing values
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].mean())
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mean())
df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mean())

# Fill missing values for categorical features with mode
df['Gender'] = df['Gender'].fillna(df['Gender'].mode()[0])
df['Married'] = df['Married'].fillna(df['Married'].mode()[0])
df['Dependents'] = df['Dependents'].fillna(df['Dependents'].mode()[0])
df['Self_Employed'] = df['Self_Employed'].fillna(df['Self_Employed'].mode()[0])

# Replace "3+" with numerical value 3 in the Dependents column
df['Dependents'] = df['Dependents'].replace('3+', 3)

# Label encoding (consider OneHotEncoder for unseen label handling)
encoder = OneHotEncoder(handle_unknown='ignore')
cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
encoded_cols = pd.get_dummies(df[cols], columns=cols, drop_first=True)
df = pd.concat([df, encoded_cols], axis=1)
df.drop(cols, axis=1, inplace=True)

# Train-test split
X = df.drop(columns=['Loan_Status','Loan_ID'], axis=1)
y = df['Loan_Status']
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Model training
model = RandomForestClassifier(n_estimators=100, min_samples_split=25, max_depth=7, max_features=1)
model.fit(x_train, y_train)

# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    # Get form data
    data = {
        'Gender': request.form.get('gender'),
        'Married': request.form.get('married'),
        'Dependents': request.form.get('dependents'),
        'Education': request.form.get('education'),
        'Self_Employed': request.form.get('self_employed'),
        'ApplicantIncome': request.form.get('applicant_income'),
        'CoapplicantIncome': request.form.get('coapplicant_income'),
        'LoanAmount': request.form.get('loan_amount'),
        'Loan_Amount_Term': request.form.get('loan_amount_term'),
        'Credit_History': request.form.get('credit_history'),
        'Property_Area': request.form.get('property_area')
    }

    # Check for missing or empty values
    for key, value in data.items():
        if not value:
            return render_template('result.html', prediction="Please fill all the fields.")

    # Convert numerical values to float
    numerical_keys = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
    for key in numerical_keys:
        try:
            data[key] = float(data[key])
        except ValueError:
            return render_template('result.html', prediction="Invalid input for numerical fields.")

    # Convert Dependents to integer
    try:
        data['Dependents'] = int(data['Dependents'])
    except ValueError:
        return render_template('result.html', prediction="Invalid input for Dependents.")

    # Convert form data to DataFrame
    df_pred = pd.DataFrame([data])

    # Preprocess form data (assuming OneHotEncoder)
    encoded_cols_pred = pd.get_dummies(df_pred[cols], columns=cols, drop_first=True)
    # Reindex columns to align with training data
    df_pred = pd.concat([df_pred, encoded_cols_pred], axis=1).reindex(columns=x_train.columns, fill_value=0)

    # Make predictions using the trained model
    prediction = model.predict(df_pred)
    if prediction[0] == "Y":
        resultt = "Approved"
    if prediction[0] == "N":
        resultt = "Not Approved"

    return render_template('result.html', prediction= resultt)

if __name__ == '__main__':
    app.run(debug=True)
