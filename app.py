from flask import Flask, request, jsonify
import numpy as np
from scipy.stats import norm

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    p1 = 5  # Πάγιο πακέτου 1
    p2 = 15   # Πάγιο πακέτου 2
    l1 = 0.13 # Τιμή κιλοβατώρας πακέτου 1
    l2 = 0.094  # Τιμή κιλοβατώρας πακέτου 2

    # Κατανάλωση από τον χρήστη
    consumption = data.get("consumption", [])

    # Υπολογισμός μέσης τιμής και τυπικής απόκλισης
    x_mean = round(np.mean(consumption), 2)
    x_std = round(np.std(consumption, ddof=1), 2)

    # Υπολογισμός του ορίου x0
    x0 = round((p2 - p1) / (l1 - l2), 2)

    # Κανονικοποίηση z0
    z0 = round((x0 - x_mean) / x_std, 2)

    # Υπολογισμός πιθανότητας
    probability = round(1 - norm.cdf(z0), 2)

    # Υπολογισμός κόστους για κάθε πακέτο
    cost_p1 = [round(p1 + l1 * c, 2) for c in consumption]
    cost_p2 = [round(p2 + l2 * c, 2) for c in consumption]

    # Υπολογισμός κέρδους
    profit = np.array(cost_p1) - np.array(cost_p2)
    profit_mean = round(np.mean(profit), 2)
    annual_profit = round(profit_mean * 12, 2)

    result = {
        "mean_consumption": x_mean,
        "std_consumption": x_std,
        "x0": x0,
        "probability": probability,
        "profit_mean": profit_mean,
        "annual_profit": annual_profit,
        "suggestion": "Package 2 is better" if probability >= 0.5 else "Package 1 is better"
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)