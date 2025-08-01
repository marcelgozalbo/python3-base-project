from app.BalanceTransferService import Account, BalanceTransferService

class TestBalanceTransferService:
    def test_balance_transfer(self):
        # GIVEN
        from_account = Account("Bob", 10000)
        to_account = Account("Alice", 5000)
        amount = 10000
        service = BalanceTransferService()

        total_amount = from_account.balance + to_account.balance

        # WHEN
        service.transfer(from_account, to_account, amount)

        # THEN
        assert total_amount == from_account.balance + to_account.balance
        assert from_account.balance == 10000 - amount
        assert to_account.balance == 5000 + amount
    
    # TODO: Check negative amounts when account creation + transfer
    # TODO: Check same from & to account -> 'Bob' sending same amount to himself
    # TODO: No funds, so transaction fails
    # TODO: Concurrency producer+consumer scenario thread: "client" method (thread target method) triggering the transaction,
    # creating like 4 transactions and 2 threads, 2 transactions per thread
        