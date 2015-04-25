import json
import os
import urllib.request
base_url = "https://graph.facebook.com/v2.3"

#super secret api password thingy!
facebook_api_key = os.getenv('FACEBOOK_API_KEY')

data, next = return_data(facebook_api_key)
condition = True

while(condition):
    data, next = return_data(facebook_api_key, next)
    print(len(data))

def return_data(api_key, continuation_url=None):
    if continuation_url is None:
        url = base_url + "/me/photos"
    else:
        url = base_url + continuation_url

    request = urllib.request.Request(url)
    request.add_header('Authorization', 'Bearer {}'.format(api_key))

    response = urllib.request.urlopen(request)
    encoding = response.headers.get_content_charset()

    data = json.loads(response.read().decode(encoding))
    # NOTE: if you want more parsing, do it here!

    # wrap in try catch?
    next = data['paging']['next']
    data = data['data']
    return data, next
