import uuid
from datetime import datetime

class Claim:
    def __init__(self, id, policyholder_id, amount, reason, status, date):
        self.id = id
        self.policyholder_id = policyholder_id
        self.amount = amount
        self.reason = reason
        self.status = status
        self.date = datetime.strptime(date, "%Y-%m-%d") if isinstance(date, str) else date

claims = []  

def add_claim(policyholder_id, amount, reason, status, date):
    claim_id = str(uuid.uuid4())
    new_claim = Claim(claim_id, policyholder_id, amount, reason, status, date)
    claims.append(new_claim)
    return new_claim

def get_all_claims():
    return claims