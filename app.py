import pandas as pd

# Load dataset
df = pd.read_csv("orders_sample (1).csv")

# Total orders
total_orders = len(df)

# Count order statuses
status_counts = df["final_status"].str.strip().str.upper().value_counts()

delivered = status_counts.get("DELIVERED", 0)
rto = status_counts.get("RTO", 0)

# Calculate percentages
completed_orders = delivered + rto

rto_rate = (rto / completed_orders) * 100 if completed_orders else 0
delivery_rate = (delivered / completed_orders) * 100 if completed_orders else 0

# Display results
print("===== COD ORDER ANALYSIS =====")
print("Total Orders:", total_orders)
print("Delivered Orders:", delivered)
print("RTO Orders:", rto)
print("RTO Rate:", round(rto_rate, 2), "%")
print("Delivery Rate:", round(delivery_rate, 2), "%")
# Customer RTO Risk Analysis

print("\n===== CUSTOMER RISK ANALYSIS =====")

customer_risk = df.groupby("customer_prior_rto").agg(
    total_orders=("order_id", "count"),
    rto_orders=("final_status", lambda x: (
        x.astype(str).str.strip().str.upper() == "RTO"
    ).sum())
)

customer_risk["rto_rate"] = (
    customer_risk["rto_orders"] /
    customer_risk["total_orders"] * 100
).round(2)

print(customer_risk)
# DATA CLEANING

print("\n===== DATA CLEANING =====")

# Standardize order status
df["final_status"] = (
    df["final_status"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate order IDs
duplicate_count = df["order_id"].duplicated().sum()

print("\nDuplicate Order IDs:", duplicate_count)

# Display cleaned status counts
print("\nCleaned Order Status:")
print(df["final_status"].value_counts())

# Calculate completed orders
completed = df[
    df["final_status"].isin(["DELIVERED", "RTO"])
]

print("\nCompleted Orders:", len(completed))
# COD RISK DECISION ENGINE

print("\n===== COD RISK DECISION ENGINE =====")

def calculate_risk(row):

    previous_rto = row["customer_prior_rto"]

    if pd.isna(previous_rto):
        previous_rto = 0

    if previous_rto >= 2:
        return "HIGH RISK"

    elif previous_rto == 1:
        return "MEDIUM RISK"

    else:
        return "LOW RISK"


# Apply risk calculation
df["risk_level"] = df.apply(calculate_risk, axis=1)


# Assign business decisions
def make_decision(risk):

    if risk == "HIGH RISK":
        return "HOLD / CANCEL"

    elif risk == "MEDIUM RISK":
        return "WHATSAPP CONFIRMATION"

    else:
        return "SHIP AS-IS"


df["decision"] = df["risk_level"].apply(make_decision)


# Display results
print(df[[
    "order_id",
    "customer_prior_rto",
    "risk_level",
    "decision"
]].head(10))


print("\n===== DECISION SUMMARY =====")

print(df["decision"].value_counts())
# ADVANCED RISK SCORING

def calculate_risk_score(row):

    score = 0

    previous_rto = row["customer_prior_rto"]
    previous_orders = row["customer_prior_orders"]
    order_value = row["order_value"]

    if pd.notna(previous_rto):
        if previous_rto >= 2:
            score += 50
        elif previous_rto == 1:
            score += 25

    if pd.notna(order_value) and order_value >= 2000:
        score += 20

    if pd.notna(previous_orders) and previous_orders == 0:
        score += 20

    return score


df["risk_score"] = df.apply(calculate_risk_score, axis=1)


def risk_category(score):

    if score >= 50:
        return "HIGH RISK"
    elif score >= 25:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"


df["advanced_risk"] = df["risk_score"].apply(risk_category)


print("\n===== ADVANCED RISK SCORING =====")

print(df[[
    "order_id",
    "order_value",
    "customer_prior_orders",
    "customer_prior_rto",
    "risk_score",
    "advanced_risk"
]].head(10))
# WHATSAPP CONFIRMATION FLOW

print("\n===== WHATSAPP CONFIRMATION =====")

def whatsapp_confirmation(reply):

    reply = str(reply).strip().upper()

    if reply == "YES":
        return "ORDER CONFIRMED - SHIP"

    elif reply == "NO":
        return "ORDER CANCELLED"

    elif reply == "":
        return "NO RESPONSE - PENDING"

    else:
        return "INVALID REPLY - ASK AGAIN"


# Test customer replies

test_replies = ["YES", "NO", "MAYBE", ""]

for reply in test_replies:

    result = whatsapp_confirmation(reply)

    print("Customer Reply:", reply if reply else "No Reply")
    print("System Action:", result)
    print("-------------------------")
    # PREPAID DISCOUNT CALCULATION

print("\n===== PREPAID DISCOUNT =====")

def calculate_prepaid_discount(order_value):

    discount_percentage = 5

    discount_amount = order_value * discount_percentage / 100

    final_amount = order_value - discount_amount

    return discount_amount, final_amount


# Test calculation

order_value = 1000

discount, final_amount = calculate_prepaid_discount(order_value)

print("Original Order Value: Rs.", order_value)
print("Discount: Rs.", discount)
print("Final Prepaid Amount: Rs.", final_amount)
# GENERATE ACTUAL DECISION LOG

print("\n===== GENERATING DECISION LOG =====")

def get_decision(row):
    if row["risk_score"] >= 50:
        return "HOLD / CANCEL"

    elif row["risk_score"] >= 35:
        return "NUDGE TO PREPAID"

    elif row["risk_score"] >= 25:
        return "WHATSAPP CONFIRMATION"

    else:
        return "SHIP AS-IS"


df["decision"] = df.apply(get_decision, axis=1)

# Create decision log
decision_log = df[[
    "order_id",
    "risk_score",
    "advanced_risk",
    "decision"
]].copy()

# Add reason
decision_log["reason"] = decision_log["decision"].map({
    "HOLD / CANCEL": "High risk score",
    "NUDGE TO PREPAID": "Moderately high risk score",
    "WHATSAPP CONFIRMATION": "Medium risk score",
    "SHIP AS-IS": "Low risk score"
})

# Save CSV file
decision_log.to_csv("decision_log.csv", index=False)

print("Decision log generated successfully!")

print(decision_log.head(10))