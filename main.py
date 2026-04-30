from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Thailand Digital Savings Account Data (updated April 2026)
ACCOUNTS = [
    {
        "bank": "KKP Bank",
        "account": "FIN SAVE by KKP",
        "app": "Finnomena / KKP App",
        "color": "#1B3A6B",
        "logo_letter": "K",
        "tiers": [
            {"min": 0, "max": 500_000, "rate": 1.70},
            {"min": 500_000, "max": float("inf"), "rate": 0.50},
        ],
        "max_cap": 500_000,
        "highlight_rate": 1.70,
        "conditions": "ยอดฝากไม่เกิน 500,000 บาท รับดอกเบี้ย 1.70% ต่อปี",
        "conditions_en": "Up to ฿500,000 at 1.70% p.a.",
        "interest_freq": "Monthly",
        "open_online": True,
        "dpa_protected": True,
        "url": "https://www.finnomena.com",
        "badge": "🏆 Highest Rate",
    },
    {
        "bank": "CIMB Thai",
        "account": "Speed D+ Savings",
        "app": "CIMB THAI App",
        "color": "#C41E3A",
        "logo_letter": "C",
        "tiers": [
            {"min": 0, "max": 10_000, "rate": 0.50},
            {"min": 10_000, "max": 200_000, "rate": 1.30},
            {"min": 200_000, "max": 2_000_000, "rate": 1.60},
            {"min": 2_000_000, "max": 5_000_000, "rate": 1.60},
            {"min": 5_000_000, "max": float("inf"), "rate": 0.50},
        ],
        "max_cap": 5_000_000,
        "highlight_rate": 1.60,
        "conditions": "ยอดฝาก 200,000 – 2,000,000 บาท รับ 1.60% ต่อปี",
        "conditions_en": "฿200K–฿2M balance at 1.60% p.a.",
        "interest_freq": "Monthly",
        "open_online": True,
        "dpa_protected": True,
        "url": "https://www.cimbthai.com",
        "badge": "⚡ Best for Large Amounts",
    },
    {
        "bank": "SCB",
        "account": "SCB Easy Savings",
        "app": "SCB Easy App",
        "color": "#4A154B",
        "logo_letter": "S",
        "tiers": [
            {"min": 0, "max": 2_000_000, "rate": 1.50},
            {"min": 2_000_000, "max": float("inf"), "rate": 0.50},
        ],
        "max_cap": 2_000_000,
        "highlight_rate": 1.50,
        "conditions": "ยอดฝากไม่เกิน 2,000,000 บาท รับ 1.50% ต่อปี",
        "conditions_en": "Up to ฿2,000,000 at 1.50% p.a.",
        "interest_freq": "Bi-annual (Jun/Dec)",
        "open_online": True,
        "dpa_protected": True,
        "url": "https://www.scb.co.th",
        "badge": "🌟 Most Popular",
    },
    {
        "bank": "LH Bank",
        "account": "M Choice Digital Savings",
        "app": "LH Bank M Choice App",
        "color": "#006B54",
        "logo_letter": "L",
        "tiers": [
            {"min": 0, "max": 5_000_000, "rate": 1.50},
            {"min": 5_000_000, "max": float("inf"), "rate": 0.50},
        ],
        "max_cap": 5_000_000,
        "highlight_rate": 1.50,
        "conditions": "ยอดฝากไม่เกิน 5,000,000 บาท รับ 1.50% ต่อปี",
        "conditions_en": "Up to ฿5,000,000 at 1.50% p.a.",
        "interest_freq": "Monthly",
        "open_online": True,
        "dpa_protected": True,
        "url": "https://www.lhbank.co.th",
        "badge": "💎 Best Cap Limit",
    },
    {
        "bank": "Krungsri (BAY)",
        "account": "Kept Grow Savings",
        "app": "Kept by Krungsri App",
        "color": "#F5A623",
        "logo_letter": "G",
        "tiers": [
            {"min": 0, "max": 5_000_000, "rate": 1.45},
            {"min": 5_000_000, "max": float("inf"), "rate": 0.25},
        ],
        "max_cap": 5_000_000,
        "highlight_rate": 1.45,
        "conditions": "ยอดฝากไม่เกิน 5,000,000 บาท รับสูงสุด 1.45% ต่อปี (เดือนที่ 19-24)",
        "conditions_en": "Up to ฿5,000,000 at up to 1.45% p.a. (months 19–24)",
        "interest_freq": "Monthly (28th)",
        "open_online": True,
        "dpa_protected": True,
        "url": "https://www.keptbykrungsri.com",
        "badge": "📈 Auto-Savings",
    },
    {
        "bank": "Krungthai",
        "account": "NEXT Savings",
        "app": "Krungthai NEXT App",
        "color": "#005BAA",
        "logo_letter": "N",
        "tiers": [
            {"min": 0, "max": 500_000, "rate": 1.25},
            {"min": 500_000, "max": float("inf"), "rate": 0.35},
        ],
        "max_cap": 500_000,
        "highlight_rate": 1.25,
        "conditions": "ยอดฝากไม่เกิน 500,000 บาท รับ 1.25% ต่อปี (เปิดผ่านแอป NEXT เท่านั้น)",
        "conditions_en": "Up to ฿500,000 at 1.25% p.a. (via NEXT App only)",
        "interest_freq": "Bi-annual (Jun/Dec)",
        "open_online": True,
        "dpa_protected": True,
        "url": "https://krungthai.com",
        "badge": "🏦 State Bank",
    },
    {
        "bank": "Bangkok Bank",
        "account": "Bualuang Extra Digital",
        "app": "Bangkok Bank Mobile",
        "color": "#003087",
        "logo_letter": "B",
        "tiers": [
            {"min": 0, "max": 2_000_000, "rate": 1.50},
            {"min": 2_000_000, "max": float("inf"), "rate": 0.50},
        ],
        "max_cap": 2_000_000,
        "highlight_rate": 1.50,
        "conditions": "ยอดฝากไม่เกิน 2,000,000 บาท รับ 1.50% ต่อปี (เมื่อฝากมากกว่าถอน)",
        "conditions_en": "Up to ฿2M at 1.50% when deposits > withdrawals",
        "interest_freq": "Bi-annual",
        "open_online": True,
        "dpa_protected": True,
        "url": "https://www.bangkokbank.com",
        "badge": "🔒 Most Trusted",
    },
]


def calculate_interest(account, amount):
    """Calculate yearly and monthly interest based on tiered rates."""
    yearly_interest = 0.0
    remaining = amount

    for tier in account["tiers"]:
        if remaining <= 0:
            break
        tier_amount = min(remaining, tier["max"] - tier["min"])
        if tier_amount > 0:
            yearly_interest += tier_amount * tier["rate"] / 100
            remaining -= tier_amount

    monthly = yearly_interest / 12
    net_yearly = yearly_interest * 0.85  # 15% withholding tax (if > 20k THB)
    tax_exempt = yearly_interest <= 20_000

    return {
        "yearly": round(yearly_interest, 2),
        "monthly": round(monthly, 2),
        "net_yearly": round(yearly_interest if tax_exempt else net_yearly, 2),
        "tax_exempt": tax_exempt,
    }


@app.route("/")
def index():
    accounts_data = []
    for acc in ACCOUNTS:
        accounts_data.append({
            "bank": acc["bank"],
            "account": acc["account"],
            "app": acc["app"],
            "color": acc["color"],
            "logo_letter": acc["logo_letter"],
            "highlight_rate": acc["highlight_rate"],
            "conditions_en": acc["conditions_en"],
            "conditions": acc["conditions"],
            "interest_freq": acc["interest_freq"],
            "open_online": acc["open_online"],
            "max_cap": acc["max_cap"],
            "badge": acc["badge"],
            "url": acc["url"],
        })
    return render_template("index.html", accounts=accounts_data)


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    amount = float(data.get("amount", 0))

    results = []
    for acc in ACCOUNTS:
        interest = calculate_interest(acc, amount)
        results.append({
            "bank": acc["bank"],
            "account": acc["account"],
            "color": acc["color"],
            "logo_letter": acc["logo_letter"],
            "highlight_rate": acc["highlight_rate"],
            "badge": acc["badge"],
            "yearly": interest["yearly"],
            "monthly": interest["monthly"],
            "net_yearly": interest["net_yearly"],
            "tax_exempt": interest["tax_exempt"],
        })

    # Sort by yearly interest descending
    results.sort(key=lambda x: x["yearly"], reverse=True)
    return jsonify({"results": results, "amount": amount})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
