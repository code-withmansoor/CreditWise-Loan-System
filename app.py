import json
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request, send_from_directory
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "creditwise.db"
DATA_PATHS = [BASE_DIR / "2) loan approval data.csv", BASE_DIR / "loan_approval_data.csv", BASE_DIR / "data" / "loan_approval_data.csv"]


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            applicant_name TEXT NOT NULL,
            result TEXT NOT NULL,
            probability REAL NOT NULL,
            risk_score REAL NOT NULL,
            confidence REAL NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def load_dataset():
    for path in DATA_PATHS:
        if path.exists():
            df = pd.read_csv(path)
            return df

    rows = []
    for idx in range(120):
        income = 25000 + idx * 800
        coapp = 3000 + (idx % 5) * 2000
        loan = 300000 + (idx % 10) * 50000
        credit = 600 + (idx % 5) * 40
        dti = round(0.2 + (idx % 8) * 0.05, 2)
        savings = 10000 + (idx % 7) * 6000
        employment = ['Employed', 'Self Employed', 'Unemployed'][idx % 3]
        marital = ['Single', 'Married', 'Divorced'][idx % 3]
        purpose = ['Education', 'Home', 'Business', 'Personal'][idx % 4]
        property_area = ['Urban', 'Rural', 'Semiurban'][idx % 3]
        gender = ['Female', 'Male', 'Other'][idx % 3]
        education = ['Graduate', 'Undergraduate', 'High School'][idx % 3]
        employer = ['Private', 'Government', 'Startup'][idx % 3]
        age = 22 + (idx % 20)
        dependents = idx % 3
        existing_loans = idx % 2
        approved = 1 if (credit > 700 and dti < 0.4 and income > 40000) else 0
        rows.append({
            'Applicant_Income': income,
            'Coapplicant_Income': coapp,
            'Loan_Amount': loan,
            'Credit_Score': credit,
            'DTI_Ratio': dti,
            'Savings': savings,
            'Employment_Status': employment,
            'Marital_Status': marital,
            'Loan_Purpose': purpose,
            'Property_Area': property_area,
            'Gender': gender,
            'Education_Level': education,
            'Employer_Category': employer,
            'Age': age,
            'Dependents': dependents,
            'Existing_Loans': existing_loans,
            'Loan_Approved': approved,
        })

    return pd.DataFrame(rows)


def build_model():
    df = load_dataset()

    df = df.copy()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    target_col = 'Loan_Approved'

    if target_col in categorical_cols:
        categorical_cols.remove(target_col)
    if target_col in numerical_cols:
        numerical_cols.remove(target_col)

    if not categorical_cols or not numerical_cols:
        raise ValueError("Dataset shape is incompatible with the required training pipeline.")

    X = df.drop(columns=[target_col])
    y = df[target_col].astype(int)

    categorical_features = [c for c in X.columns if c in categorical_cols]
    numerical_features = [c for c in X.columns if c in numerical_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), numerical_features),
            ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical_features),
        ]
    )

    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    score = accuracy_score(y_test, predictions)
    return model, df, score


MODEL, DATAFRAME, MODEL_SCORE = build_model()
init_db()


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/health')
def health():
    return jsonify({'status': 'ok', 'model_score': MODEL_SCORE})


@app.post('/predict')
def predict():
    payload = request.get_json(silent=True) or {}
    applicant_name = payload.get('applicant_name', 'Guest Applicant')

    record = {}
    for key in DATAFRAME.columns:
        if key == 'Loan_Approved':
            continue
        value = payload.get(key)
        if value is None:
            fallback = DATAFRAME[key].dropna().mode().iloc[0] if DATAFRAME[key].dtype == 'O' else float(DATAFRAME[key].median())
            record[key] = fallback
        else:
            record[key] = value

    df_input = pd.DataFrame([record])
    probability = float(MODEL.predict_proba(df_input)[0, 1])
    predicted = int(probability >= 0.5)
    risk_score = round(max(0.0, 1 - probability) * 100, 2)
    confidence = round(abs(probability - 0.5) * 200, 2)
    result = 'Approved' if predicted else 'Rejected'

    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO predictions (created_at, applicant_name, result, probability, risk_score, confidence, payload)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.utcnow().isoformat(),
            applicant_name,
            result,
            probability,
            risk_score,
            confidence,
            json.dumps(payload),
        ),
    )
    conn.commit()
    conn.close()

    return jsonify({
        'result': result,
        'probability': round(probability, 4),
        'risk_score': risk_score,
        'confidence': confidence,
        'risk_level': 'Low' if risk_score < 30 else 'Medium' if risk_score < 70 else 'High',
        'emi': round(float(payload.get('Loan_Amount', 0)) * 0.012, 2),
        'monthly_emi': round(float(payload.get('Loan_Amount', 0)) * 0.012, 2),
        'total_interest': round(float(payload.get('Loan_Amount', 0)) * 0.012 * 12, 2),
        'total_payment': round(float(payload.get('Loan_Amount', 0)) * 1.144, 2),
        'recommendation': 'Proceed with standard review' if result == 'Approved' else 'Focus on credit strengthening and document verification'
    })


@app.get('/history')
def history():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM predictions ORDER BY id DESC LIMIT 10').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(BASE_DIR / 'static', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
