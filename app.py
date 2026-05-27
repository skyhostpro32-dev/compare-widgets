import streamlit as st
import pandas as pd

from compare_engine import compare_excel_files

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SAC Excel Compare Tool",
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
st.title("📊 SAC Excel Compare Tool")

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

        # READ EXCEL FILES
        df_a = pd.read_excel(excel_a)

        df_b = pd.read_excel(excel_b)

        # COMPARE
        result_df = compare_excel_files(
            df_a,
            df_b
        )

        # =========================
        # SHOW RESULT
        # =========================
        st.subheader("📋 Comparison Result")

        st.dataframe(
            result_df,
            use_container_width=True
        )

        # =========================
        # DIFFERENCE FILTER
        # =========================
        different_rows = result_df[
            result_df["Status"] == "Different"
        ]

        st.markdown("---")

        if not different_rows.empty:

            st.warning("⚠ Differences Found")

            st.dataframe(
                different_rows,
                use_container_width=True
            )

        else:

            st.success("✅ Both Excel Files Match")

        # =========================
        # EXPORT RESULT
        # =========================
        excel_path = "/tmp/compare_result.xlsx"

        result_df.to_excel(
            excel_path,
            index=False
        )

        with open(excel_path, "rb") as file:

            st.download_button(
                label="⬇ Download Compare Result",
                data=file,
                file_name="compare_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:

        st.error(f"Application Error: {e}")

else:

    st.info("⬅ Upload two Excel files")

# =========================
# FOOTER
# =========================
st.markdown("---")

st.caption("SAC Excel Compare Tool")
