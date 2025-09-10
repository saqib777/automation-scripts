"""Download Images from URLs"""
import requests
import os

def download_images(urls, folder="downloads"):
    os.makedirs(folder, exist_ok=True)
    for i, url in enumerate(urls):
        response = requests.get(url)
        if response.status_code == 200:
            path = os.path.join(folder, f"image_{i}.jpg")
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {path}")

if __name__ == "__main__":
    sample_urls = ["https://picsum.photos/200/300"] * 3
    download_images(sample_urls)
