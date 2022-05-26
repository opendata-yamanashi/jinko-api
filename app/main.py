from jinko import Yamanashi_Jinko
from fastapi import FastAPI
from datetime import datetime 

yj = Yamanashi_Jinko()
yj.reboot_data()

app = FastAPI()

@app.get('/')
def hello():
    return "Hello! Please access /docs"

@app.get('/dtypes/')
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
    data["dtype"] = list(yj.df[year][month].columns)
    return [data]

@app.get('/data/')
def get_data(year = "latest", month = "latest", city = None, dtype = None):
    now = datetime.now()
    if year == "latest":
        year = str(now.year)
    if month == "latest":
        month = str(now.month - 1)
    if (not city) and (not dtype):
        return yj.df[year][month].T
    elif city and (not dtype):
        if not city in yj.df[year][month].index:
            return {"error": "no city data"}
        for key,value in yj.df[year][month].T.iteritems():
            # print(city, key, city==key)
            if key == city:
                return {key: value}
    elif (not city) and dtype:
        fff = dict()
        for key, value in yj.df[year][month].T.iteritems():
            fff[key] = {dtype: value[dtype]}
        return fff
    else:
        for key, value in yj.df[year][month].T.iteritems():
            if key == city:
                return {city: {dtype: value[dtype]}}
