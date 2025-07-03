# Fancaps Episode Image Scraper

A Python script to scrape and download full-resolution anime episode images from [Fancaps.net](https://fancaps.net). Supports both single-episode scraping and batch downloading using a `.txt` file.

## Features

- ✅ Scrape full-resolution images from `episodeimages.php` links  
- ✅ Auto-download all images into organized folders  
- ✅ Batch download support via `.txt` file  
- ✅ Multithreading for faster scraping  
- ✅ Auto-skip existing files  

## Requirements

Install Python packages before running:

```
pip install requests beautifulsoup4 tqdm
```

## Folder Structure

```
.
├── scraper.py
├── urls.txt         # optional - list of episode URLs for batch mode
├── downloads/       # images will be saved here
│   ├── Episode_01/
│   ├── Episode_02/
│   └── ...
```

## Usage

### 1. Scrape a Single Episode
You can modify `scraper.py` to call `scrape_episode()` manually:
```python
scrape_episode("https://fancaps.net/anime/episodeimages.php?12345-Series_Name/Episode_11", "downloads/Episode_11")
```

### 2. Batch Download from Text File

Create `urls.txt` with one URL per line:
```
https://fancaps.net/anime/episodeimages.php?12345-Series_Name/Episode_11
https://fancaps.net/anime/episodeimages.php?12345-Series_Name/Episode_12
```

Run the script:
```
python scraper.py urls.txt --out downloads --workers 6
```

**Arguments:**
- `urls.txt` — Text file with one episode URL per line  
- `--out` — Base output folder (default: `downloads`)  
- `--workers` — Number of threads for batch scraping (default: 4)  

## Notes

- The script navigates from the episode page to individual `picture.php` pages, then extracts the full-size image.
- Images are stored under folders named after the episode (e.g., `Episode_11`).
- Make sure you have a stable connection—no resume support yet.

## TODO

- [ ] Add retry logic on failure  
- [ ] CLI support for scraping by range (Episode 1–12)  
- [ ] ZIP/compress downloaded folders (optional)  
- [ ] Proxy and rate-limit handling  
- [ ] GUI version  

## Credits

Inspired by requests from the anime community to automate screenshot extraction for research, review, and fan use.

Made with ❤️ in Python.
