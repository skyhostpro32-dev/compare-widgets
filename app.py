import streamlit as st
import pandas as pd

from compare_engine import compare_excel_files

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SAC Compare Tool",
    layout="wide"
)

# =========================
# LOAD CSS
# =========================
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

# =========================
# TITLE
# =========================
st.title("📊 SAC Measure / Dimension Compare Tool")

st.markdown("""
Upload two SAC Excel exports and compare:

- Measures
- Dimensions
- Widgets
- Missing Items
- Matching Items
""")

st.markdown("---")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Upload Excel Files")

excel_a = st.sidebar.file_uploader(
    "Upload Excel A",
    type=["xlsx"]
)

excel_b = st.sidebar.file_uploader(
    "Upload Excel B",
    type=["xlsx"]
)

# =========================
# MAIN
# =========================
if excel_a and excel_b:

    try:

        # =========================
        # LOAD ALL SHEETS
        # =========================
        workbook_a = pd.read_excel(
            excel_a,
            sheet_name=None
        )

        workbook_b = pd.read_excel(
            excel_b,
            sheet_name=None
        )

        # =========================
        # COMPARE
        # =========================
        result_df = compare_excel_files(
            workbook_a,
            workbook_b
        )

        # =========================
        # SUMMARY METRICS
        # =========================
        total_items = len(result_df)

        same_count = len(
            result_df[
                result_df["Status"] == "Same"
            ]
        )

        diff_count = len(
            result_df[
                result_df["Status"] != "Same"
            ]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Items",
            total_items
        )

        col2.metric(
            "Matched",
            same_count
        )

        col3.metric(
            "Differences",
            diff_count
        )

        st.markdown("---")

        # =========================
        # FILTER
        # =========================
        filter_option = st.selectbox(
            "Filter Status",
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

        # =========================
        # SHOW RESULT
        # =========================
        st.subheader("📋 Comparison Result")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=600
        )

        # =========================
        # DIFFERENCE TABLE
        # =========================
        st.markdown("---")

        st.subheader("⚠ Difference Report")

        diff_df = result_df[
            result_df["Status"] != "Same"
        ]

        if not diff_df.empty:

            st.dataframe(
                diff_df,
                use_container_width=True
            )

        else:

            st.success("✅ No Differences Found")

        # =========================
        # EXPORT EXCEL
        # =========================
        st.markdown("---")

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

        st.error(f"Application Error: {e}")

else:

    st.info("⬅ Upload both Excel files to start comparison")

# =========================
# FOOTER
# =========================
st.markdown("---")

st.caption("SAC Story Compare Tool")
