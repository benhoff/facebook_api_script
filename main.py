import json
import os
import urllib.request

PIC_NUM = 0

def return_data(url, api_key):
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'Bearer {}'.format(api_key))

    response = urllib.request.urlopen(request)
    encoding = response.headers.get_content_charset()

    data = json.loads(response.read().decode(encoding))
    
    return data 

def parse_images(data, user_id, open_tagged_file):
    for data_object in data:
        picture_url = data_object['source']

        f = open('{}.jpg'.format(PIC_NUM), 'wb')
        f.write(urllib.request.urlopen(picture_url).read())
        f.close()

        PIC_NUM += 1
        picture_tags = data_object['tags']
        # NOTE: Start here
        #urllib.request.
        for tagee in picture_tags:
            if tagee == user_id:
                # This will give us access to the x, y coordinates of 
                # the tagged face!
                pass

def get_next_from_data(data):
    if 'paging' in data:
        paging = data['paging']
        if 'next' in paging:
            return paging['next']
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    base_url = "https://graph.facebook.com/v2.3/"

    #super secret api password thingy!
    facebook_api_key = os.getenv('FACEBOOK_API_KEY')

    data = return_data(base_url+"me", facebook_api_key)

    # Will need id for parsing photo tags
    user_id = data['id']

    data = return_data(base_url+"me/photos", facebook_api_key)

    next_ = get_next_from_data(data)

    data = data['data']
    print(len(data))

    if next_ is None:
        more_photos = False
    else:
        more_photos = True 

    while(more_photos):
        data = return_data(next_, facebook_api_key)
        next_ = get_next_from_data(data)

        data = data['data']


        print(len(data))
        if next_ is None:
            more_photos=False

    print("Done!")
