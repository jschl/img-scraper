# img_scraper

Application for scraping images from google.

## Prerequirements

- download system specific version of [geckodriver](https://github.com/mozilla/geckodriver/releases)
- go to repository root and extract geckodriver

## Usage

- fill `cats.txt` with categories (new line per category)
- run `get_images.py` from terminal

> ```python get_images.py -c cats.txt -l 10 -e path_to_exportfolder --headless True```