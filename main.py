import json
import os
import urllib.request

PIC_NUM = 0

def return_data(url, api_key, continuation_url=None):
    if continuation_url is None:
        url = base_url + "me/photos"
    else:
        url = continuation_url

    request = urllib.request.Request(url)
    request.add_header('Authorization', 'Bearer {}'.format(api_key))

    response = urllib.request.urlopen(request)
    encoding = response.headers.get_content_charset()

    data = json.loads(response.read().decode(encoding))
    # NOTE: if you want more parsing, do it here!

    # wrap in try catch?
    print("Data keys: ", data.keys())
    paging = data['paging']
    print("Paging Keys: ", paging.keys())
    if 'next' in paging:
        next = paging['next']
    else:
        next=None

    return data, next

def parse_images(data, user_id, open_tagged_file):
    for data_object in data:
        picture_url = data_object['source']

        f = open('{}.jpg'.format(PIC_NUM), 'wb')
        f.write(urllib.request.urlopen(picture_url).read())
        f.close()

        PIC_NUM += 1
        picture_tags = data_object['tags']
        urllib.request.
        for tagee in picture_tags:
            if tagee == user_id:
                # This will give us access to the x, y coordinates of 
                # the tagged face!
                pass
if __name__ == '__main__':
    base_url = "https://graph.facebook.com/v2.3/"

    #super secret api password thingy!
    facebook_api_key = os.getenv('FACEBOOK_API_KEY')
    data, next = return_data(base_url+"me", facebook_api_key)

    # Will need id for parsing photo tags
    user_id = data['id']

    data, next = return_data(base_url+"me/photos", facebook_api_key)
    data = data['data']
    print(len(data))
    condition = True

    while(condition):
        data, next = return_data(base_url, facebook_api_key, next)
        data = data['data']


        print(len(data))
        if next is None:
            condition=False

    print("Done!")

