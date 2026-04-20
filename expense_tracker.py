import csv
import os
from datetime import date
from unicodedata import category

CATEGORIES = {
"food": ["food", "lunch", "dinner", "snack", "restaurant", "cafe"],
"travel": ["bus", "auto", "taxi", "train", "flight", "hotel"],
"health": ["medicine", "doctor", "hospital", "pharmacy"],
"shopping": ["clothes", "shoes", "amazon", "flipkart", "mall"],
}

def get_category (description):
 desc = description.lower()
 for category, keywords in CATEGORIES.items():
   if any(word in desc for word in keywords):
    return category
 return "other"

def add_expense():
   amount = float(input("Enter amount (R): "))
   description = input("Enter description: ")
   category = get_category(description)
   today = date.today()

   with open("expenses.csv", "a", newline="") as f:
     writer = csv.writer(f)
     writer.writerow([today, amount, description, category])
     print(f"Saved! Category: {category}")

import pandas as pd 

def show_summary():
    if not os.path.exists("expenses.csv"):
        print("No expenses recorded yet!")
        return
    
    df = pd.read_csv("expenses.csv",
        names=["Date","Amount","Description","Category"])
    
    print("\n--- Spending Summary ---")
    print(df.groupby("Category")["Amount"].sum())
    print(f"\nTotal Spent: ₹{df['Amount'].sum():.2f}")

def main():
    print("=== Automated Expense Tracker ===")
    while True:
        print("\n1. Add Expense")
        print("2. View Summary")
        print("3. Exit")
        choice = input("Choose (1/2/3): ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()