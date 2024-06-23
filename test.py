import os
import requests
import json
from bs4 import BeautifulSoup

def get_source(url: str):
    json_data_list = []
    try:
        res = requests.get(url)
        res.raise_for_status() # Ensure we handle HTTP errors
    except Exception as e:
        print(f"Error fetching the URL: {e}")
        return json_data_list

    html = BeautifulSoup(res.text, 'html.parser')
    json_data = html.find_all("script", attrs={"id": "__PWS_INITIAL_PROPS__"})
    if not len(json_data):
        json_data = html.find_all("script", attrs={"id": "__PWS_DATA__"})

    if len(json_data):
        json_data_list.append(json.loads(json_data[0].string))
    else:
        json_data_list.append({})

    print(f'json_data_list: {json_data_list}')
    return json_data_list

def save_image_url(json_data_list, max_images: int) -> list:
    url_list = []
    for js in json_data_list:
        try:
            if 'initialReduxState' in js:
                pins = js['initialReduxState'].get('pins', {})
            elif 'props' in js and 'initialReduxState' in js['props']:
                pins = js['props']['initialReduxState'].get('pins', {})
            else:
                continue

            urls = []
            for pin in pins.values():
                images = pin.get('images', {})
                orig_images = images.get('orig')
                if isinstance(orig_images, list):
                    for img in orig_images:
                        urls.append(img.get('url'))
                elif orig_images:
                    urls.append(orig_images.get('url'))

            for url in urls:
                url_list.append(url)
                if max_images is not None and max_images == len(url_list):
                    return list(set(url_list))
        except Exception as e:
            print(f"Error processing JSON data: {e}")
            continue

    return list(set(url_list))

def download_images(url_list, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for idx, url in enumerate(url_list):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                with open(os.path.join(folder, f'image_{idx + 1}.jpg'), 'wb') as file:
                    file.write(response.content)
                print(f'Downloaded image_{idx + 1}.jpg')
            else:
                print(f"Failed to download {url}")
        except Exception as e:
            print(f"Error downloading image {url}: {e}")

# Usage
url = "https://pt.pinterest.com/avgustcunningham/scenery/"
folder = "pntrst"
max_images = 10 # Set your desired number of images to download

json_data_list = get_source(url)
image_urls = save_image_url(json_data_list, max_images)
download_images(image_urls, folder)