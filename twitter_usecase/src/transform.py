


import re
from html import unescape
import pandas as pd



def clean_text(text):
    if not text:
        return ""

    # remove html tags
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)

    # remvoe urls
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # remvoe @mention

    text = re.sub(r"@\w+", "", text)

    # remove special characters

    text = re.sub(r"[^\w\s#]", " ", text)

    return text


def transform_data(data):
    sol = []
    for d in data:
        sol.append({
            'id': d.get('id'),
            'created_at': d.get('created_at'),
            'text': clean_text(d.get('content')),
            'author_id': d.get("account", {}).get("id"),
            'repost_count': d.get('reblogs_count',0),
            'upvote_count': d.get('favourites_count',0),
        })

    
    df = pd.DataFrame(sol)
    df = df.drop_duplicates(subset=['id'])
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True).dt.tz_convert(None)


    print('transform done')
    return df