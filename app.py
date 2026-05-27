import streamlit as st
import pandas as pd
from io import BytesIO

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="SAC Comparison Tool",
    layout="wide"
)

# =========================================
# TITLE
# =========================================
st.title("📊 SAC Story / Model Comparison Tool")

st.markdown("""
Upload two SAC exported Excel files.

The tool compares:

- Measures
- Dimensions
- Widgets
- Missing Fields
- Matching Fields
""")

st.markdown("---")

# =========================================
# SIDEBAR
# =========================================
st.sidebar.header("📂 Upload Files")

file_a = st.sidebar.file_uploader(
    "Upload Excel File A",
    type=["xlsx"]
)

file_b = st.sidebar.file_uploader(
    "Upload Excel File B",
    type=["xlsx"]
)

# =========================================
# HELPER FUNCTION
# =========================================
def extract_all_values(workbook):

    values = []

    for sheet_name, df in workbook.items():

        try:

            # Convert all values to string
            flat_values = (
                df.astype(str)
                .fillna("")
                .values
                .flatten()
            )

            for item in flat_values:

                clean_item = str(item).strip()

                if clean_item != "" and clean_item.lower() != "nan":

                    values.append({
                        "Sheet": sheet_name,
                        "Value": clean_item
                    })

        except:
            pass

    return pd.DataFrame(values)

# =========================================
# MAIN
# =========================================
if file_a and file_b:

    try:

        # =========================================
        # READ EXCEL
        # =========================================
        workbook_a = pd.read_excel(
            file_a,
            sheet_name=None
        )

        workbook_b = pd.read_excel(
            file_b,
            sheet_name=None
        )

        # =========================================
        # EXTRACT VALUES
        # =========================================
        df_a = extract_all_values(workbook_a)
        df_b = extract_all_values(workbook_b)

        # =========================================
        # UNIQUE VALUES
        # =========================================
        values_a = set(df_a["Value"].unique())
        values_b = set(df_b["Value"].unique())

        # =========================================
        # COMPARISON
        # =========================================
        all_values = sorted(
            list(values_a.union(values_b))
        )

        comparison_rows = []

        for value in all_values:

            in_a = value in values_a
            in_b = value in values_b

            if in_a and in_b:
                status = "Same"

            elif in_a and not in_b:
                status = "Missing in B"

            else:
                status = "Missing in A"

            comparison_rows.append({
                "Field": value,
                "Exists in A": "Yes" if in_a else "No",
                "Exists in B": "Yes" if in_b else "No",
                "Status": status
            })

        result_df = pd.DataFrame(comparison_rows)

        # =========================================
        # METRICS
        # =========================================
        total = len(result_df)

        same_count = len(
            result_df[result_df["Status"] == "Same"]
        )

        diff_count = len(
            result_df[result_df["Status"] != "Same"]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Fields", total)
        col2.metric("Matched", same_count)
        col3.metric("Differences", diff_count)

        st.markdown("---")

        # =========================================
        # FILTER
        # =========================================
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

        # =========================================
        # RESULT TABLE
        # =========================================
        st.subheader("📋 Comparison Result")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=600
        )

        # =========================================
        # DIFFERENCE TABLE
        # =========================================
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

        # =========================================
        # EXPORT EXCEL
        # =========================================
        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            result_df.to_excel(
                writer,
                index=False,
                sheet_name="Comparison"
            )

            diff_df.to_excel(
                writer,
                index=False,
                sheet_name="Differences"
            )

        output.seek(0)

        st.download_button(
            label="⬇ Download Comparison Report",
            data=output,
            file_name="sac_comparison_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error(f"Application Error: {e}")

# =========================================
# NO FILES
# =========================================
else:

    st.info("⬅ Upload both Excel files to start comparison")

# =========================================
# FOOTER
# =========================================
st.markdown("---")

st.caption("SAC Story / Model Comparison Tool")
