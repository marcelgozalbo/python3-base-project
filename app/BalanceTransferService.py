import threading


class InvalidAmount(Exception):
    pass

class Account:
    def __init__(self, id: str, amount: int) -> None:
        self._id : str = id
        self._balance : int = amount
        self._lock : threading.RLock = threading.RLock()

    def deposit(self, amount: int) -> None:
        if amount < 0:
            raise InvalidAmount
        with self._lock:
            self._balance += amount
    
    def withdraw(self, amount: int) -> bool:
        if amount < 0:
            raise InvalidAmount
        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                return True
        return False
    
    @property
    def balance(self) -> int:
        with self._lock:
            return self._balance


class BalanceTransferService:
     def transfer(self, from_account: Account, to_account: Account, amount: int) -> bool:
        if amount < 0:
            raise InvalidAmount

        lock1 = from_account._lock
        lock2 = to_account._lock
        if from_account._id > to_account._id:
            lock1, lock2 = to_account._lock, from_account._lock
        
        with lock1, lock2:
            if from_account.withdraw(amount):
                to_account.deposit(amount)
                return True
        return False
