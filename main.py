import json
import os
import base64
import urllib.request

url = "https://graph.facebook.com/v2.3/me/photos"
#super secret api password thingy!
facebook_api_key = os.getenv('FACEBOOK_API_KEY')
base64string = base64.encodestring

request = urllib.request.Request(url)
request.add_header('Authorization', 'Bearer {}'.format(facebook_api_key))

response = urllib.request.urlopen(request)
encoding = response.headers.get_content_charset()
# if we don't get anything, assume 'utf-8'
if encoding is None:
    print('encoding none!')
    encoding = 'utf-8'

data = json.loads(response.read().decode(encoding))
print(data)
