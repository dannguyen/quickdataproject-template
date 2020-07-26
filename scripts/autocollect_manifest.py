#!/usr/bin/env python

"""
autocollect_manifest.py

Reads data/MANIFEST.yaml, and for each entry where autocollect==true, downloads from the
  corresponding `url`

"""
from pathlib import Path
import requests
from sys import stderr
import yaml


MANIFEST_PATH = Path('./data/MANIFEST.yaml')

def collect_manifest():
    """
    returns list of tuples, with file filepath and source url

    filtered for data/collected prefixes
    """
    mani = yaml.load(MANIFEST_PATH.open(), Loader=yaml.BaseLoader)
    return [(filepath, v['url']) for filepath, v in mani.items() if v['autocollect'] == 'true']


def fetch_file(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        # be noisy and alert the user that the download unexpectedly failed
        raise ValueError(f"Got status code {resp.status_code} for: {url}")
    return resp.content



def main():
    dest_dir = MANIFEST_PATH.parent

    for filename, url in collect_manifest():
        stderr.write("\n")
        stderr.write(f"Downloading: {url}\n")

        content = fetch_file(url)

        dest_path = dest_dir.joinpath(filename)
        dest_path.parent.mkdir(exist_ok=True, parents=True)
        dest_path.write_bytes(content)

        stderr.write(f"\tWrote {len(content)} bytes to: {dest_path}\n")


if __name__ == '__main__':
    main()
