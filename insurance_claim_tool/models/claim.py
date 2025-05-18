import uuid
from datetime import datetime

class Claim:
    def __init__(self, policyholder_id, amount, reason, status, date_str):
        self.id = str(uuid.uuid4())  # Unique ID
        self.policyholder_id = policyholder_id
        self.amount = amount
        self.reason = reason
        self.status = status
        self.date_str = datetime.strptime(date_str, "%Y-%m-%d")
