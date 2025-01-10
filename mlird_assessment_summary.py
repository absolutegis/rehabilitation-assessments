import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Helper function to style "Good" and "Bad" cells
def highlight_good_bad(val):
    if val == "good":
        return "background-color: rgba(0, 255, 0, 0.2);"  # Semi-transparent green
    elif val == "bad":
        return "background-color: rgba(255, 0, 0, 0.2);"  # Semi-transparent red
    return ""  # No style

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
    
    # Identify Records with Multiple "Bad" Categories
    st.subheader("Records with Multiple 'Bad' Categories")
    bad_columns = [column for column in categories.values()]
    data["Bad_Count"] = data[bad_columns].apply(lambda row: sum(row == "bad"), axis=1)
    multiple_bad_records = data[data["Bad_Count"] > 1]
    st.write(f"Total Records with Multiple 'Bad' Categories: {multiple_bad_records.shape[0]}")

    # Display only "Bad" records with highlighting
    styled_multiple_bad = multiple_bad_records.style.applymap(
        highlight_good_bad,
        subset=bad_columns
    )
    st.dataframe(styled_multiple_bad, use_container_width=True)

    # Breakdown of "Bad" Reasons
    st.subheader("Breakdown of 'Bad' Reasons")
    bad_breakdown = {
        category: data[data[column] == "bad"].shape[0]
        for category, column in categories.items()
    }
    bad_breakdown_df = pd.DataFrame(list(bad_breakdown.items()), columns=["Category", "Bad Count"])
    st.dataframe(bad_breakdown_df)

    # Filter the Detailed Table
    st.subheader("Filter the Detailed Table")
    selected_category = st.selectbox("Filter by Category", ["All"] + list(categories.keys()))
    if selected_category != "All":
        filtered_data = data[data[categories[selected_category]] == "bad"]
        styled_filtered = filtered_data.style.applymap(
            highlight_good_bad,
            subset=[categories[selected_category]]
        )
        st.dataframe(styled_filtered, use_container_width=True)
    else:
        # Show unstyled full detailed table for performance
        st.dataframe(data, use_container_width=True)

    # Summary Statistics for "Bad" Data
    st.subheader("Summary Statistics for 'Bad' Data")
    total_bad_records = data["Bad_Count"].sum()
    multiple_issues_count = multiple_bad_records.shape[0]
    st.write(f"Total 'Bad' Records: {total_bad_records}")
    st.write(f"Records with Multiple Issues: {multiple_issues_count}")

    # Visualization of "Bad" Reasons
    st.subheader("Visualization of 'Bad' Counts by Category")
    fig, ax = plt.subplots()
    bad_breakdown_df.plot(kind="bar", x="Category", y="Bad Count", ax=ax, legend=False)
    ax.set_ylabel("Bad Count")
    st.pyplot(fig)

    # Detailed Table (Optional)
    st.subheader("Detailed Data (Optional)")
    with st.expander("View Detailed Table"):
        st.dataframe(data, use_container_width=True)  # Unstyled full table for performance
