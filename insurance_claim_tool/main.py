import streamlit as st
from services import claim_service, policy_service, risk_analysis, reports
st.markdown("""
    <style>
    /* Global styles */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f7fa;
    }
    .main .block-container {
        max-width: 900px;
        padding: 2rem;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e3a8a;
        color: #ffffff;
    }
    .css-1d391kg .stSelectbox label {
        color: #ffffff;
        font-weight: bold;
    }
    .css-1d391kg .stSelectbox div[role="combobox"] {
        background-color: #ffffff;
        color: #1e3a8a;
        border-radius: 5px;
    }
    
    /* Header styling */
    h1 {
        color: #1e3a8a;
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 1.5rem;
    }
    h2 {
        color: #1e3a8a;
        font-size: 1.5rem;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.3rem;
        margin-bottom: 1rem;
    }
    
    /* Form styling */
    .stForm {
        background-color: #f9fafb;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 1px solid #d1d5db;
        border-radius: 5px;
        padding: 0.5rem;
        background-color: #ffffff;
    }
    .stButton > button {
        background-color: #3b82f6;
        color: #ffffff;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #2563eb;
    }
    
    /* Output text styling */
    .stSuccess {
        background-color: #d1fae5;
        color: #065f46;
        border-radius: 5px;
        padding: 0.8rem;
    }
    .stError {
        background-color: #fee2e2;
        color: #991b1b;
        border-radius: 5px;
        padding: 0.8rem;
    }
    .stInfo {
        background-color: #e0f2fe;
        color: #1e40af;
        border-radius: 5px;
        padding: 0.8rem;
    }
    .stMarkdown p {
        color: #374151;
        line-height: 1.6;
    }
    
    /* Report sections */
    .report-section {
        margin-top: 1.5rem;
        padding: 1rem;
        background-color: #f9fafb;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("Insurance Claims Management and Risk Analysis Tool")
    
    menu = ["Register Policyholder", "Add Claim", "Risk Analysis", "Reports"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register Policyholder":
        st.header("Register a New Policyholder")

        with st.form("register_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=0, step=1)
            policy_type = st.selectbox("Policy Type", ["Health", "Vehicle", "Life"])
            sum_insured = st.number_input("Sum Insured", min_value=1000.0, step=1000.0)

            submitted = st.form_submit_button("Register")

            if submitted:
                try:
                    new_ph = policy_service.add_policyholder(name, age, policy_type, sum_insured)
                    st.success(f"Policyholder {new_ph.name} registered successfully with ID: {new_ph.id}")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif choice == "Add Claim":
        st.header("Add a Claim")

        with st.form("claim_form"):
            policyholder_id = st.text_input("Policyholder ID")
            claim_amount = st.number_input("Claim Amount", min_value=0.0, step=100.0)
            claim_reason = st.text_area("Reason for Claim")
            status = st.selectbox("Claim Status", ["Pending", "Approved", "Rejected"])
            date_str = st.date_input("Claim Date").strftime("%Y-%m-%d")

            submitted = st.form_submit_button("Submit Claim")
            if submitted:
                try:
                    claim = claim_service.add_claim(policyholder_id, claim_amount, claim_reason, status, date_str)
                    st.success(f"Claim submitted successfully with ID: {claim.id}")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif choice == "Risk Analysis":
        st.header("High Risk Policyholders")

        try:
            high_risk_list = risk_analysis.get_high_risk_policyholders()
            if high_risk_list:
                for ph in high_risk_list:
                    st.write(f"ID: {ph.id}, Name: {ph.name}, Age: {ph.age}, Policy: {ph.policy_type}, Risk Score: {ph.risk_score}")
            else:
                st.info("No high-risk policyholders found.")
        except Exception as e:
            st.error(f"Error during risk analysis: {e}")

    elif choice == "Reports":
        st.header("Reports")
        with st.container():
            try:
                with st.expander("Basic Report", expanded=True):
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    report_data = reports.generate_reports()
                    cols = st.columns(2)
                    for i, (key, value) in enumerate(report_data.items()):
                        cols[i % 2].markdown(f"**{key}**: {value}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with st.expander("Claims per Month"):
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    monthly_counts = reports.total_claims_per_month()
                    cols = st.columns(2)
                    for i, (month, count) in enumerate(monthly_counts.items()):
                        cols[i % 2].markdown(f"**{month}**: {count}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with st.expander("Average Claim by Policy Type"):
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    avg_claims = reports.average_claim_by_policy_type()
                    cols = st.columns(2)
                    for i, (ptype, avg) in enumerate(avg_claims.items()):
                        cols[i % 2].markdown(f"**{ptype}**: ${avg:.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with st.expander("Highest Claim"):
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    highest = reports.get_highest_claim()
                    if highest:
                        st.markdown(f"**ID**: {highest.id} | **Amount**: ${highest.amount} | **Policyholder ID**: {highest.policyholder_id}")
                    else:
                        st.info("No claims found.")
                    st.markdown('</div>', unsafe_allow_html=True)

                with st.expander("Policyholders with Pending Claims"):
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    pending_phs = reports.get_policyholders_with_pending_claims()
                    if pending_phs:
                        for ph in pending_phs:
                            st.markdown(f"**ID**: {ph['id']} | **Name**: {ph['name']} | **Policy Type**: {ph['policy_type']}")
                            for claim in ph['claims']:
                                st.markdown(f"&nbsp;&nbsp;- **Claim ID**: {claim['id']} | **Amount**: ${claim['amount']} | **Reason**: {claim['reason']} | **Date**: {claim['date']}")
                    else:
                        st.info("No policyholders with pending claims.")
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating report: {e}")

if __name__ == "__main__":
    main()
