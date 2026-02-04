import pandas as pd 
from decimal import Decimal




def transform(mails):
    df = pd.DataFrame(mails)
    print('transform done')
    return df