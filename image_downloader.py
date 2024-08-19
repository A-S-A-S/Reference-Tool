import os
import requests
import json
from bs4 import BeautifulSoup
import customtkinter as ctk

class ImageDownloader(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # URL
        self.url_label = ctk.CTkLabel(self, text="Enter Pinterest board URI here:")
        self.url_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter URL here")
        self.url_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")
        #self.url_entry.insert(0, "https://pt.pinterest.com/avgustcunningham/scenery/")

        # Folder
        self.folder_label = ctk.CTkLabel(self, text="Folder to download:")
        self.folder_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.folder_entry = ctk.CTkEntry(self, placeholder_text="Enter folder name")
        self.folder_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.folder_entry.insert(0, "images")

        # Max Images
        self.max_images_label = ctk.CTkLabel(self, text="Max Images:")
        self.max_images_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.max_images_entry = ctk.CTkEntry(self, placeholder_text="Max images")
        self.max_images_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        self.max_images_entry.insert(0, "10")

        # Download
        download_button = ctk.CTkButton(self, text="Download Images", command=self.start_download)
        download_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Column weight for proportional Sizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def start_download(self):
        url = self.url_entry.get()
        folder = self.folder_entry.get()
        try:
            max_images = int(self.max_images_entry.get())
        except ValueError:
            print("Invalid number of images. Please enter a valid integer.")
            return

        json_data_list = self.get_source(url)
        image_urls = self.save_image_url(json_data_list, max_images)
        self.download_images(image_urls, folder)

    def get_source(self, url: str):
        json_data_list = []
        try:
            res = requests.get(url)
            res.raise_for_status()  # Ensure we handle HTTP errors
        except Exception as e:
            print(f"Error fetching the URL: {e}")
            return json_data_list

        html = BeautifulSoup(res.text, 'html.parser')
        json_data = html.find_all("script", attrs={"id": "__PWS_INITIAL_PROPS__"})
        if not json_data:
            json_data = html.find_all("script", attrs={"id": "__PWS_DATA__"})

        if json_data:
            json_data_list.append(json.loads(json_data[0].string))
        else:
            json_data_list.append({})

        print(f'json_data_list: {json_data_list}')
        return json_data_list

    def save_image_url(self, json_data_list, max_images: int) -> list:
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

    def download_images(self, url_list, folder):
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
