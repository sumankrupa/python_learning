import pandas as pd

def transform_data(master, updated):
    master = master.copy()
    updated = updated.copy()

    # ----------------------------
    # Master cleanup (ONLY master has these)
    # ----------------------------
    master["CurrentFlag"] = master["CurrentFlag"].fillna(1).astype(int)
    master["Version"] = master["Version"].fillna(1).astype(int)
    master["PrevLoyaltyTier"] = master["PrevLoyaltyTier"].astype(object)

    # current snapshot rows
    current_master = master[master["CurrentFlag"] == 1].copy()

    def norm(s):
        return s.fillna("").astype(str).str.strip()

    # ----------------------------
    # SCD4: Subscription History
    # ----------------------------
    left_df = updated[["CustomerID", "SubscriptionStart", "SubscriptionEnd"]]
    right_df = current_master[["CustomerID", "SubscriptionStart", "SubscriptionEnd"]]

    merged = left_df.merge(
        right_df,
        on="CustomerID",
        how="left",
        suffixes=("_upd", "_mst")
    )

    start_upd = merged["SubscriptionStart_upd"].fillna(pd.Timestamp("1900-01-01"))
    start_mst = merged["SubscriptionStart_mst"].fillna(pd.Timestamp("1900-01-01"))
    end_upd   = merged["SubscriptionEnd_upd"].fillna(pd.Timestamp("2100-01-01"))
    end_mst   = merged["SubscriptionEnd_mst"].fillna(pd.Timestamp("2100-01-01"))

    is_changed = (
        merged["SubscriptionStart_mst"].isna() |
        (start_upd != start_mst) |
        (end_upd != end_mst)
    )

    history_df = merged.loc[is_changed, [
        "CustomerID", "SubscriptionStart_upd", "SubscriptionEnd_upd"
    ]].copy()

    history_df.columns = ["CustomerID", "SubscriptionStart", "SubscriptionEnd"]
    history_df["LoadTS"] = pd.Timestamp.now()

    # ----------------------------
    # New vs existing customers
    # ----------------------------
    existing_ids = set(current_master["CustomerID"].astype(int))
    update_ids = set(updated["CustomerID"].astype(int))

    new_ids = update_ids - existing_ids
    common_ids = update_ids & existing_ids

    # ----------------------------
    # SCD1: overwrite Email/Phone (current row only)
    # ----------------------------
    for c in ["Email", "Phone"]:
        if c in master.columns and c in updated.columns and common_ids:
            col_map = updated.set_index("CustomerID")[c].to_dict()
            mask = (master["CurrentFlag"] == 1) & (master["CustomerID"].isin(common_ids))
            master.loc[mask, c] = master.loc[mask, "CustomerID"].map(col_map)

    # ----------------------------
    # SCD3: LoyaltyTier + PrevLoyaltyTier (same row)
    # ----------------------------
    if "LoyaltyTier" in master.columns and "LoyaltyTier" in updated.columns and common_ids:
        cur = master[(master["CurrentFlag"] == 1) & (master["CustomerID"].isin(common_ids))].copy()
        cur = cur.merge(updated[["CustomerID", "LoyaltyTier"]], on="CustomerID", how="left", suffixes=("", "_upd"))

        tier_changed = cur["LoyaltyTier_upd"].notna() & (norm(cur["LoyaltyTier_upd"]) != norm(cur["LoyaltyTier"]))
        changed_ids = set(cur.loc[tier_changed, "CustomerID"].astype(int))

        if changed_ids:
            mask = (master["CurrentFlag"] == 1) & (master["CustomerID"].isin(changed_ids))
            master.loc[mask, "PrevLoyaltyTier"] = master.loc[mask, "LoyaltyTier"].values

            tier_map = updated.set_index("CustomerID")["LoyaltyTier"].to_dict()
            master.loc[mask, "LoyaltyTier"] = master.loc[mask, "CustomerID"].map(tier_map)

    # ----------------------------
    # SCD2: Address change -> expire old row + insert new version row
    # ----------------------------
    if "Address" in master.columns and "Address" in updated.columns and common_ids:
        cur = master[(master["CurrentFlag"] == 1) & (master["CustomerID"].isin(common_ids))].copy()
        cur = cur.merge(updated[["CustomerID", "Address"]], on="CustomerID", how="left", suffixes=("", "_upd"))

        addr_changed = cur["Address_upd"].notna() & (norm(cur["Address_upd"]) != norm(cur["Address"]))
        addr_changed_ids = set(cur.loc[addr_changed, "CustomerID"].astype(int))

        if addr_changed_ids:
            expire_mask = (master["CurrentFlag"] == 1) & (master["CustomerID"].isin(addr_changed_ids))
            master.loc[expire_mask, "CurrentFlag"] = 0

            new_rows = master[expire_mask].copy()   # copy expired rows
            new_rows["Version"] = new_rows["Version"] + 1
            new_rows["CurrentFlag"] = 1

            addr_map = updated.set_index("CustomerID")["Address"].to_dict()
            new_rows["Address"] = new_rows["CustomerID"].map(addr_map)

            master = pd.concat([master, new_rows], ignore_index=True)

    # ----------------------------
    # Insert NEW customers into master
    # ----------------------------
    if new_ids:
        new_rows = updated[updated["CustomerID"].isin(new_ids)].copy()
        new_rows["CurrentFlag"] = 1
        new_rows["Version"] = 1
        new_rows["PrevLoyaltyTier"] = None

        # align schema to master
        for c in master.columns:
            if c not in new_rows.columns:
                new_rows[c] = None
        new_rows = new_rows[master.columns]

        master = pd.concat([master, new_rows], ignore_index=True)

    print("transform done")
    return master, history_df
