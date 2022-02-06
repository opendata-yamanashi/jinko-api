from pathlib import Path
import requests
from urllib.parse import urljoin
from jeraconv import jeraconv
import re
import neologdn
from download import Download
from bs4 import BeautifulSoup
import pandas as pd
import xlrd
import json

PAGE_URL = "https://www.pref.yamanashi.jp/toukei_2/HP/y_pop.html"

j2w = jeraconv.J2W()

headers = [
    "市町村名",
    "人口 総数",
    "人口 男",
    "人口 女",
    "前月比",
    "自然増減",
    "自然増減 出生",
    "自然増減 死亡",
    "社会増減",
    "社会増減 転入計",
    "社会増減 転入県内",
    "社会増減 転入県外",
    "社会増減 転入国外",
    "社会増減 その他",
    "社会増減 転出計",
    "社会増減 転出県内",
    "社会増減 転出県外",
    "社会増減 転出国外",
    "社会増減 転出その他",
    "前月人口",
]

class Yamanashi_Jinko:
    BASE_DIR = Path(__file__).absolute().parent.parent
    DATA_DIR = BASE_DIR / "data"
    struct_json = BASE_DIR / "info.json"

    def __init__(self):
        if not self.struct_json.exists():
            with open(self.struct_json, "w") as f:
                json.dump(dict(), f)

        if not self.DATA_DIR.exists():
            self.DATA_DIR.mkdir()
            self.setup_data()

    def get_years(self, year=None):
        data = dict()
        res = requests.get(PAGE_URL)
        soup = BeautifulSoup(res.content)
        for i in soup.find_all("li"):
            if re.search('.+年', i.text):
                seireki = j2w.convert(re.search('.+年', i.text)[0])
            data[str(seireki)] = urljoin(res.url, i.a.get("href"))
        if year:
            return data[year]
        self.urllist = data

    def get_data(self, year, url):
        d = Download(url, self.DATA_DIR)
        d.download()

        with open(self.struct_json, "r") as f:
            st = json.load(f)
        
        st[year] = d.name
        with open(self.struct_json, "w") as f:
            json.dump(st, f, indent=4)
        return d.name

    def get_filename(self, year=None):
        with open(self.struct_json, "r") as f:
            st = json.load(f)
        if year:
            return st[year]
        else:
            return st

    def _get_excel_info(self, fname):
        #self.sheet_names = list()
        wb = xlrd.open_workbook_xls(self.DATA_DIR / fname)
        for i in wb.sheet_names():
            if wb.sheet_by_name(i).ncols <= 10:
                continue
            if re.search("^外?[1-9][0-2]?", neologdn.normalize(i)):
                yield i

    def _create_dataframe(self, fname="", sheet_name=None):
        fpath = self.DATA_DIR / fname 
        df = pd.read_excel(fpath, sheet_name=sheet_name, header=10,nrows=100,usecols="A:T")
        df = df.dropna()
        df.columns = headers
        df = df.set_index("市町村名")
        return df

    def setup_data(self):
        self.get_years()
        self.df = dict()
        for year, url in self.urllist.items():
            fname = self.get_data(year, url)
            self.df.setdefault(year, dict())
            for sname in self._get_excel_info(fname):
                self.df[year][neologdn.normalize(sname)] = self._create_dataframe(fname, sname)

    def reboot_data(self):
        self.df = dict()
        #self.get_filename()
        for year, fname in self.get_filename().items():
            self.df.setdefault(year, dict())
            for sname in self._get_excel_info(fname):
                self.df[year][neologdn.normalize(sname)] = self._create_dataframe(fname, sname)
