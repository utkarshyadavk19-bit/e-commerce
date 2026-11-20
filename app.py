import streamlit as st
import pandas as pd
import pickle

# Page setup
st.set_page_config(
    page_title="Online Shoppers Purchasing Intention",
    page_icon="🛒",
    layout="centered"
)

# Load saved model, scaler, and training columns
@st.cache_resource
def load_artifacts():
    with open("best_shopper_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("feature_columns.pkl", "rb") as f:
        feature_cols = pickle.load(f)
    return model, scaler, feature_cols

model, scaler, feature_cols = load_artifacts()

# Header
st.title("🛒 Online Shoppers Purchasing Intention")
st.write("Enter a visitor's browsing behaviour below to predict whether they will complete a purchase.")
st.divider()

# Input layout (two columns for a clean dashboard look)
col1, col2 = st.columns(2)

with col1:
    product_pages = st.number_input("Product Pages Visited", min_value=0, max_value=300, value=20, step=1)
    product_duration = st.number_input("Time on Product Pages (seconds)", min_value=0.0, max_value=5000.0, value=600.0, step=10.0)
    admin_pages = st.number_input("Account / Admin Pages Visited", min_value=0, max_value=50, value=2, step=1)
    page_values = st.slider("Page Values", min_value=0.0, max_value=100.0, value=25.0, step=0.5)

with col2:
    bounce_rate = st.slider("Bounce Rate", min_value=0.0, max_value=0.20, value=0.01, step=0.005, format="%.3f")
    exit_rate = st.slider("Exit Rate", min_value=0.0, max_value=0.20, value=0.02, step=0.005, format="%.3f")
    month = st.selectbox("Month", ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], index=8)
    visitor_type = st.selectbox("Visitor Type", ["Returning_Visitor", "New_Visitor", "Other"])
    is_weekend = st.checkbox("Weekend Visit", value=True)

st.divider()

# Predict button
if st.button("Predict Purchase Intention", type="primary", use_container_width=True):
    # Initialize 1-row DataFrame matching exact training columns
    input_df = pd.DataFrame(0.0, index=[0], columns=feature_cols)

    # Fill numerical & boolean features
    input_df.at[0, "ProductRelated"] = product_pages
    input_df.at[0, "ProductRelated_Duration"] = product_duration
    input_df.at[0, "Administrative"] = admin_pages
    input_df.at[0, "Administrative_Duration"] = admin_pages * 25.0
    input_df.at[0, "PageValues"] = page_values
    input_df.at[0, "BounceRates"] = bounce_rate
    input_df.at[0, "ExitRates"] = exit_rate
    input_df.at[0, "Weekend"] = 1 if is_weekend else 0

    # Standard defaults for background session metadata
    for col, default_val in [("OperatingSystems", 2), ("Browser", 2), ("Region", 1), ("TrafficType", 2)]:
        if col in input_df.columns:
            input_df.at[0, col] = default_val

    # Set One-Hot Encoded Month & VisitorType columns
    month_col = f"Month_{month}"
    if month_col in input_df.columns:
        input_df.at[0, month_col] = 1

    visitor_col = f"VisitorType_{visitor_type}"
    if visitor_col in input_df.columns:
        input_df.at[0, visitor_col] = 1

    # Scale inputs using the saved StandardScaler and predict
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]

    # Display result
    if prediction == 1:
        st.success("### High Intent: Visitor WILL Purchase")
    else:
        st.warning("### Low Intent: Visitor will NOT Purchase")

    # Show confidence bar if supported by the winning model
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(input_scaled)[0][1])
        st.metric("Estimated Purchase Probability", f"{prob * 100:.2f}%")
        st.progress(prob)
