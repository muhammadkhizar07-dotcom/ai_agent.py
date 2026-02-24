import streamlit as st
import pandas as pd
from PIL import Image

st.title("AI Ads Agent 🚀")

# --- MULTIPLE CSV UPLOAD ---
csv_files = st.file_uploader(
    "Upload Ads CSV files (Meta / Google Ads)",
    type=["csv"],
    accept_multiple_files=True
)

if csv_files:
    all_data = []
    for uploaded_file in csv_files:
        try:
            df = pd.read_csv(uploaded_file, sep=',', engine='python', on_bad_lines="skip")
            df['source_file'] = uploaded_file.name  # Track file origin
            all_data.append(df)
        except Exception as e:
            st.error(f"Error reading {uploaded_file.name}: {e}")
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        st.subheader("Combined CSV Preview")
        st.dataframe(combined_df.head(10))  # Show first 10 rows safely

        # --- DYNAMIC METRICS (only if columns exist, no data change) ---
        metrics_calculated = False
        if "Impressions" in combined_df.columns and "Clicks" in combined_df.columns:
            combined_df["CTR (%)"] = (combined_df["Clicks"] / combined_df["Impressions"] * 100).fillna(0)
            metrics_calculated = True
        if "Cost" in combined_df.columns and "Clicks" in combined_df.columns:
            combined_df["CPC"] = (combined_df["Cost"] / combined_df["Clicks"]).fillna(0)
            metrics_calculated = True
        if "Cost" in combined_df.columns and "Conversions" in combined_df.columns:
            combined_df["CPA"] = (combined_df["Cost"] / combined_df["Conversions"]).fillna(0)
            metrics_calculated = True

        if metrics_calculated:
            st.subheader("Calculated Metrics (Averages)")
            avg_metrics = {
                "Avg CTR (%)": combined_df["CTR (%)"].mean() if "CTR (%)" in combined_df else "N/A",
                "Avg CPC": combined_df["CPC"].mean() if "CPC" in combined_df else "N/A",
                "Avg CPA": combined_df["CPA"].mean() if "CPA" in combined_df else "N/A"
            }
            st.write(avg_metrics)
            st.subheader("CTR (%) Chart")
            st.bar_chart(combined_df[["CTR (%)"]])

# --- AD SCREENSHOT UPLOAD ---
image_file = st.file_uploader("Upload Ad Screenshot", type=["png", "jpg", "jpeg"])
if image_file:
    img = Image.open(image_file)
    st.image(img, caption="Screenshot") # Auto-fits to column