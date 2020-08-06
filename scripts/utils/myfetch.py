from io import BytesIO
import requests
from tqdm import tqdm
from pathlib import Path

def download(url):
    """
    easy downloading function: provides progress bar
    https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
    """
    resp = requests.get(url, stream=True)
    if resp.status_code != 200:
        # be noisy and alert the user that the download unexpectedly failed
        raise ValueError(f"Got status code {resp.status_code} for: {url}")

    content_length = int(resp.headers.get('content-length', 0))
    blocksize = 1024
    progress_bar = tqdm(total=content_length, unit='iB', unit_scale=True)

    for datablock in resp.iter_content(blocksize):
        progress_bar.update(len(datablock))
        yield datablock
    progress_bar.close()


def existed_size(path):
    """
    if path exists and is a file, returns file size in bytes
    else, returns False
    """
    e = Path(path)
    if e.is_file():
        return e.stat().st_size
    else:
        return False


def fetch_content(url):
    """simple wrapper around download that returns a big bytes object"""
    bx = BytesIO()
    for content in download(url):
        bx.write(content)

    allbytes = bx.getvalue()
    bx.close()
    return allbytes



