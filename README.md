# 🌍 BorderBuddies

> **"Ship Right or Ship Twice"**  
> A rapid compliance checker for cross-border shipments built using Streamlit, Gemini AI, and Python.

BorderBuddies simplifies international shipping for small exporters by providing an all-in-one dashboard to validate shipments, check regulations, and generate reports — reducing manual errors and delays.

---

##  Project Summary

BorderBuddies is a real-time export compliance system that:

- Collects shipment details
- Checks country-wise and item-based restrictions
- Flags potential violations (like banned combinations or destination conflicts)
- Enables order tracking and split shipment management
- Generates downloadable reports (CSV/PDF)
- Integrates a Gemini-powered chatbot for compliance Q&A
- Provides updated shipping regulations via AI

---

##  Key Features

###  1. **Shipment Entry & Validation**
- Collects: sender/recipient country, item types, value, weight, shipping service
- Validates:
  - Missing fields
  - Country-specific restricted items (`RESTRICTED_ITEMS`)
  - Country-to-country conflict (`CONFLICTING_DESTINATIONS`)
  - Conflicting item pairs (`ITEM_CONFLICTS`)
- Weight limit: max 30kg per container

###  2. **Split Shipment Handling**
- If weight > 30kg, prompts user to split
- Asks for:
  - Number of containers
  - Weight & value per container
  - Items per container
- Submits each container as a separate shipment under the same Order ID

###  3. **Order & Tracking System**
- Unique Order ID: `ORD-######`
- Unique Tracking ID per container: `TRK-######`
- Uses `st.session_state` to manage all shipment data persistently

###  4. **Analytics Dashboard**
- Displays all shipments in a table
- Allows downloading reports:
  - `.csv`: DataFrame export
  - `.pdf`: Custom formatted report using FPDF

### 5. **Tracking Page**
- Enter Order ID to view all containers
- Shows status, origin, destination, value, and items

###  6. **AI-Powered Compliance Chatbot**
- Asks compliance-related questions
- Powered by Google Gemini AI via `google.generativeai`
- Function: `compliance_chatbot(user_query)`

###  7. **Regulation Update Generator**
- Provides latest shipping rules per origin, destination, and item
- Uses Gemini AI to generate summaries and external news links
- Function: `get_generated_regulation_updates(sender, recipient, items)`

---

## 🏗System Architecture

### High-Level Flow:
1. **UI Form** → Collects shipment details via Streamlit
2. **Rule Engine** → Validates with multiple rule sets
3. **Storage** → Data stored in Streamlit's session state
4. **PDF/CSV Generator** → Export report options
5. **Gemini AI Calls** → For chatbot and updates

### Rule Sets Defined:
- `RESTRICTED_ITEMS`
- `CONFLICTING_DESTINATIONS`
- `ITEM_CONFLICTS`
- Weight limits: 1kg–30kg

---

##  Demo Preview

### UI Screenshot:
<img width="1304" alt="image" src="https://github.com/user-attachments/assets/4983ffbd-f763-4b23-a3d0-462b6f523040" />

###  Validation Errors for Restricted Items and Conflicts
The app flags any restricted items based on destination (e.g., Perishable in USA) and incompatible item combinations (e.g., Knives + Electronics).

<img width="767" alt="image" src="https://github.com/user-attachments/assets/6ae125dc-ea66-4ab0-bafd-d2ddb09583a3" />

###  Weight Limit Exceeded Warning
If the shipment weight exceeds 30 kg, the app immediately prompts the user to split the shipment into multiple containers.
<img width="775" alt="image" src="https://github.com/user-attachments/assets/66977bbd-ec18-4eca-98c6-47f71950d55d" />
### 📦 Split Shipment Form
When splitting is required, users can enter the number of containers and assign specific weights, declared values, and item types to each.

<img width="776" alt="image" src="https://github.com/user-attachments/assets/ca0bd978-070e-4e22-8f54-91ddd9a2ba41" />


<img width="756" alt="image" src="https://github.com/user-attachments/assets/4a9d7f19-7408-434d-a796-02f224791cde" />


asking chatbot
<img width="789" alt="image" src="https://github.com/user-attachments/assets/0e03df3b-7d24-4cea-871b-3952fb7cc3a0" />



<img width="1278" alt="image" src="https://github.com/user-attachments/assets/277d4d81-9e86-4d62-ab12-05cb0d8b190d" />

<img width="1372" alt="image" src="https://github.com/user-attachments/assets/8cc1d3a7-5615-4a49-a48c-6b554c6aca2d" />

### Sample Report:
<img width="693" alt="image" src="https://github.com/user-attachments/assets/e29721d3-beed-43c0-8915-ffffbce47257" />

---

##  Technologies Used

| Tool | Role |
|------|------|
| **Streamlit** | Interactive front-end app |
| **Pandas** | Data handling |
| **FPDF** | PDF report generation |
| **Google Generative AI (Gemini)** | Real-time compliance answers + regulation updates |
| **Python** | Backend + logic |
| **Session State** | In-app persistent memory |

---

##  Setup Instructions

###  Requirements

Install the dependencies:

```bash
pip install -r requirements.txt
