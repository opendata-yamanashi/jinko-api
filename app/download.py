import requests

class Download:
    def __init__(self, url, dpath):
        self.url = url
        self.name = url.split("/")[-1]
        self.dpath = dpath / self.name

    def download(self):
        with open(self.dpath, "wb") as f:
            res = requests.get(self.url, allow_redirects=True)
            f.write(res.content)
