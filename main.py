class TransactionError(Exception):
    pass

class InMemoryDB:
    def __init__(self):
        self.db = {}
        self.transaction = None

    def get(self, key):
        if self.transaction is not None and key in self.transaction:
            return self.transaction[key]
        return self.db.get(key, None)

    def put(self, key, val):
        if self.transaction is None:
            raise TransactionError("No transaction in progress")
        self.transaction[key] = val

    def begin_transaction(self):
        if self.transaction is not None:
            raise TransactionError("Transaction already in progress")
        self.transaction = {}

    def commit(self):
        if self.transaction is None:
            raise TransactionError("No transaction in progress")
        self.db.update(self.transaction)
        self.transaction = None

    def rollback(self):
        if self.transaction is None:
            raise TransactionError("No transaction in progress")
        self.transaction = None

def main():
    inmemoryDB = InMemoryDB()

    print("\n--- Test 1: Get on non-existent key ---")
    print("Attempting to get non-existent key A...")
    if inmemoryDB.get("A") is None:
        print("SUCCESS")

    print("\n--- Test 2: Put without a transaction ---")
    print("Attempting to put A:5 without a transaction...")
    try:
        inmemoryDB.put("A", 5)
    except TransactionError:
        print("SUCCESS")

    print("\n--- Test 3: Start a new transaction ---")
    print("Starting a new transaction...")
    inmemoryDB.begin_transaction()
    print("SUCCESS")

    print("\n--- Test 4: Put within a transaction ---")
    print("Putting A:5 within the transaction...")
    inmemoryDB.put("A", 5)
    print("SUCCESS")

    print("\n--- Test 5: Get within a transaction ---")
    print("Attempting to get A within the transaction...")
    if inmemoryDB.get("A") is None:
        print("SUCCESS")

    print("\n--- Test 6: Update within the transaction ---")
    print("Updating A to 6 within the transaction...")
    inmemoryDB.put("A", 6)
    print("SUCCESS")

    print("\n--- Test 7: Commit the transaction ---")
    print("Committing the transaction...")
    inmemoryDB.commit()
    print("SUCCESS")

    print("\n--- Test 8: Get after commit ---")
    print("Attempting to get A after commit...")
    if inmemoryDB.get("A") == 6:
        print("SUCCESS")

    print("\n--- Test 9: Commit without a transaction ---")
    print("Attempting to commit without a transaction...")
    try:
        inmemoryDB.commit()
    except TransactionError:
        print("SUCCESS")

    print("\n--- Test 10: Rollback without a transaction ---")
    print("Attempting to rollback without a transaction...")
    try:
        inmemoryDB.rollback()
    except TransactionError:
        print("SUCCESS")

    print("\n--- Test 11: Get on another non-existent key ---")
    print("Attempting to get non-existent key B...")
    if inmemoryDB.get("B") is None:
        print("SUCCESS")

    print("\n--- Test 12: Start another transaction ---")
    print("Starting another transaction...")
    inmemoryDB.begin_transaction()
    print("SUCCESS")

    print("\n--- Test 13: Put within the new transaction ---")
    print("Putting B:10 within the new transaction...")
    inmemoryDB.put("B", 10)
    print("SUCCESS")

    print("\n--- Test 14: Rollback the transaction ---")
    print("Rolling back the transaction...")
    inmemoryDB.rollback()
    print("SUCCESS")

    print("\n--- Test 15: Get after rollback ---")
    print("Attempting to get B after rollback...")
    if inmemoryDB.get("B") is None:
        print("SUCCESS")

if __name__ == "__main__":
    main()