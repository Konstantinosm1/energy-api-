from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_energy_costs():
    # Λήψη των δεδομένων από το αίτημα
    data = request.get_json()
    
    p1 = data.get('p1', 0)  # Πάγιο πακέτου 1
    l1 = data.get('l1', 0)  # Τιμή κιλοβατώρας πακέτου 1
    x = data.get('x', [])  # Λίστα καταναλώσεων κιλοβατώρας για 12 μήνες
    
    # Δεδομένα για το πακέτο 2
    p2 = 15   # Πάγιο πακέτου 2
    l2 = 0.094  # Τιμή κιλοβατώρας πακέτου 2

    x = np.array(x)

    # Υπολογισμός μέσης τιμής και τυπικής απόκλισης
    x_mean = round(np.mean(x), 2)
    x_std = round(np.std(x, ddof=1), 2)  # Τυπική απόκλιση δείγματος

    # Υπολογισμός του ορίου x0
    x0 = round((p2 - p1) / (l1 - l2), 2)

    # Υπολογισμός κόστους για κάθε πακέτο
    cost_p1 = [round(p1 + l1 * consumption, 2) for consumption in x]  # Κόστος για το πακέτο 1
    cost_p2 = [round(p2 + l2 * consumption, 2) for consumption in x]  # Κόστος για το πακέτο 2

    # Υπολογισμός κέρδους (διαφορά κόστους)
    profit = np.array(cost_p1) - np.array(cost_p2)

    # Υπολογισμός μέσου κέρδους και τυπικής απόκλισης κέρδους
    profit_mean = round(np.mean(profit), 2)
    profit_std = round(np.std(profit, ddof=1), 2)
    
    # Δημιουργία του αποτελέσματος ως JSON
    result = {
        "x_mean": x_mean,
        "x_std": x_std,
        "x0": x0,
        "cost_p1": cost_p1,
        "cost_p2": cost_p2,
        "profit": profit.tolist(),
        "profit_mean": profit_mean,
        "profit_std": profit_std
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
