from jinko import Yamanashi_Jinko
from fastapi import FastAPI

yj = Yamanashi_Jinko()
yj.reboot_data()

app = FastAPI()

@app.get('/columns/')
def get_param():
    for i in yj.df["2022"]["1"].columns:
        yield i

@app.get('/cities/')
def get_city():
    for i in yj.df["2022"]["1"].index:
        yield i

@app.get('/format/')
def get_format(year=None, month=None):
    data = dict()
    if not year:
        data["year"] = list(yj.df.keys())
        year = "2022" # latest
    if (year) and (not month):
        month = "1" # latest
        data["month"] = list(yj.df[year].keys())

    data["city"] = list(yj.df[year][month].index)
    data["column"] = list(yj.df[year][month].columns)
    print(data)
    return [data]

@app.get('/data/')
def get_data(year = "latest", month = "latest", city = None):
    if year == "latest":
        year = "2022"
    if month == "latest":
        month = "1"
    
    return yj.df[year][month]