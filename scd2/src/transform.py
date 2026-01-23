import pandas as pd 


def transform_data(master,df):
    key = "CustomerID"
    tracked_col = "Address"
    
    if 'CurrentFlag' not in master.columns:
        master['CurrentFlag'] = 1
    if 'Version' not in master.columns:
        master['Version'] = 1
    
    current_master = master[master["CurrentFlag"] == 1].copy()
    merged = df.merge(
        current_master,
        on='CustomerID',
        how = 'left',
        suffixes = ('_upd','_cur')
    )


    
    
    changed = merged[
        merged["Version"].notna() &
        (merged[f"{tracked_col}_upd"].fillna("") != merged[f"{tracked_col}_cur"].fillna(""))
    ].copy()

    # expire old current rows
    if not changed.empty:
        changed_ids = changed[key].unique()
        master.loc[(master[key].isin(changed_ids)) & (master["CurrentFlag"] == 1), "CurrentFlag"] = 0

        # insert new versions
        new_rows = df[df[key].isin(changed_ids)].copy()
        ver_map = changed.set_index(key)["Version"].astype(int).to_dict()
        new_rows["Version"] = new_rows[key].map(ver_map) + 1
        new_rows["CurrentFlag"] = 1

        # add missing master columns
        for col in master.columns:
            if col not in new_rows.columns:
                new_rows[col] = None

        master = pd.concat([master, new_rows[master.columns]], ignore_index=True)

    # insert brand new customers
    existing_ids = set(master[key].tolist())
    brand_new = df[~df[key].isin(existing_ids)].copy()
    if not brand_new.empty:
        brand_new["Version"] = 1
        brand_new["CurrentFlag"] = 1
        for col in master.columns:
            if col not in brand_new.columns:
                brand_new[col] = None
        master = pd.concat([master, brand_new[master.columns]], ignore_index=True)

    return master.sort_values([key, "Version"]).reset_index(drop=True)