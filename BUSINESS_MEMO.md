BUSINESS MEMO

Project: AI-Powered COD Order Risk Detection System

1. Executive Summary

The objective of this project is to reduce Return to Origin (RTO) losses in an e-commerce haircare business by identifying high-risk Cash on Delivery orders before shipment.

The system analyses historical order information and assigns risk categories to help the business make better shipping decisions.

2. Business Problem

Cash on Delivery orders can result in failed deliveries, customer rejections, and additional logistics expenses.

The business needs a system that identifies potentially risky orders and recommends suitable actions.

3. Proposed Solution

The proposed system uses Python and Pandas to analyse historical order data.

It evaluates:

- Previous customer orders.
- Previous RTO history.
- Order value.
- Customer ordering behaviour.

Orders are assigned risk categories:

- Low Risk
- Medium Risk
- High Risk

4. Decision Strategy

Risk Category| Recommended Action
Low Risk| Ship as-is
Medium Risk| WhatsApp confirmation
High Risk| Additional verification before shipment

Prepaid discounts are also proposed to encourage customers to pay online.

5. WhatsApp Confirmation

A mock WhatsApp workflow handles:

- YES: Confirm order.
- NO: Cancel order.
- Invalid reply: Ask again.
- No response: Keep pending.

6. Financial Impact

The dashboard estimates:

- Potential RTO handling cost savings.
- Potential genuine-order cancellation losses.
- Net estimated financial impact.

The financial calculations use illustrative assumptions and require validation using actual business costs and customer outcomes.

7. Technology Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- Seaborn

8. Limitations

- Historical data contains duplicate order IDs and inconsistent status labels.
- Current risk scoring uses rule-based logic rather than a trained machine-learning model.
- WhatsApp integration is simulated.
- Financial impact estimates depend on assumed values.

9. Recommendations

1. Validate and clean historical order records.
2. Train and evaluate a machine-learning model using historical delivery outcomes.
3. Test risk decisions before deploying them.
4. Introduce real WhatsApp integration.
5. Monitor RTO rates and financial performance regularly.

10. Conclusion

The proposed COD Order Risk Detection System provides a foundation for improving order verification and reducing potential RTO costs.

Further validation and testing are necessary before using the system in a live business environment.