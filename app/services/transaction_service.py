from app.models import Transaction
from app.extensions import db
from app.utils.errors import NotFoundError

def create_transaction(user_id, data):
    txn = Transaction(
        user_id=user_id, 
        amount=data['amount'], 
        type=data['type'], 
        category=data['category'], 
        description=data.get('description', '')
    )
    db.session.add(txn)
    db.session.commit()
    return txn

def get_user_transactions(user_id):
    # Retrieve global ledger, not just personal ones
    return Transaction.query.filter_by(is_deleted=False).order_by(Transaction.date.desc()).all()

def update_transaction(txn_id, user_id, data):
    txn = Transaction.query.filter_by(id=txn_id, is_deleted=False).first()
    if not txn:
        raise NotFoundError("Transaction not found or you don't have access to it.")
        
    if 'amount' in data: txn.amount = data['amount']
    if 'type' in data: txn.type = data['type']
    if 'category' in data: txn.category = data['category']
    if 'description' in data: txn.description = data['description']
    
    db.session.commit()
    return txn

def delete_transaction(txn_id, user_id):
    txn = Transaction.query.filter_by(id=txn_id, is_deleted=False).first()
    if not txn:
        raise NotFoundError("Transaction not found.")
    
    # Notice we don't db.session.delete(txn), we trigger our soft delete!
    txn.soft_delete()
    db.session.commit()
    return True
