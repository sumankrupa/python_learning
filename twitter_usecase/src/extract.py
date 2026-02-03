import requests


def extract_data():

    url = "https://mastodon.social/api/v1/timelines/tag/chess?limit=40"
    response = requests.get(url)
    if response.status_code == 200:
        print('extract done')
#   ['id', 'created_at', 'in_reply_to_id', 'in_reply_to_account_id', 'sensitive', 'spoiler_text', 'visibility', 'language', 'uri', 'url', 'replies_count', 'reblogs_count', 'favourites_count', 'quotes_count', 'edited_at', 'content', 'reblog', 'account', 'media_attachments', 'mentions', 'tags', 'emojis', 'quote', 'card', 'poll', 'quote_approval']

    return response.json()
