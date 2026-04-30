from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import csv
import os
import pandas as pd
from datetime import date

app = Flask(__name__)
CORS(app)

CATEGORIES = {
    "food": ["food", "lunch", "dinner", "snack", "restaurant", "cafe"],
    "travel": ["bus", "auto", "taxi", "train", "flight", "hotel"],
    "health": ["medicine", "doctor", "hospital", "pharmacy"],
    "shopping": ["clothes", "shoes", "amazon", "flipkart", "mall"],
}

def get_category(description):
    desc = description.lower()
    for category, keywords in CATEGORIES.items():
        if any(word in desc for word in keywords):
            return category
    return "other"

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses"""
    try:
        if not os.path.exists("expenses.csv"):
            return jsonify({"expenses": [], "total": 0})
        
        df = pd.read_csv("expenses.csv", names=["Date", "Amount", "Description", "Category"])
        expenses = df.to_dict('records')
        total = float(df['Amount'].sum())
        
        return jsonify({
            "expenses": expenses,
            "total": round(total, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get spending summary by category"""
    try:
        if not os.path.exists("expenses.csv"):
            return jsonify({"summary": {}, "total": 0})
        
        df = pd.read_csv("expenses.csv", names=["Date", "Amount", "Description", "Category"])
        summary = df.groupby("Category")["Amount"].sum().to_dict()
        total = float(df['Amount'].sum())
        
        # Round all values
        summary = {k: round(v, 2) for k, v in summary.items()}
        
        return jsonify({
            "summary": summary,
            "total": round(total, 2),
            "categories": list(summary.keys())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/add-expense', methods=['POST'])
def add_expense():
    """Add a new expense"""
    try:
        data = request.json
        amount = float(data.get('amount'))
        description = data.get('description')
        
        if not description:
            return jsonify({"error": "Description is required"}), 400
        
        category = get_category(description)
        today = date.today()
        
        with open("expenses.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([today, amount, description, category])
        
        return jsonify({
            "success": True,
            "message": f"Expense added! Category: {category}",
            "category": category,
            "date": str(today),
            "amount": amount,
            "description": description
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    return jsonify({"categories": list(CATEGORIES.keys())})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
