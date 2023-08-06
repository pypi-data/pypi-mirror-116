# from https://gist.github.com/yashbonde/62df9d16858a43775c22a6af00a8d707

import os
import io
import logging
from PIL import Image

logging.basicConfig(level="INFO")
def info(x, *args):
  # because logging.info requires formatted strings
  x = repr(x)
  x = " ".join([x] + [repr(y) for y in args])
  logging.info(x)

def fetch(url):
    # efficient loading of URLS
    import os, tempfile, hashlib, requests
    fp = os.path.join(tempfile.gettempdir(), hashlib.md5(url.encode("utf-8")).hexdigest())
    if os.path.isfile(fp) and os.stat(fp).st_size > 0:
        with open(fp, "rb") as f:
            dat = f.read()
    else:
        dat = requests.get(url).content
        with open(fp + ".tmp", "wb") as f:
            f.write(dat)
        os.rename(fp + ".tmp", fp)
    return dat

def get_image(file_path_or_url):
    if os.path.exists(file_path_or_url):
        return Image.open(file_path_or_url)
    else:
        return Image.open(io.BytesIO(fetch(file_path_or_url)))

def folder(x):
    # get the folder of this file path
    import os
    return os.path.split(os.path.abspath(x))[0]


def is_available(package: str):
    import importlib
    spam_spec = importlib.util.find_spec(package)
    return spam_spec is not None
