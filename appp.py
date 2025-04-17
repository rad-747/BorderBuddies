import streamlit as st
import random
import pandas as pd
from fpdf import FPDF  # Import FPDF for PDF generation  

import google.generativeai as genai

import io  # Add this import for handling PDF buffer

def generate_report():
    if not st.session_state.shipments:
        return None
    df = pd.DataFrame(st.session_state.shipments)
    return df.to_csv(index=False)

def generate_pdf():
    if not st.session_state.shipments:
        return None

    pdf = FPDF()
    pdf.add_page()
    
    # Set up automatic page breaks and margins
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Header
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 0, 128)  # Dark blue text
    pdf.cell(0, 10, "Shipment Report", ln=True, align="C")
    pdf.ln(10)  # Add a line break
    
    # Reset font and text color for the body
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)  # Black text

    # Loop through each shipment and display its details in a structured format
    for shipment in st.session_state.shipments:
        # Header for each shipment block
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Order ID: {shipment['order_id']}", ln=True)
        
        # Details for each shipment
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Tracking ID: {shipment['tracking_id']}", ln=True)
        pdf.cell(0, 8, f"Sender: {shipment['sender_name']} ({shipment['sender_country']})", ln=True)
        pdf.cell(0, 8, f"Recipient: {shipment['recipient_country']}", ln=True)
        pdf.cell(0, 8, f"Items: {', '.join(shipment['item_type'])}", ln=True)
        pdf.cell(0, 8, f"Declared Value: ${shipment['declared_value']}", ln=True)
        pdf.cell(0, 8, f"Weight: {shipment['weight']} kg", ln=True)
        pdf.cell(0, 8, f"Shipping Service: {shipment['shipping_service']}", ln=True)
        pdf.cell(0, 8, f"Status: {shipment['status']}", ln=True)
        pdf.ln(5)  # Space between shipments

        # Optionally, you can add a horizontal line between shipments for clarity:
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
    
    # Generate the PDF content as a string, then encode it to bytes
    pdf_data = pdf.output(dest="S").encode("latin1")
    buffer = io.BytesIO(pdf_data)
    buffer.seek(0)
    return buffer



# -----------------------
# Configuration and Data
# -----------------------

RESTRICTED_ITEMS = {
    "USA": ["Lithium Battery", "Perishable"],
    "Canada": ["Knives", "Electronics"],
    "UK": ["Medicine"],
    "Australia": ["Perishable"],
    "India": ["Perishable"],
    "Saudi Arabia": ["Alcohol"],
    "UAE": ["Alcohol"],
    "Singapore": ["Medicine"],
    "Japan": ["Medicine"],
    "Germany": ["Chemicals"],
}

CONFLICTING_DESTINATIONS = {
    "India": ["Canada"],
    "USA": ["Cuba", "North Korea", "Iran", "Syria"],
    "EU": ["Russia"],
}

ITEM_CONFLICTS = [
    {"Lithium Battery", "Alcohol"},
    {"Medicine", "Perishable"},
    {"Knives", "Electronics"},
    {"Chemicals", "Food Items"},
    {"Electronics", "Flammable"},
]

MAX_WEIGHT_KG = 30.0  
MIN_WEIGHT_KG = 1.0   

genai.configure(api_key=st.secrets["GEN_AI_API_KEY"])

def generate_order_id():
    """Generates a unique Order ID."""
    return f"ORD-{random.randint(100000, 999999)}"

def generate_tracking_id():
    """Generates a unique Tracking ID."""
    return f"TRK-{random.randint(100000, 999999)}"


# Initialize session state
if 'shipments' not in st.session_state:
    st.session_state.shipments = []
if 'tracking_data' not in st.session_state:
    st.session_state.tracking_data = {}
if 'selected_countries' not in st.session_state:
    st.session_state.selected_countries = []
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []
if 'split_option' not in st.session_state:
    st.session_state.split_option = False

# -----------------------
# Compliance Chatbot & Regulation Updates using GenAI
# -----------------------

def compliance_chatbot(user_query):
    """ Generates compliance answers using Gemini AI. """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(user_query)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def get_generated_regulation_updates(sender_country, recipient_country, selected_items):
    """ Uses Gemini AI to generate compliance updates and provide news links. """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = f"""
        You are a global shipping compliance expert. Provide the latest shipping regulations and restrictions for shipping from {sender_country} to {recipient_country}.
        Consider the following items being shipped: {', '.join(selected_items)}.
        Mention any restrictions, required documentation, or safety guidelines.
        Also, provide reliable news links where this information can be verified.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error fetching regulation updates: {str(e)}"

# -----------------------
# Streamlit UI
# -----------------------

st.title("Export Compliance and Tracking System")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Shipment Entry", "Tracking", "Analytics", "Compliance Chatbot", "Regulation Updates"])


if page == "Shipment Entry":
    st.header("Enter Shipment Details")

    sender_name = st.text_input("Sender Name")
    sender_country = st.selectbox("Sender Country", list(RESTRICTED_ITEMS.keys()))
    recipient_country = st.selectbox("Recipient Country", list(RESTRICTED_ITEMS.keys()))
    item_type = st.multiselect("Item Type", ["Lithium Battery", "Perishable", "Medicine", "Knives", "Alcohol",
                                              "Electronics", "Clothing", "Food Items", "Cosmetics",
                                              "Chemicals", "Household Goods", "Automotive Parts",
                                              "Toys and Games", "Books", "Jewelry"])
    declared_value = st.number_input("Declared Value ($)", min_value=0.0, step=1.0)
    weight = st.number_input("Weight (kg)", min_value=MIN_WEIGHT_KG, step=1.0)
    shipping_service = st.selectbox("Shipping Service", ["DHL", "FedEx", "UPS", "USPS"])

    # Normal submission if weight is within limit
    if st.button("Check Compliance and Submit") and not st.session_state.split_option and weight <= MAX_WEIGHT_KG:
        errors = []

        if not sender_name or not recipient_country or not item_type or declared_value <= 0 or weight <= 0:
            errors.append("⚠️ Submission failed! Please enter all required fields: Sender Name, Recipient Country, Item Type, Declared Value, and Weight.")

        # Check for conflicting destinations
        if sender_country in CONFLICTING_DESTINATIONS and recipient_country in CONFLICTING_DESTINATIONS[sender_country]:
            errors.append(f"⚠️ Shipments from {sender_country} to {recipient_country} are not allowed.")

        # Check for restricted items in the recipient country
        restricted_in_recipient = RESTRICTED_ITEMS.get(recipient_country, [])
        for item in item_type:
            if item in restricted_in_recipient:
                errors.append(f"⚠️ {item} is restricted in {recipient_country}.")

        # Check for item conflicts
        selected_set = set(item_type)
        if len(selected_set) > 1:  # Only check if more than one item is selected
            for conflict_set in ITEM_CONFLICTS:
                if conflict_set.issubset(selected_set):
                    errors.append(f"⚠️ Items {', '.join(conflict_set)} cannot be shipped together.")

        # Display errors if any
        if errors:
            for err in errors:
                st.error(err)
        else:
            order_id = generate_order_id()
            tracking_id = generate_tracking_id()
            shipment = {
                "order_id": order_id,
                "tracking_id": tracking_id,
                "sender_name": sender_name,
                "sender_country": sender_country,
                "recipient_country": recipient_country,
                "item_type": item_type,
                "declared_value": declared_value,
                "weight": weight,
                "shipping_service": shipping_service,
                "status": "Processing"
            }
            st.session_state.shipments.append(shipment)
            st.session_state.tracking_data[tracking_id] = "Processing"
            st.success(f"Shipment submitted successfully! Order ID: {order_id}")

            st.session_state.selected_countries = [sender_country, recipient_country]
            st.session_state.selected_items = item_type

    if weight > MAX_WEIGHT_KG:
        st.error("More than 30kg in one container is not allowed. Please split the shipment.")
        if st.button("Split Shipment"):
            st.session_state.split_option = True

    if st.session_state.split_option:
        st.subheader("Split Shipment Details")
        num_containers = st.number_input("Number of Containers", min_value=2, step=1, value=2)

        # Evenly distribute the remaining weight after 30kg in the first container
        container_weights = [30.0]
        remaining_weight = weight - 30.0
        if num_containers > 1:
            for i in range(1, num_containers):
                container_weights.append(min(MAX_WEIGHT_KG, remaining_weight / (num_containers - 1)))

        user_weights = [
            st.number_input(
                f"Weight for Container {i+1} (kg)",
                min_value=MIN_WEIGHT_KG,
                max_value=MAX_WEIGHT_KG,
                step=1.0,
                value=float(container_weights[i])
            ) for i in range(num_containers)
        ]

        container_declared_values = [st.number_input(f"Declared Value for Container {i+1} ($)", min_value=0.0, step=1.0) for i in range(num_containers)]
        container_items = [st.multiselect(f"Item Type for Container {i+1}", item_type) for i in range(num_containers)]

        if st.button("Submit Split Shipments"):
            order_id = generate_order_id()  # Order ID is generated only after splitting details are provided
            for i in range(num_containers):
                tracking_id = generate_tracking_id()

                shipment = {
                    "order_id": order_id,
                    "tracking_id": tracking_id,
                    "sender_name": sender_name,
                    "sender_country": sender_country,
                    "recipient_country": recipient_country,
                    "item_type": container_items[i],
                    "declared_value": container_declared_values[i],
                    "weight": user_weights[i],
                    "shipping_service": shipping_service,
                    "status": "Processing"
                }
                st.session_state.shipments.append(shipment)
                st.session_state.tracking_data[tracking_id] = shipment

            st.session_state.split_option = False  # Reset after successful split shipment
            st.success(f"Split shipment submitted successfully! *Order ID: {order_id}*")


elif page == "Tracking":
    st.header("Track Your Shipment")

    order_id = st.text_input("Enter Order ID to Track Shipments:").strip()
    
    if st.button("Track"):
        filtered_shipments = [
            s for s in st.session_state.shipments 
            if s["order_id"].strip() == order_id
        ]
        
        if filtered_shipments:
            st.subheader(f"Tracking Details for Order ID: {order_id}")
            df = pd.DataFrame(filtered_shipments)
            st.dataframe(df)  # Display all shipments linked to the Order ID
        else:
            st.warning("Order ID not found. Please enter a valid Order ID.")



elif page == "Analytics":
    st.header("Shipment Analytics")
    if st.session_state.shipments:
        df = pd.DataFrame(st.session_state.shipments)
        st.dataframe(df)
        
        csv_report = generate_report()
        pdf_report = generate_pdf()

        if csv_report:
            st.download_button("Download CSV Report", csv_report, "shipment_report.csv", "text/csv")
        
        if pdf_report:
            st.download_button("Download PDF Report", pdf_report, "shipment_report.pdf", "application/pdf")
    else:
        st.write("No shipments recorded yet.")


elif page == "Compliance Chatbot":
    st.header("Ask the Compliance Chatbot")
    user_query = st.text_input("Enter your question about shipping compliance:")
    if st.button("Get Answer"):
        response = compliance_chatbot(user_query)
        st.write("Compliance Bot:", response)

elif page == "Regulation Updates":
    st.header("Latest Shipping Regulation Updates 🌎")

    if not st.session_state.selected_countries or not st.session_state.selected_items:
        st.warning("Please enter a shipment first to get personalized compliance updates.")
    else:
        updates = get_generated_regulation_updates(
            st.session_state.selected_countries[0], 
            st.session_state.selected_countries[1], 
            st.session_state.selected_items
        )
        st.markdown(updates)
        