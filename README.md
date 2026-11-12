# FreshWatch 🥬
### Supermarket Expiry & Wastage Prediction System

FreshWatch is a machine learning-powered web application that helps supermarkets monitor perishable stock, predict items at risk of expiring before being sold, and take automated preventive actions (such as dynamic discounts or supplier returns) to minimize food and financial wastage.

---

## 🚀 Features
- **Smart Expiry Risk Scoring**: Predicts probability of stock wastage using a trained **Random Forest Classifier**.
- **Visual Alert System**: High-contrast dark and light modes with KPI summary cards and health progress bars.
- **Dynamic Pricing Recommendations**: Suggests targeted discounts (10% to 40%) or combo deals based on risk and days remaining.
- **Interactive Inventory Management**: Filter by risk level, upload custom supermarket CSVs, or download reports.
- **Single Item Simulator**: Test new items before purchasing or stocking them.
- **Assistant Chatbot**: Quick answers regarding loss, urgent items, and recommended actions.
- **Model Evaluation**: Displays Accuracy, Precision, Recall, F1-Score, Confusion Matrix, and Feature Importance.

---

## 🛠️ Tech Stack
- **Frontend / Dashboard**: Streamlit
- **Machine Learning**: Scikit-Learn (Random Forest, Decision Tree, Logistic Regression)
- **Data Handling**: Pandas & NumPy
- **Visualizations**: Altair
- **Model Persistence**: Joblib

---

## 💻 Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/expiry_project.git
   cd expiry_project
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```
