
# AI-Powered COD Order Risk Detection System

## Project Overview
This project identifies potential Cash on Delivery (COD) orders that may result in Return to Origin (RTO).

It analyzes historical order data and assigns risk levels to help businesses reduce delivery failures and financial losses.

## Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib

## Project Features
1. COD order risk scoring
2. Risk-based order decisions
3. Mock WhatsApp confirmation
4. Prepaid discount calculation
5. Order analytics dashboard
6. Estimated financial impact analysis

## Project Files
- app.py – Risk detection logic
- dashboard.py – Interactive dashboard
- decision_log.csv – Order decision records
- orders_sample (1).csv – Historical dataset
- BUSINESS_MEMO.md – Business report
- AI_USAGE_LOG.md – AI usage documentation

## How to Run

Install dependencies:

pip install -r requirements.txt

Run the decision engine:

python app.py

Run the dashboard:

streamlit run dashboard.py

## Disclaimer
Risk scores and financial estimates are based on predefined rules and illustrative business assumptions.

