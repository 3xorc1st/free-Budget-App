class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def deposit(self, amount, description=""):
        """Add a deposit to the ledger"""
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=""):
        """Withdraw from the category if funds are available"""
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    
    def get_balance(self):
        """Return the current balance of the category"""
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance
    
    def transfer(self, amount, other_category):
        """Transfer funds to another category"""
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {other_category.name}")
            other_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
    
    def check_funds(self, amount):
        """Check if there are sufficient funds"""
        return amount <= self.get_balance()
    
    def __str__(self):
        """Return string representation of the category"""
        # Title line: 30 characters with category name centered
        title = self.name.center(30, "*")
        
        # Ledger items
        ledger_lines = []
        for item in self.ledger:
            description = item["description"][:23]  # First 23 characters
            amount = f"{item['amount']:.2f}"
            # Right align amount to make 7 characters total
            line = f"{description:<23}{amount:>7}"
            ledger_lines.append(line)
        
        # Balance line
        balance = self.get_balance()
        balance_line = f"Total: {balance:.2f}"
        
        # Combine all parts
        result = title + "\n" + "\n".join(ledger_lines) + "\n" + balance_line
        return result


def create_spend_chart(categories):
    """Create a bar chart showing percentage spent by category"""
    
    # Calculate total spent (withdrawals only)
    total_spent = 0
    spent_by_category = {}
    
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_by_category[category.name] = spent
        total_spent += spent
    
    # Calculate percentages
    percentages = {}
    for category in categories:
        if total_spent > 0:
            percentage = (spent_by_category[category.name] / total_spent) * 100
        else:
            percentage = 0
        # Round down to nearest 10
        percentages[category.name] = int(percentage / 10) * 10
    
    # Build the chart
    chart_lines = ["Percentage spent by category"]
    
    # Y-axis labels and bars (100 down to 0)
    # Each bar line: "XXX|" (4 chars) + bars (10 chars for 3 categories)
    for y in range(100, -1, -10):
        line = f"{y:>3}|"
        for i, category in enumerate(categories):
            if percentages[category.name] >= y:
                line += " o"
            else:
                line += "  "
            if i < len(categories) - 1:
                line += " "
        # Add extra space at end to make line 14 chars (4 + 10)
        line += "  "
        chart_lines.append(line)
    
    # Horizontal line: 4 spaces + dashes (3*num_categories + 1)
    dashes = "-" * (len(categories) * 3 + 1)
    chart_lines.append("    " + dashes)
    
    # Category names vertically
    # Find the longest category name
    max_name_length = max(len(category.name) for category in categories)
    
    for i in range(max_name_length):
        line = "    "
        for j, category in enumerate(categories):
            if i < len(category.name):
                line += " " + category.name[i]
            else:
                line += "  "
            if j < len(categories) - 1:
                line += " "
        # Add extra space at end
        line += "  "
        chart_lines.append(line)
    
    return "\n".join(chart_lines)


# Test cases
if __name__ == "__main__":
    food = Category('Food')
    food.deposit(1000, 'deposit')
    food.withdraw(10.15, 'groceries')
    food.withdraw(15.89, 'restaurant and more food for dessert')
    
    clothing = Category('Clothing')
    clothing.deposit(5000, 'deposit')
    clothing.withdraw(34.05, 'dress')
    clothing.withdraw(3.10, 'shirt')
    
    auto = Category('Auto')
    auto.deposit(1000, 'deposit')
    auto.withdraw(15.00, 'Fuel')
    auto.withdraw(10.00, 'Repair')
    
    food.transfer(50, clothing)
    
    print(food)
    print()
    print(clothing)
    print()
    print(create_spend_chart([food, clothing, auto]))
