import pandas as pd 


def transform_data(master,updated):
    merged = updated[['CustomerID','SubscriptionStart','SubscriptionEnd']].merge(
        master[['CustomerID','SubscriptionStart','SubscriptionEnd']],
        on = 'CustomerID',
        how = 'left',
        suffixes = ('_upd','_mst')
    )

    start_upd = merged['SubscriptionStart_upd'].fillna(pd.Timestamp('1900-01-01'))
    start_mst = merged['SubscriptionStart_mst'].fillna(pd.Timestamp('1900-01-01'))
    end_upd = merged['SubscriptionEnd_upd'].fillna(pd.Timestamp('2100-01-01'))
    end_mst = merged['SubscriptionEnd_mst'].fillna(pd.Timestamp('2100-01-01'))

    changed = (
        merged['SubscriptionStart_mst'].isna()| #if master record is missing it means new customer
        (start_upd != start_mst)| # start changed?
        (end_upd != end_mst) #end changed?
    )
    # scd4 table 
    history_df = merged.loc[changed,[
        'CustomerID',
        'SubscriptionStart_upd',
        'SubscriptionEnd_upd'

    ]]
    history_df.columns  = [['CustomerID',
        'SubscritptionStart',
        'SubscriptionEnd']]
    history_df['timestamp'] = pd.Timestamp.now()

    master_new = master.set_index('CustomerID')
    upd_idx = updated.set_index('CustomerID')
    master_new.update(upd_idx[['SubscriptionStart','SubscriptionEnd']])
    master_new = master_new.reset_index()
    print('transformation done')

    
    return master_new,history_df
