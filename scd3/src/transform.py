import pandas as pd 


def transform_data(master,updated):
    if "PrevLoyaltyTier" not in master.columns:
        master["PrevLoyaltyTier"] = ""

    master["PrevLoyaltyTier"] = master["PrevLoyaltyTier"].astype(str)

    m = master.merge(
        updated[['CustomerID','LoyaltyTier']],
        on = 'CustomerID',
        how = 'left',
        suffixes = ('_cur','_upd')
        )
    
    mask = m['LoyaltyTier_upd'].notna() & (
        m['LoyaltyTier_upd'] != m['LoyaltyTier_cur']
    )

    master.loc[mask, "PrevLoyaltyTier"] = m.loc[mask, "LoyaltyTier_cur"]
    master.loc[mask, "LoyaltyTier"] = m.loc[mask, "LoyaltyTier_upd"]
    print('transform done')

    return master
