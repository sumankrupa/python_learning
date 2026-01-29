import pandas as pd
import numpy as np

def transform_data(customer_df,order_items_df,orders_data_df,products_data_df):

    # basic cleaning 
    customers = customer_df.copy()
    orders = orders_data_df.copy()
    items = order_items_df.copy()
    products = products_data_df.copy()

    # handle date
    orders['order_date'] = pd.to_datetime(orders['order_date'],errors='coerce')

    # handle number types
    items['quantity'] = pd.to_numeric(items['quantity'],errors='coerce').fillna(0).astype(int)
    items['price'] = pd.to_numeric(items['price'],errors='coerce').fillna(0.00).astype(float)

    # 1.Join Orders + Order Items
    line = items.merge(
        orders,
        how = 'inner',
        on = 'order_id',
        suffixes = ('_oi','_o')
        
        )
    

    # 2.Compute Line Total
    line['line_total'] = line['quantity'] * line['price']

    # 3. Filter Only Completed Orders

    line = line[line['status'] == 'COMPLETE'].copy() 

    # 4.Add Discount Column (Business Rule)

    line['net_total'] = np.where(line['quantity'] >= 5, line['line_total']*0.90,line['line_total'])


    # 5.Derive Order Month & Year (Date Transformation)
    line['order_month'] = pd.to_datetime(line['order_date']).dt.month
    line['order_year'] = pd.to_datetime(line['order_date']).dt.year


    # 7.Customer Region Join
    line = line.merge(
        customers[['customer_id','name','region']],
                  on = 'customer_id',
                  how = 'inner'
    )

    # 9.Category-wise Analysis (Enrichment)
    if products is not None:
        line = line.merge(
            products[['product_id','category','brand']],
            on = 'product_id',
            how = 'inner'
        )

    

    # 6.Aggregate at Order Level
    order_level = (
        line.groupby(
        ['order_id','customer_id','region','order_year','order_month'], dropna = False
        ).agg
        (
        order_total = ('line_total','sum'),
        net_order_total = ('net_total','sum'),
        line_count = ('order_item_id','count'),
        total_quantity = ('quantity','sum')
        ).reset_index()
    
    )
    # 8.Sales by Region + Month (Aggregation)

    region_month  = (
        order_level.groupby(['region','order_year','order_month'],dropna =False)
        .agg(
            total_revenue = ('net_order_total','sum'),
            order_count = ('order_id','nunique')
        ).reset_index()
    )

    # 10.Ranking Transformation
    region_totals = (
        region_month.groupby('region',dropna = False)['total_revenue'].sum().reset_index()
    )
    region_totals['region_rank'] = region_totals['total_revenue'].rank(ascending = False,method = 'dense').astype(int)

    # morege
    region_month = region_month.merge(
        region_totals[['region','region_rank']],
        on = 'region',
        how = 'inner'
    )
    # 11. sort by month 
    region_month = region_month.sort_values(['order_year','order_month','total_revenue'],ascending= [True,True,False])
    


    # 12.Outlier Flagging (Optional)
    quart_val = order_level['net_order_total'].quantile(0.95)
    order_level['is_outlier'] = order_level['net_order_total'] > quart_val




    print('transformation done')


    return line, order_level, region_month