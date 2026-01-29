import pandas as pd

def transform_data(snap_df, dim_customer_df):

    snap = snap_df.copy()
    dim = dim_customer_df.copy()

    # ---- 0) CLEAN BAD CSV COLUMNS ----
    # drop common junk index cols
    for junk in ["Unnamed: 0", "index", "Index"]:
        if junk in snap.columns:
            snap = snap.drop(columns=[junk])
        if junk in dim.columns:
            dim = dim.drop(columns=[junk])

    # remove duplicate column names (very important)
    snap = snap.loc[:, ~snap.columns.duplicated()].copy()
    dim = dim.loc[:, ~dim.columns.duplicated()].copy()

    # ---- 1) PARSE DATES ----
    if "updated_at" not in snap.columns:
        raise ValueError("snap_df must have 'updated_at' column.")

    snap["updated_at"] = pd.to_datetime(snap["updated_at"], errors="coerce")
    dim["valid_from"] = pd.to_datetime(dim.get("valid_from"), errors="coerce")
    dim["valid_to"] = pd.to_datetime(dim.get("valid_to"), errors="coerce")

    # ---- 2) CURRENT ROWS ----
    dim_current = dim[dim["is_current"] == "Y"].copy()

    # ---- 3) CLASSIFY NEW vs EXISTING ----
    merged = snap.merge(
        dim_current[["customer_id"]],
        on="customer_id",
        how="left",
        indicator=True
    )

    new_customers = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])
    existing_customers = merged[merged["_merge"] == "both"].drop(columns=["_merge"])

    # ---- 4) DETECT CHANGES ----
    def norm(s):
        return s.fillna("").astype(str).str.strip().str.lower()

    tracked_cols = ["region", "loyalty_tier", "email"]

    # if any tracked col missing in snap, create it (prevents KeyError)
    for c in tracked_cols:
        if c not in snap.columns:
            snap[c] = None
        if c not in dim.columns:
            dim[c] = None

    merged1 = existing_customers.merge(
        dim_current[["customer_id"] + tracked_cols],
        on="customer_id",
        how="inner",
        suffixes=("_snap", "_dim")
    )

    change_mask = False
    for c in tracked_cols:
        change_mask = change_mask | (norm(merged1[f"{c}_snap"]) != norm(merged1[f"{c}_dim"]))

    changed_ids = merged1.loc[change_mask, "customer_id"].dropna().astype(int).unique().tolist()

    # ---- 5) SET SNAPSHOT / EXPIRE DATES ----
    snapshot_date = snap["updated_at"].max()
    if pd.isna(snapshot_date):
        raise ValueError("updated_at is missing/invalid in snapshot.")
    snapshot_date = snapshot_date.normalize()

    expire_date = snapshot_date - pd.Timedelta(days=1)
    OPEN_ENDED = pd.Timestamp("2100-01-01")

    # ---- 6) EXPIRE OLD CURRENT ROWS ----
    expire_mask = (dim["is_current"] == "Y") & (dim["customer_id"].isin(changed_ids))
    dim.loc[expire_mask, "valid_to"] = expire_date
    dim.loc[expire_mask, "is_current"] = "N"

    # ---- 7) NEXT SURROGATE KEY ----
    if "surrogate_key" not in dim.columns:
        raise ValueError("dim_customer_df must have 'surrogate_key' column.")

    if dim["surrogate_key"].notna().any():
        next_sk = int(pd.to_numeric(dim["surrogate_key"], errors="coerce").max()) + 1
    else:
        next_sk = 1

    # ---- helper: align any df to dim schema EXACTLY ----
    dim_cols = list(pd.Index(dim.columns).unique())  # unique + ordered

    def align_to_dim(df):
        df = df.copy()
        df = df.drop(columns=["updated_at"], errors="ignore")

        # add missing cols
        for c in dim_cols:
            if c not in df.columns:
                df[c] = None

        # keep only dim cols in same order
        return df.loc[:, dim_cols]

    # ---- 8) INSERT NEW VERSIONS FOR CHANGED ----
    if changed_ids:
        new_versions = snap[snap["customer_id"].isin(changed_ids)].copy()
        new_versions["valid_from"] = snapshot_date
        new_versions["valid_to"] = OPEN_ENDED
        new_versions["is_current"] = "Y"

        new_versions = new_versions.reset_index(drop=True)
        new_versions["surrogate_key"] = range(next_sk, next_sk + len(new_versions))
        next_sk += len(new_versions)

        new_versions = align_to_dim(new_versions)

        # DEBUG (print once)
        # print("DIM COLS:", len(dim_cols), "NEW_VERS COLS:", new_versions.shape[1])

        dim = pd.concat([dim, new_versions], ignore_index=True)

    # ---- 9) INSERT BRAND NEW CUSTOMERS ----
    if len(new_customers) > 0:
        new_rows = new_customers.copy()
        new_rows["valid_from"] = snapshot_date
        new_rows["valid_to"] = OPEN_ENDED
        new_rows["is_current"] = "Y"

        new_rows = new_rows.reset_index(drop=True)
        new_rows["surrogate_key"] = range(next_sk, next_sk + len(new_rows))
        next_sk += len(new_rows)

        new_rows = align_to_dim(new_rows)
        dim = pd.concat([dim, new_rows], ignore_index=True)

    return dim
