#!/usr/bin/env python

"""
autocollect_manifest.py

Reads data/MANIFEST.yaml, and for each entry where autocollect==true, downloads from the
  corresponding `url`

"""
from sys import path as syspath; syspath.append('./scripts')
from utils.myfetch import download, existed_size
from utils.mylog import mylog

from pathlib import Path
import requests
import yaml


MANIFEST_PATH = Path('./data/DATA_MANIFEST.yaml')

def collect_manifest():
    """
    returns list of tuples, with file filepath and source url

    filtered for data/collected prefixes
    """
    mani = yaml.load(MANIFEST_PATH.open(), Loader=yaml.BaseLoader)
    return [(filepath, v['url']) for filepath, v in mani.items() if v.get('autocollect') == 'true']



def main():
    target_dir = MANIFEST_PATH.parent

    for filename, url in collect_manifest():
        target_path = target_dir.joinpath(filename)

        _bx = existed_size(target_path)
        if _bx:
            mylog(f"{target_path} already exists, with {_bx} bytes", label='Skipping')
        else:
            mylog(url, label='Fetching')
            content = download(url)
            target_path.parent.mkdir(exist_ok=True, parents=True)
            with open(target_path, 'wb') as target:
                for cx in content:
                    target.write(cx)

            mylog(f"{existed_size(target_path)} bytes to {target_path}", label='Wrote')


if __name__ == '__main__':
    main()
