import streamlit as st
import pandas as pd

from compare_engine import compare_excel_files

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="SAC Compare Tool",
    layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================
def load_css():

    try:

        with open("styles.css") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    except:
        pass

load_css()

# ==========================================
# TITLE
# ==========================================
st.title("📊 SAC Model Comparison Tool")

st.markdown("""
Compare SAC exports using Excel files.

### Features
- Compare Measures
- Compare Dimensions
- Compare Widgets
- Detect Missing Items
- Generate Downloadable Report
""")

st.markdown("---")

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.header("📂 Upload Files")

excel_a = st.sidebar.file_uploader(
    "Upload Excel File A",
    type=["xlsx"]
)

excel_b = st.sidebar.file_uploader(
    "Upload Excel File B",
    type=["xlsx"]
)

# ==========================================
# MAIN
# ==========================================
if excel_a and excel_b:

    try:

        # ==========================================
        # LOAD EXCEL SHEETS
        # ==========================================
        workbook_a = pd.read_excel(
            excel_a,
            sheet_name=None
        )

        workbook_b = pd.read_excel(
            excel_b,
            sheet_name=None
        )

        # ==========================================
        # SHOW SHEETS
        # ==========================================
        st.subheader("📑 Sheets Found")

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Excel A Sheets")
            st.write(list(workbook_a.keys()))

        with col2:

            st.write("### Excel B Sheets")
            st.write(list(workbook_b.keys()))

        st.markdown("---")

        # ==========================================
        # COMPARE FILES
        # ==========================================
        result_df = compare_excel_files(
            workbook_a,
            workbook_b
        )

        # ==========================================
        # EMPTY CHECK
        # ==========================================
        if result_df.empty:

            st.error("""
No comparison data found.

Make sure both Excel files contain:
- Measures sheet
- Dimensions sheet
- Widgets sheet
""")

        else:

            # ==========================================
            # METRICS
            # ==========================================
            total_items = len(result_df)

            matched_items = len(
                result_df[
                    result_df["Status"] == "Same"
                ]
            )

            missing_items = len(
                result_df[
                    result_df["Status"] != "Same"
                ]
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Total Items",
                    total_items
                )

            with col2:

                st.metric(
                    "Matched",
                    matched_items
                )

            with col3:

                st.metric(
                    "Differences",
                    missing_items
                )

            st.markdown("---")

            # ==========================================
            # FILTER OPTION
            # ==========================================
            filter_option = st.selectbox(

                "Filter Results",

                [
                    "All",
                    "Same",
                    "Missing in A",
                    "Missing in B"
                ]

            )

            if filter_option == "All":

                filtered_df = result_df

            else:

                filtered_df = result_df[
                    result_df["Status"] == filter_option
                ]

            # ==========================================
            # RESULT TABLE
            # ==========================================
            st.subheader("📋 Comparison Result")

            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=600
            )

            st.markdown("---")

            # ==========================================
            # DIFFERENCE REPORT
            # ==========================================
            st.subheader("⚠ Difference Report")

            diff_df = result_df[
                result_df["Status"] != "Same"
            ]

            if not diff_df.empty:

                st.dataframe(
                    diff_df,
                    use_container_width=True,
                    height=400
                )

            else:

                st.success(
                    "✅ No Differences Found"
                )

            st.markdown("---")

            # ==========================================
            # EXPORT EXCEL
            # ==========================================
            export_path = "/tmp/sac_compare_result.xlsx"

            result_df.to_excel(
                export_path,
                index=False
            )

            with open(export_path, "rb") as file:

                st.download_button(

                    label="⬇ Download Comparison Excel",

                    data=file,

                    file_name="sac_compare_result.xlsx",

                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                )

    except Exception as e:

        st.error(
            f"Application Error: {e}"
        )

# ==========================================
# EMPTY STATE
# ==========================================
else:

    st.info(
        "⬅ Upload two Excel files to start comparison"
    )

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")

st.caption(
    "SAC Story / Model Comparison Tool"
)
