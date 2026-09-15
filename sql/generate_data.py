"""Generate PostgreSQL-compatible synthetic data for the performance investigation."""
import random
from datetime import datetime, timedelta

N_CUSTOMERS = 1000
N_TRANSACTIONS = 50000
BASE_TIME = datetime(2026, 9, 1)


def sql_timestamp(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    random.seed(42)
    print("BEGIN;")
    for customer_id in range(1, N_CUSTOMERS + 1):
        print(
            "INSERT INTO customers(customer_ref, name) "
            f"VALUES ('CUST{customer_id:06d}', 'Customer {customer_id}');"
        )

    for transaction_id in range(1, N_TRANSACTIONS + 1):
        reference_number = transaction_id - 1 if transaction_id % 5000 == 0 else transaction_id
        transaction_ref = f"TXN{reference_number:08d}"
        customer_id = random.randint(1, N_CUSTOMERS)
        amount = round(random.uniform(100, 100000), 2)
        created_at = BASE_TIME + timedelta(seconds=random.randint(0, 10 * 86400))
        status_roll = random.random()

        if status_roll < 0.82:
            status = "SUCCESS"
            completed_at = created_at + timedelta(seconds=random.randint(1, 90))
            failure_code = "NULL"
        elif status_roll < 0.95:
            status = "FAILED"
            completed_at = created_at + timedelta(seconds=random.randint(1, 120))
            failure_code = "'UPSTREAM_ERROR'"
        else:
            status = "PROCESSING"
            completed_at = None
            failure_code = "NULL"

        completed_sql = f"'{sql_timestamp(completed_at)}'" if completed_at else "NULL"
        print(
            "INSERT INTO transactions(transaction_ref, customer_id, amount, status, "
            "created_at, completed_at, failure_code) "
            f"VALUES ('{transaction_ref}', {customer_id}, {amount}, '{status}', "
            f"'{sql_timestamp(created_at)}', {completed_sql}, {failure_code});"
        )

        if status in {"SUCCESS", "FAILED"}:
            callback_succeeds = status == "SUCCESS" and random.random() < 0.94
            attempts = 1 if callback_succeeds else random.randint(1, 3)
            for attempt in range(1, attempts + 1):
                callback_ok = callback_succeeds and attempt == attempts
                http_status = 200 if callback_ok else random.choice([500, 502, 503])
                callback_status = "SUCCESS" if callback_ok else "FAILED"
                attempted_at = (completed_at or created_at) + timedelta(seconds=attempt * 5)
                print(
                    "INSERT INTO callbacks(transaction_id, attempt_no, http_status, "
                    "callback_status, attempted_at) "
                    f"VALUES ({transaction_id}, {attempt}, {http_status}, "
                    f"'{callback_status}', '{sql_timestamp(attempted_at)}');"
                )
    print("COMMIT;")


if __name__ == "__main__":
    main()
