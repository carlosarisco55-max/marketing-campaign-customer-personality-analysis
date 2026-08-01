import csv
from collections import defaultdict

rows = []
with open("processed/marketing_campaign_clean.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows.append(r)

n = len(rows)
def f(r, k): return float(r[k])
def i(r, k): return int(float(r[k]))

# --- Overview ---
total_revenue = sum(f(r, "Total_Spend") for r in rows)
avg_customer_value = total_revenue / n
avg_income = sum(f(r, "Income") for r in rows) / n
avg_recency = sum(f(r, "Recency") for r in rows) / n
complaint_rate = sum(i(r, "Complain") for r in rows) / n
response_rate = sum(i(r, "Response") for r in rows) / n

print("=== OVERVIEW ===")
print(f"N customers: {n}")
print(f"Total revenue: {total_revenue:,.0f}")
print(f"Avg customer value: {avg_customer_value:,.2f}")
print(f"Avg income: {avg_income:,.2f}")
print(f"Avg recency (days): {avg_recency:.1f}")
print(f"Complaint rate: {complaint_rate*100:.2f}%")
print(f"Last campaign (Response) acceptance rate: {response_rate*100:.2f}%")

# --- Campaign acceptance rates ---
print("\n=== CAMPAIGN ACCEPTANCE RATES ===")
campaigns = ["AcceptedCmp1","AcceptedCmp2","AcceptedCmp3","AcceptedCmp4","AcceptedCmp5","Response"]
camp_rates = {}
for c in campaigns:
    rate = sum(i(r, c) for r in rows) / n
    camp_rates[c] = rate
    print(f"{c}: {rate*100:.2f}%")
best_campaign = max(camp_rates, key=camp_rates.get)
print(f"Best campaign: {best_campaign} ({camp_rates[best_campaign]*100:.2f}%)")

# --- Channel share of purchases ---
print("\n=== CHANNEL SHARE (purchase count) ===")
channels = ["NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumDealsPurchases"]
channel_totals = {c: sum(i(r, c) for r in rows) for c in channels}
total_purchases_all = sum(channel_totals[c] for c in ["NumWebPurchases","NumCatalogPurchases","NumStorePurchases"])
for c in channels:
    share = channel_totals[c] / total_purchases_all * 100 if c != "NumDealsPurchases" else None
    print(f"{c}: {channel_totals[c]} total" + (f" ({share:.1f}% share)" if share else ""))

# web conversion proxy
total_web_visits = sum(i(r, "NumWebVisitsMonth") for r in rows)
web_conv = channel_totals["NumWebPurchases"] / total_web_visits
print(f"Web conversion proxy (purchases/visits): {web_conv*100:.1f}%")

# --- Response rate by segment ---
print("\n=== RESPONSE RATE BY HAS CHILDREN ===")
groups = defaultdict(lambda: [0,0])
for r in rows:
    has_kids = "Con hijos" if (i(r,"Kidhome") + i(r,"Teenhome")) > 0 else "Sin hijos"
    groups[has_kids][0] += i(r, "Response")
    groups[has_kids][1] += 1
for k, (acc, tot) in groups.items():
    print(f"{k}: {acc}/{tot} = {acc/tot*100:.2f}%")

print("\n=== RESPONSE RATE BY EDUCATION ===")
groups = defaultdict(lambda: [0,0])
for r in rows:
    groups[r["Education"]][0] += i(r, "Response")
    groups[r["Education"]][1] += 1
for k, (acc, tot) in sorted(groups.items(), key=lambda x: -x[1][0]/x[1][1]):
    print(f"{k}: {acc}/{tot} = {acc/tot*100:.2f}%  (n={tot})")

# --- Age group ---
print("\n=== RESPONSE RATE BY AGE GROUP ===")
def age_group(age):
    if age < 30: return "18-29"
    if age < 45: return "30-44"
    if age < 60: return "45-59"
    return "60+"
groups = defaultdict(lambda: [0,0])
for r in rows:
    g = age_group(i(r, "Age"))
    groups[g][0] += i(r, "Response")
    groups[g][1] += 1
for k in ["18-29","30-44","45-59","60+"]:
    acc, tot = groups[k]
    print(f"{k}: {acc}/{tot} = {acc/tot*100:.2f}%  (n={tot})")

# --- Spend tier vs response (upsell opportunity) ---
print("\n=== SPEND TIER ===")
spends = sorted(f(r, "Total_Spend") for r in rows)
def pct(p): return spends[int(len(spends)*p)]
q1, q2, q3 = pct(0.25), pct(0.5), pct(0.75)
print(f"Quartiles: Q1={q1:.0f} Q2={q2:.0f} Q3={q3:.0f}")

def spend_tier(spend):
    if spend <= q1: return "Low"
    if spend <= q2: return "Medium"
    if spend <= q3: return "High"
    return "Top"

tier_groups = defaultdict(lambda: [0,0,0.0])
for r in rows:
    t = spend_tier(f(r, "Total_Spend"))
    tier_groups[t][0] += i(r, "Response")
    tier_groups[t][1] += 1
    tier_groups[t][2] += f(r, "Total_Spend")
for t in ["Low","Medium","High","Top"]:
    acc, tot, sp = tier_groups[t]
    print(f"{t}: response {acc}/{tot} = {acc/tot*100:.2f}%, avg spend {sp/tot:.0f}")

# --- Multi-campaign responders ---
multi = sum(1 for r in rows if i(r,"Total_Campaigns_Accepted") >= 2)
print(f"\n=== MULTI-CAMPAIGN RESPONDERS (>=2 campaigns) ===")
print(f"{multi}/{n} = {multi/n*100:.2f}%")

# --- High spend + low response = upsell opportunity ---
print("\n=== UPSELL OPPORTUNITY: Top spend tier, did NOT respond to last campaign ===")
top_no_response = sum(1 for r in rows if spend_tier(f(r,"Total_Spend")) == "Top" and i(r,"Response")==0)
top_total = tier_groups["Top"][1]
print(f"{top_no_response}/{int(top_total)} top-tier customers ({top_no_response/top_total*100:.1f}%) didn't respond to last campaign")

# --- Churn risk: high recency + high past spend ---
print("\n=== RETENTION RISK: high recency (>60d) among Top spend tier ===")
at_risk = sum(1 for r in rows if spend_tier(f(r,"Total_Spend"))=="Top" and f(r,"Recency")>60)
print(f"{at_risk}/{int(top_total)} top-tier customers ({at_risk/top_total*100:.1f}%) haven't purchased in 60+ days")

# --- Category spend share ---
print("\n=== CATEGORY SPEND SHARE ===")
cats = ["MntWines","MntFruits","MntMeatProducts","MntFishProducts","MntSweetProducts","MntGoldProds"]
cat_totals = {c: sum(f(r,c) for r in rows) for c in cats}
total_cat = sum(cat_totals.values())
for c in sorted(cat_totals, key=cat_totals.get, reverse=True):
    print(f"{c}: {cat_totals[c]:,.0f} ({cat_totals[c]/total_cat*100:.1f}%)")
