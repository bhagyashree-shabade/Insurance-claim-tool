from collections import defaultdict
from services.claim_service import get_all_claims
from services.policy_service import get_policyholder_by_id
from datetime import datetime

def generate_reports():
    claims = get_all_claims()
    total_claims = len(claims)
    total_amount = sum(claim.amount for claim in claims) if claims else 0.0

    return {
        "Total Claims": total_claims,
        "Total Claimed Amount": total_amount
    }

def total_claims_per_month():
    monthly_counts = defaultdict(int)
    for claim in get_all_claims():
        month = claim.date.strftime("%Y-%m")
        monthly_counts[month] += 1
    return dict(sorted(monthly_counts.items()))

def average_claim_by_policy_type():
    type_totals = defaultdict(list)
    for claim in get_all_claims():
        ph = get_policyholder_by_id(claim.policyholder_id)
        if ph:
            type_totals[ph.policy_type].append(claim.amount)
    
    return {
        ptype: (sum(amts) / len(amts)) if amts else 0.0
        for ptype, amts in type_totals.items()
    }

def get_highest_claim():
    claims = get_all_claims()
    return max(claims, key=lambda c: c.amount, default=None)

def get_policyholders_with_pending_claims():
    pending_claims = [c for c in get_all_claims() if c.status == "Pending"]
    policyholders = {}
    for claim in pending_claims:
        ph = get_policyholder_by_id(claim.policyholder_id)
        if ph:
            if ph.id not in policyholders:
                policyholders[ph.id] = {
                    "policyholder": ph,
                    "claims": []
                }
            policyholders[ph.id]["claims"].append(claim)
    
    return [
        {
            "id": ph_info["policyholder"].id,
            "name": ph_info["policyholder"].name,
            "policy_type": ph_info["policyholder"].policy_type,
            "claims": [
                {"id": c.id, "amount": c.amount, "reason": c.reason, "date": c.date.strftime("%Y-%m-%d")}
                for c in ph_info["claims"]
            ]
        }
        for ph_info in policyholders.values()
    ]