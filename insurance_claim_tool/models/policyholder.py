class Policyholder:
    def __init__(self, id, name, age, policy_type, sum_insured):
        self.id = id
        self.name = name
        self.age = age
        self.policy_type = policy_type
        self.sum_insured = sum_insured
        self.risk_score = 0.0
