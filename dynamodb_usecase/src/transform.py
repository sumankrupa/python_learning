import pandas as pd 
from decimal import Decimal


def convert_types(obj):
    if isinstance(obj, list):
        return [convert_types(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj



def transform(records):
    clean_records = [convert_types(r) for r in records]
    df = pd.DataFrame(clean_records)
    print(df)
    print('transform done')
    return df