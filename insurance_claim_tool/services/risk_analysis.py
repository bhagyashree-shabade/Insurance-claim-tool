from services.policy_service import get_all_policyholders

def get_high_risk_policyholders():
    high_risk = []
    for ph in get_all_policyholders():
        risk_score = (ph.age / 100) + (ph.sum_insured / 1000000)
        ph.risk_score = risk_score  
        if risk_score > 0.5:  
            high_risk.append(ph)
    return high_risk