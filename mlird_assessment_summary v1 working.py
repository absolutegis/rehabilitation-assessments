import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Streamlit App
st.title("RCW 87.84 Rehabilitation Assessments QA/QC")

# File Upload
uploaded_file = st.file_uploader("Upload your assessment CSV file", type=["csv"])
if uploaded_file:
    # Load the data
    data = pd.read_csv(uploaded_file)

    # Fix PARCEL formatting
    if "PARCEL" in data.columns:
        # Ensure PARCEL numbers are 9 digits with no commas
        data["PARCEL"] = data["PARCEL"].astype(str).str.zfill(9).str.replace(",", "")
    
    # Summarize results
    categories = {
        "Residential Waterfront": "RES Waterfront Point Comp. to Col. BU",
        "Commercial Waterfront": "COM Waterfront Point Comp. to Col. BU",
        "Parks Waterfront": "PARKS Waterfront Point Comp. to Col. BU",
        "Residential Non-Waterfront": "RES NON-Waterfront Point Comp. to Col. BU",
        "Commercial Non-Waterfront": "COM NON-Waterfront Point Comp. to Col. BU",
        "Farms Non-Waterfront": "FARMS NON-Waterfront Point Comp. to Col. BU",
    }
    
    summary = {}
    for category, column in categories.items():
        good_count = data[data[column] == "good"].shape[0]
        bad_count = data[data[column] == "bad"].shape[0]
        summary[category] = {"Good": good_count, "Bad": bad_count}
    
    # Create a summary DataFrame
    summary_df = pd.DataFrame.from_dict(summary, orient="index")
    summary_df.reset_index(inplace=True)
    summary_df.columns = ["Category", "Good", "Bad"]
    
    # Display summary table
    st.subheader("Summary Table")
    st.dataframe(summary_df)
    
    # Visualization
    st.subheader("Good vs. Bad Points by Category")
    fig, ax = plt.subplots()
    summary_df.set_index("Category")[["Good", "Bad"]].plot(kind="bar", ax=ax)
    ax.set_ylabel("Count")
    ax.set_title("Good vs. Bad Points")
    st.pyplot(fig)
    
    # Detailed Table (Optional)
    st.subheader("Detailed Data (Optional)")
    with st.expander("View Detailed Table"):
        st.dataframe(data) 