
from pathlib import Path
import random
import uuid

import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
rng = np.random.default_rng(SEED)

AS_OF_DATE = pd.Timestamp("2026-06-30")
N_CUSTOMERS = 600

ROOT = Path(__file__).resolve().parents[1]
CRM_DIR = ROOT / "data" / "raw" / "crm"
BILLING_DIR = ROOT / "data" / "raw" / "billing"
PRODUCT_DIR = ROOT / "data" / "raw" / "product"

for folder in (CRM_DIR, BILLING_DIR, PRODUCT_DIR):
    folder.mkdir(parents=True, exist_ok=True)

plans = pd.DataFrame(
    [
        {"PlanID": "PLN-001", "PlanName": "Starter", "MonthlyPrice": 29.0, "IncludedCredits": 5_000, "TargetSegment": "Micro"},
        {"PlanID": "PLN-002", "PlanName": "Growth", "MonthlyPrice": 99.0, "IncludedCredits": 25_000, "TargetSegment": "Small"},
        {"PlanID": "PLN-003", "PlanName": "Scale", "MonthlyPrice": 299.0, "IncludedCredits": 100_000, "TargetSegment": "Medium"},
        {"PlanID": "PLN-004", "PlanName": "Enterprise", "MonthlyPrice": 899.0, "IncludedCredits": 500_000, "TargetSegment": "Large"},
    ]
)

industries = ["Technology", "Finance", "Healthcare", "Retail", "Professional Services", "Education", "Manufacturing", "Media"]
countries = ["United Kingdom", "Ireland", "Germany", "France", "Netherlands", "Spain", "United States", "Canada"]
company_sizes = ["Micro", "Small", "Medium", "Large"]
channels = ["Organic Search", "Paid Search", "Partner", "Referral", "LinkedIn", "Webinar"]
prefixes = ["Blue", "North", "Vertex", "Bright", "Silver", "Quantum", "Oak", "Cloud", "Apex", "Nova", "Cedar", "Peak"]
nouns = ["Analytics", "Labs", "Systems", "Works", "Digital", "Solutions", "Partners", "Studio", "Group", "Technologies"]

def random_date(start: str, end: str) -> pd.Timestamp:
    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    return start_ts + pd.to_timedelta(rng.integers(0, (end_ts - start_ts).days + 1), unit="D")

def choose_initial_plan(size: str) -> str:
    probabilities = {
        "Micro":  [0.76, 0.21, 0.03, 0.00],
        "Small":  [0.22, 0.62, 0.15, 0.01],
        "Medium": [0.04, 0.27, 0.60, 0.09],
        "Large":  [0.00, 0.04, 0.31, 0.65],
    }
    return rng.choice(plans["PlanID"], p=probabilities[size])

customer_rows = []
for i in range(1, N_CUSTOMERS + 1):
    size = rng.choice(company_sizes, p=[0.30, 0.40, 0.22, 0.08])
    created = random_date("2023-01-01", "2026-05-31")
    name = f"{rng.choice(prefixes)} {rng.choice(nouns)}"
    if rng.random() < 0.12:
        name += f" {rng.integers(2, 99)}"

    customer_rows.append(
        {
            "CustomerID": f"CUS-{i:05d}",
            "CustomerName": name,
            "Industry": rng.choice(industries),
            "Country": rng.choice(countries, p=[0.42, 0.08, 0.08, 0.07, 0.06, 0.06, 0.15, 0.08]),
            "CompanySize": size,
            "AcquisitionChannel": rng.choice(channels, p=[0.25, 0.18, 0.15, 0.18, 0.14, 0.10]),
            "CreatedDate": created.date(),
        }
    )

customers_clean = pd.DataFrame(customer_rows)

subscription_rows = []
customer_outcomes = {}

for customer in customers_clean.itertuples(index=False):
    start = pd.Timestamp(customer.CreatedDate) + pd.to_timedelta(int(rng.integers(0, 31)), unit="D")
    if start > AS_OF_DATE:
        start = pd.Timestamp(customer.CreatedDate)

    plan_id = choose_initial_plan(customer.CompanySize)
    plan_index = plans.index[plans["PlanID"] == plan_id][0]

    # Larger firms churn less; newer and smaller firms churn more.
    churn_probability = {"Micro": 0.34, "Small": 0.24, "Medium": 0.14, "Large": 0.06}[customer.CompanySize]
    will_churn = rng.random() < churn_probability and start < AS_OF_DATE - pd.Timedelta(days=120)

    if will_churn:
        minimum_end = start + pd.Timedelta(days=90)
        maximum_end = AS_OF_DATE - pd.Timedelta(days=10)
        cancel_date = minimum_end + pd.to_timedelta(
            int(rng.integers(0, max(1, (maximum_end - minimum_end).days + 1))), unit="D"
        )
    else:
        cancel_date = None

    max_changes = 2 if customer.CompanySize in ("Medium", "Large") else 1
    change_count = int(rng.choice(range(max_changes + 1), p=[0.58, 0.34, 0.08] if max_changes == 2 else [0.72, 0.28]))

    final_date = cancel_date if cancel_date is not None else AS_OF_DATE
    possible_change_dates = pd.date_range(start + pd.Timedelta(days=120), final_date - pd.Timedelta(days=60), freq="30D")
    if len(possible_change_dates) < change_count:
        change_count = len(possible_change_dates)

    change_dates = sorted(rng.choice(possible_change_dates, size=change_count, replace=False)) if change_count else []
    period_start = start

    for change_no, change_date in enumerate(change_dates):
        change_date = pd.Timestamp(change_date)
        monthly_price = float(plans.loc[plan_index, "MonthlyPrice"])
        billing_frequency = rng.choice(["Monthly", "Annual"], p=[0.82, 0.18])
        subscription_rows.append(
            {
                "SubscriptionID": f"SUB-{customer.CustomerID[4:]}-{change_no + 1:02d}",
                "CustomerID": customer.CustomerID,
                "PlanID": plans.loc[plan_index, "PlanID"],
                "StartDate": period_start.date(),
                "EndDate": (change_date - pd.Timedelta(days=1)).date(),
                "Status": "Changed",
                "BillingFrequency": billing_frequency,
                "MonthlyRecurringRevenue": round(monthly_price * (0.90 if billing_frequency == "Annual" else 1.00), 2),
                "EndReason": "Plan Change",
            }
        )

        # Upgrades are more common than downgrades.
        if rng.random() < 0.72 and plan_index < len(plans) - 1:
            plan_index += 1
        elif plan_index > 0:
            plan_index -= 1

        period_start = change_date

    monthly_price = float(plans.loc[plan_index, "MonthlyPrice"])
    billing_frequency = rng.choice(["Monthly", "Annual"], p=[0.82, 0.18])
    subscription_rows.append(
        {
            "SubscriptionID": f"SUB-{customer.CustomerID[4:]}-{len(change_dates) + 1:02d}",
            "CustomerID": customer.CustomerID,
            "PlanID": plans.loc[plan_index, "PlanID"],
            "StartDate": period_start.date(),
            "EndDate": cancel_date.date() if cancel_date is not None else pd.NaT,
            "Status": "Cancelled" if cancel_date is not None else "Active",
            "BillingFrequency": billing_frequency,
            "MonthlyRecurringRevenue": round(monthly_price * (0.90 if billing_frequency == "Annual" else 1.00), 2),
            "EndReason": rng.choice(["Low Usage", "Cost", "Missing Features", "Business Closed"], p=[0.42, 0.30, 0.18, 0.10]) if cancel_date is not None else pd.NA,
        }
    )

    customer_outcomes[customer.CustomerID] = cancel_date

subscriptions = pd.DataFrame(subscription_rows)

usage_rows = []
event_number = 1
plan_lookup = plans.set_index("PlanID").to_dict("index")

for sub in subscriptions.itertuples(index=False):
    start = pd.Timestamp(sub.StartDate)
    end = pd.Timestamp(sub.EndDate) if pd.notna(sub.EndDate) else AS_OF_DATE
    plan = plan_lookup[sub.PlanID]
    plan_multiplier = {"PLN-001": 0.45, "PLN-002": 0.62, "PLN-003": 0.74, "PLN-004": 0.82}[sub.PlanID]
    customer_factor = float(rng.lognormal(mean=0.0, sigma=0.32))

    for event_date in pd.date_range(start, end, freq="D"):
        weekday_factor = 0.45 if event_date.weekday() >= 5 else 1.0
        days_to_end = (end - event_date).days

        # Usage declines before cancellation, making churn analytically meaningful.
        churn_factor = 0.35 if sub.Status == "Cancelled" and days_to_end <= 45 else 1.0
        expected_credits = plan["IncludedCredits"] / 30 * plan_multiplier * customer_factor * weekday_factor * churn_factor

        credits = max(0, int(rng.normal(expected_credits, max(10, expected_credits * 0.18))))
        if rng.random() < 0.025:
            credits = 0

        workflows = max(0, int(credits / rng.uniform(35, 70))) if credits else 0
        api_calls = max(0, int(credits * rng.uniform(1.2, 2.8))) if credits else 0
        active_users = max(0, int(np.sqrt(credits) / rng.uniform(2.5, 4.5))) if credits else 0

        usage_rows.append(
            {
                "UsageEventID": f"USE-{event_number:09d}",
                "CustomerID": sub.CustomerID,
                "SubscriptionID": sub.SubscriptionID,
                "EventDate": event_date.date(),
                "WorkflowsRun": workflows,
                "APICalls": api_calls,
                "CreditsConsumed": credits,
                "ActiveUsers": active_users,
            }
        )
        event_number += 1

usage = pd.DataFrame(usage_rows)

# Add controlled source-system quality issues to the CRM extract.
customers_raw = customers_clean.copy()
customers_raw.loc[rng.choice(customers_raw.index, size=12, replace=False), "Industry"] = pd.NA
customers_raw.loc[rng.choice(customers_raw.index, size=9, replace=False), "Country"] = pd.NA

space_indexes = rng.choice(customers_raw.index, size=15, replace=False)
customers_raw.loc[space_indexes, "CustomerName"] = "  " + customers_raw.loc[space_indexes, "CustomerName"] + " "

# Append exact duplicate source rows. CustomerID remains a business key that Silver must deduplicate.
duplicate_rows = customers_raw.sample(6, random_state=SEED)
customers_raw = pd.concat([customers_raw, duplicate_rows], ignore_index=True)

customers_raw.to_csv(CRM_DIR / "customers.csv", index=False)
plans.to_csv(BILLING_DIR / "plans.csv", index=False)
subscriptions.to_csv(BILLING_DIR / "subscriptions.csv", index=False)
usage.to_csv(PRODUCT_DIR / "usage_events.csv", index=False)

print("Synthetic source data generated")
print(f"Customers rows:      {len(customers_raw):,}")
print(f"Plans rows:          {len(plans):,}")
print(f"Subscriptions rows:  {len(subscriptions):,}")
print(f"Usage rows:          {len(usage):,}")
print(f"Output root:         {ROOT / 'data' / 'raw'}")
