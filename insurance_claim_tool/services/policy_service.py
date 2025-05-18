from models.policyholder import Policyholder
import uuid

policyholders = []  

def add_policyholder(name, age, policy_type, sum_insured):
    ph_id = str(uuid.uuid4())
    new_ph = Policyholder(ph_id, name, age, policy_type, sum_insured)
    policyholders.append(new_ph)
    return new_ph

def get_policyholder_by_id(ph_id):
    for ph in policyholders:
        if ph.id == ph_id:
            return ph
    return None

def get_all_policyholders():
    return policyholders