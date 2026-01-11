import pandas as pd

def load_and_process_data():
    # ========== EXTRACT ==========
    df_raw = pd.read_csv("data/supply_chain_data.csv")

    # ========== TRANSFORM ==========
    df = df_raw.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    df["total_lead_time"] = (
        df["manufacturing_lead_time"] + df["shipping_times"]
    )

    df["estimated_profit"] = (
        df["revenue_generated"] - df["costs"]
    )

    # ========== CLEANING ==========
    df = df.drop_duplicates()

    df["availability"] = df["availability"].astype(int)
    df["stock_levels"] = df["stock_levels"].astype(int)

    df["product_type"] = df["product_type"].str.lower().str.strip()
    df["customer_demographics"] = df["customer_demographics"].str.lower()

    # ========== TIME INDEX ==========
    df["time_index"] = range(len(df))

    return df
