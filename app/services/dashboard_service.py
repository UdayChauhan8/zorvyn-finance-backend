from app.models import Transaction

def get_summary(user_id):
    transactions = Transaction.query.filter_by(is_deleted=False).all()
    # Python-level generation so we don't write complex RAW SQL queries
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }

def get_category_breakdown(user_id):
    transactions = Transaction.query.filter_by(is_deleted=False).all()
    breakdown = {}
    
    for t in transactions:
        if t.category not in breakdown:
            breakdown[t.category] = 0
        breakdown[t.category] += t.amount
        
    return breakdown
