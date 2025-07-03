import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

BASE = 'https://fancaps.net'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_episode(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    thumbs = soup.select('a[href*="picture.php"] img')
    page_links = [urljoin(BASE, thumb.parent['href']) for thumb in thumbs]

    images = []
    for page in page_links:
        r2 = requests.get(page, headers=HEADERS)
        r2.raise_for_status()
        s2 = BeautifulSoup(r2.text, 'html.parser')
        img = s2.select_one('img[src*="/anime/"]')
        if img:
            images.append(urljoin(BASE, img['src']))

    for img_url in tqdm(images, desc=os.path.basename(output_folder)):
        fname = os.path.basename(img_url)
        path = os.path.join(output_folder, fname)
        if not os.path.exists(path):
            r = requests.get(img_url, headers=HEADERS, stream=True)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)

def batch_download(txt_file, base_output='downloads', max_workers=4):
    with open(txt_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for url in urls:
            folder = os.path.join(base_output, url.split('/')[-1])
            tasks.append(executor.submit(scrape_episode, url, folder))
        for _ in tqdm(tasks, desc='Total Episodes', unit='ep'):
            _.result()  # Wait for completion

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch download Fancaps episode images")
    parser.add_argument("txtfile", help="Text file with one episode URL per line")
    parser.add_argument("--out", default="downloads", help="Base output folder")
    parser.add_argument("--workers", type=int, default=4, help="Parallel threads")
    args = parser.parse_args()

    batch_download(args.txtfile, base_output=args.out, max_workers=args.workers)
