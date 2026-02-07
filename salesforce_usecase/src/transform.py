import pandas as pd 
from decimal import Decimal




def transform_data(data):
    df = pd.DataFrame(data)

    print('transform done')
    return df