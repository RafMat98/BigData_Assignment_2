import streamlit as st
import requests

st.title("Πρόβλεψη Μηνιαίας Χρέωσης")

# Widgets για είσοδο δεδομένων
age = st.number_input("Ηλικία", 18, 90)
tenure = st.slider("Μήνες Συνεργασίας", 1, 120)
complaints = st.number_input("Παράπονα ανα μήνα", 0,20)
calls = st.number_input("Κλήσεις τεχνικής υποστήριξης", 0,100)
has_phone_label = st.selectbox('Υπηρεσία Τηλεφώνου;', ['Ναι', 'Όχι'])
has_phone = 1 if has_phone_label == 'Ναι' else 0
has_internet_label = st.selectbox('Υπηρεσία Ιντερνετ;', ['Ναι', 'Όχι'])
has_internet = 1 if has_internet_label == 'Ναι' else 0
has_tv_label = st.selectbox('Υπηρεσία Τηλεόρασης;', ['Ναι', 'Όχι'])
has_tv = 1 if has_tv_label == 'Ναι' else 0
num_services = has_phone + has_internet + has_tv
contract_type = st.selectbox('Τύπος Συμβολαίου;', ['Month-to-month', 'One year', 'Two year'])
payment_method = st.selectbox('Τρόπος Πληρωμής;', ['Cash', 'Credit card', 'E-banking', 'Bank transfer'])
# ... πρόσθεσε και τα υπόλοιπα πεδία (CONTRACT_TYPE κλπ)

if st.button("Υπολόγισε Χρέωση"):
    # Τα δεδομένα που περιμένει το μοντέλο
    payload = {
        "AGE": age,
        "TENURE_MONTHS": tenure,
        "NUM_COMPLAINTS": complaints,  # Παράδειγμα
        "SUPPORT_CALLS": calls,
        "HAS_INTERNET": has_internet,
        "HAS_MOBILE": has_phone,
        "HAS_TV": has_tv,
        "NUM_SERVICES": num_services,
        "CONTRACT_TYPE": contract_type,
        "PAYMENT_METHOD": payment_method,
        "COUNTRY": "GR"
    }
    if num_services == 0:
        st.error("Σφάλμα: Πρέπει να επιλέξετε τουλάχιστον μία υπηρεσία (Τηλέφωνο, Ίντερνετ ή Τηλεόραση).")
        st.stop()  # Σταματάει την εκτέλεση εδώ, δεν προχωράει στο requests.post
    # Κλήση του API (χρησιμοποιούμε το όνομα του service στο docker-compose)
    response = requests.post("http://web-api:5000/predict", json=payload)
    
    if response.status_code == 200:
        prediction = response.json()["predicted_charges"]
        st.success(f"Η προβλεπόμενη χρέωση είναι: {prediction} €")