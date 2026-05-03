from guara import abstract_transaction 


class TransactionException(Exception):
    pass

# Preconditons
class OrderDoesNotExist(abstract_transaction.AbstractTransaction):
    def do(self, orders, order):
        if order in orders:
            raise TransactionException("Order already exists")
        
# Actions
class CreateOrder(abstract_transaction.AbstractTransaction):
    def do(self, orders, order):
        orders.append(order)   # ⬅️ ინახავს order-ს
        return True