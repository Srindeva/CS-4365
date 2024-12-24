import threading
import random
import time

NUM_TELLERS = 3
NUM_CUSTOMERS = 50
customers_served = 0

# Semaphores and locks
safe_access = threading.Semaphore(2)         # Only 2 tellers allowed in the safe at once
manager_access = threading.Semaphore(1)      # Only 1 teller can talk to the manager at a time
bank_entry = threading.Semaphore(2)          # Only 2 customers allowed in the bank at once
queue_lock = threading.Lock()                # Lock for queue operations
served_lock = threading.Lock()               # Lock for updating the customers_served count
print_lock = threading.Lock()                # Lock for synchronized printing
customer_queue = []                          # Queue to manage customers
customer_available = threading.Condition(queue_lock)  # Condition to notify tellers of customers

class Teller(threading.Thread):
    def __init__(self, teller_id):
        super().__init__()
        self.teller_id = teller_id

    def run(self):
        global customers_served
        print_message(f"Teller {self.teller_id} is ready to serve.")
        
        while True:
            with customer_available:
                # Wait for a customer to be available in the queue or check if all customers are served
                while not customer_queue and customers_served < NUM_CUSTOMERS:
                    customer_available.wait()
                
                # Stop if all customers are served
                if customers_served >= NUM_CUSTOMERS:
                    break

                # Serve the next customer in line
                customer = customer_queue.pop(0)
                print_message(f"Teller {self.teller_id} is serving Customer {customer.customer_id}.")

            # Process the transaction type
            if customer.transaction == "withdrawal":
                print_message(f"Teller {self.teller_id} requesting manager permission for withdrawal.")
                with manager_access:
                    print_message(f"Teller {self.teller_id} got manager's permission for withdrawal.")
                    time.sleep(random.uniform(0.005, 0.03))  # Simulate interaction time with manager

            # Enter the safe to complete the transaction
            print_message(f"Teller {self.teller_id} attempting to enter the safe.")
            with safe_access:
                print_message(f"Teller {self.teller_id} is in the safe.")
                time.sleep(random.uniform(0.01, 0.05))  # Simulate safe interaction time
                print_message(f"Teller {self.teller_id} leaving the safe.")

            # Complete transaction and increment served count
            print_message(f"Teller {self.teller_id} finished serving Customer {customer.customer_id}.")
            customer.transaction_complete.set()  # Notify the customer their transaction is complete

            # Increment the served count and check if we should close the bank
            with served_lock:
                customers_served += 1
                if customers_served >= NUM_CUSTOMERS:
                    print_message("Bank is closed.")
                    # Wake all waiting threads to exit
                    with customer_available:
                        customer_available.notify_all()

class Customer(threading.Thread):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id
        self.transaction = random.choice(["deposit", "withdrawal"])
        self.transaction_complete = threading.Event()  # Event to wait until the transaction is complete

    def run(self):
        bank_entry.acquire()  # Limit entry to 2 customers at a time
        try:
            print_message(f"Customer {self.customer_id} is going to the bank.")
            print_message(f"Customer {self.customer_id} is getting in line.")
            
            # Add customer to the queue and notify tellers
            with customer_available:
                customer_queue.append(self)
                customer_available.notify_all()

            # Wait until the teller completes the transaction
            self.transaction_complete.wait()
            print_message(f"Customer {self.customer_id} leaves the bank after completing the transaction.")
        finally:
            bank_entry.release()  # Allow another customer to enter only after the transaction is complete

# Synchronized print function
def print_message(message):
    with print_lock:
        print(message)

# Start the threads
tellers = [Teller(i) for i in range(NUM_TELLERS)]
customers = [Customer(i) for i in range(NUM_CUSTOMERS)]

for teller in tellers:
    teller.start()

for customer in customers:
    customer.start()

for customer in customers:
    customer.join()

for teller in tellers:
    teller.join()
