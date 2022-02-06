# 山梨人口推移データ API
市町村別の世帯数、男女別人口、自然増減・社会増減

## 出典:
* [山梨の人口](https://www.pref.yamanashi.jp/toukei_2/HP/y_pop.html)

## API 仕様
(後で書く)

## ライセンス
本ソフトウェアは、[MITライセンス](https://github.com/opendata-yamanashi/onsen-api/blob/main/LICENSE.txt)の元提供されています。

## Installation

* how to setup  
```
$ git clone https://github.com/opendata-yamanashi/jinko-api
$ pip install -r requirements.txt
```
* access my application!
```
$ uvicorn app.main:app --reload 
$ curl http://localhost:8000/
```

done
