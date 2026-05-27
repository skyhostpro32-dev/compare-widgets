import pandas as pd

def compare_excel_files(df_a, df_b):

    # CONVERT TO STRING
    df_a = df_a.astype(str)

    df_b = df_b.astype(str)

    # GET ALL VALUES
    values_a = set(df_a.stack())

    values_b = set(df_b.stack())

    all_values = sorted(
        values_a.union(values_b)
    )

    results = []

    for item in all_values:

        in_a = item in values_a
        in_b = item in values_b

        status = (
            "Same"
            if in_a and in_b
            else "Different"
        )

        results.append({
            "Value": item,
            "Excel A": "Yes" if in_a else "No",
            "Excel B": "Yes" if in_b else "No",
            "Status": status
        })

    return pd.DataFrame(results)
