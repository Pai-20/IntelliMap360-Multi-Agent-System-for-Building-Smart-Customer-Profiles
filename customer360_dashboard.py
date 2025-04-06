import streamlit as st
import pandas as pd

# -----------------------
# Functions from Multi-Agent System
# -----------------------
def interpret_use_case(use_case_text):
    keywords = {
        "customer_identification": ["name", "customer_id", "contact", "email", "phone"],
        "demographics": ["age", "gender", "location", "dob"],
        "transactions": ["transaction", "debit", "credit", "spending"],
        "loans": ["loan", "mortgage", "credit score", "emi"],
        "preferences": ["channel", "sms", "email_opt_in"]
    }
    output = {key: [] for key in keywords}
    for key, terms in keywords.items():
        for term in terms:
            if term in use_case_text.lower():
                output[key].append(term)
    return output

def recommend_data_product_structure(use_case_summary):
    structure = []
    for domain, terms in use_case_summary.items():
        if domain == 'customer_identification':
            structure += ['Customer_ID', 'Full_Name', 'Email', 'Phone_Number']
        elif domain == 'demographics':
            structure += ['DOB', 'Gender', 'City']
        elif domain == 'transactions':
            structure += ['Last_Transaction_Date', 'Monthly_Spend', 'Transaction_Count']
        elif domain == 'loans':
            structure += ['Loan_Amount', 'Loan_Status', 'Credit_Score']
        elif domain == 'preferences':
            structure += ['Preferred_Channel', 'Email_Opt_In']
    return list(set(structure))

def identify_sources(attributes):
    catalog = {
        'Customer_ID': 'CRM_DB',
        'Full_Name': 'CRM_DB',
        'Email': 'CRM_DB',
        'Phone_Number': 'CRM_DB',
        'DOB': 'KYC_DB',
        'Gender': 'KYC_DB',
        'City': 'KYC_DB',
        'Last_Transaction_Date': 'TXN_DB',
        'Monthly_Spend': 'TXN_DB',
        'Transaction_Count': 'TXN_DB',
        'Loan_Amount': 'LOAN_DB',
        'Loan_Status': 'LOAN_DB',
        'Credit_Score': 'CREDIT_BUREAU',
        'Preferred_Channel': 'CHANNEL_PREF_SYS',
        'Email_Opt_In': 'CHANNEL_PREF_SYS'
    }
    return {attr: catalog.get(attr, "UNKNOWN") for attr in attributes}

def generate_mapping(attributes, sources):
    mapping = []
    for attr in attributes:
        mapping.append({
            'Target_Attribute': attr,
            'Source_System': sources[attr],
            'Source_Attribute': attr,
            'Transformation': 'Direct' if sources[attr] != "UNKNOWN" else 'Manual Mapping Required'
        })
    return pd.DataFrame(mapping)

def define_ingress_egress():
    return {
        "Ingress": {
            "Method": "Batch + Streaming",
            "Tools": ["Apache NiFi", "Kafka", "Azure Data Factory"]
        },
        "Egress": {
            "Access Methods": ["REST API", "Power BI Dataset", "Snowflake View"],
            "Auth": "OAuth2 with RBAC"
        }
    }

def certify_data_product(mapping_df):
    checks = {
        'Completeness': mapping_df['Source_Attribute'].notnull().all(),
        'Mapping Coverage': len(mapping_df) > 0,
        'Transformation Specified': mapping_df['Transformation'].notnull().all()
    }
    result = all(checks.values())
    return result, checks

# -----------------------
# Streamlit Dashboard
# -----------------------
st.set_page_config(page_title="Customer 360 Agent Dashboard", layout="wide")
st.title("🤖 Customer 360 Data Product Builder")

use_case_text = st.text_area("📋 Enter Use Case Description", "The marketing team wants a unified customer profile to launch personalized cross-sell campaigns. Required fields include name, contact info, demographics, transaction behavior, loan history, and channel preferences.")

if st.button("Run Multi-Agent System"):
    st.subheader("1️⃣ Use Case Interpretation")
    summary = interpret_use_case(use_case_text)
    st.json(summary)

    st.subheader("2️⃣ Target Data Product Structure")
    structure = recommend_data_product_structure(summary)
    st.write(structure)

    st.subheader("3️⃣ Source System Identification")
    sources = identify_sources(structure)
    st.json(sources)

    st.subheader("4️⃣ Attribute Mapping")
    mapping_df = generate_mapping(structure, sources)
    st.dataframe(mapping_df)

    st.subheader("5️⃣ Ingress & Egress Design")
    ie = define_ingress_egress()
    st.write("**Ingress:**", ie['Ingress'])
    st.write("**Egress:**", ie['Egress'])

    st.subheader("6️⃣ Data Product Certification")
    certified, checks = certify_data_product(mapping_df)
    st.write("✔️ Certification Status:", "PASSED" if certified else "❌ FAILED")
    st.write(checks)

    st.success("Multi-Agent Flow Complete ✅")
