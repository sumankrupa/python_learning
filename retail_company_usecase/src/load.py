

import pandas as pd 

def load_data(line, order_level, region_month,engine):
    line.to_sql(
        name = 'sales_line',
        con = engine,
        if_exists ='replace',
        index = False
    )
    order_level.to_sql(
        name = 'sales_order',
        con = engine,
        if_exists ='replace',
        index = False
    )
    region_month.to_sql(
        name = 'sales_by_region_month',
        con = engine,
        if_exists ='replace',
        index = False
    )
    
    print('loading done')
    return 