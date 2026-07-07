# 💳 CreditWise Loan System

A Machine Learning project that predicts whether a loan application should be **Approved** or **Rejected** based on an applicant's financial, employment, and credit information.

---

## 📌 Project Overview

CreditWise Loan System is an intelligent loan approval prediction system developed using Python and Machine Learning. The project helps financial institutions automate loan approval decisions by analyzing applicant data and predicting loan eligibility.

---

## 🎯 Problem Statement

Traditional loan approval is a manual process that takes time and may lead to inconsistent decisions.

This project aims to:
- Predict loan approval automatically.
- Reduce manual effort.
- Improve decision-making accuracy.
- Help identify eligible applicants quickly.

---

## 📂 Dataset

The dataset contains **1,000 loan applications** with **20 features**, including:

- Applicant Income
- Co-applicant Income
- Employment Status
- Age
- Marital Status
- Dependents
- Credit Score
- Existing Loans
- Debt-to-Income Ratio (DTI)
- Savings
- Collateral Value
- Loan Amount
- Loan Term
- Loan Purpose
- Property Area
- Education Level
- Gender
- Employer Category

**Target Variable**
- `Loan_Approved`
  - **1 = Approved**
  - **0 = Rejected**

---

## ⚙️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

## 🔄 Project Workflow

1. Data Collection
2. Data Cleaning
3. Missing Value Handling
4. Exploratory Data Analysis (EDA)
5. Feature Encoding
6. Feature Scaling
7. Model Training
8. Model Evaluation
9. Feature Engineering
10. Final Prediction

---

## 🤖 Machine Learning Models

The following algorithms were implemented:

- Logistic Regression
- K-Nearest Neighbors (KNN)
- Gaussian Naive Bayes

---

## 📊 Model Performance

| Model | Accuracy |
|--------|----------|
| Logistic Regression | **88%** |
| Gaussian Naive Bayes | **85.5%** |
| K-Nearest Neighbors | **76.5%** |

**Best Performing Model:** Logistic Regression (88% Accuracy)

---

## 📈 Features of the Project

- Missing value handling
- Data visualization
- Feature engineering
- Correlation analysis
- Standardization
- Multiple ML model comparison
- Loan approval prediction

---

## 🚀 How to Run

1. Clone this repository
2. Install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

3. Open the Jupyter Notebook.

4. Run all cells.

---

## 📁 Project Structure

```
CreditWise-Loan-System/
│
├── credit_wise_minor_1.ipynb
├── loan_approval_data.csv
├── README.md
```

---

## 📌 Future Improvements

- Deploy using Streamlit or Flask
- Hyperparameter tuning
- Add Random Forest and XGBoost
- Build a web application
- Real-time loan prediction

---

## 👨‍💻 Author

**Mansoor Makandar**

GitHub: https://github.com/code-withmansoor

---

⭐ If you found this project useful, consider giving it a star!
