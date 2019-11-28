import json
import requests
import argparse
import time

LOCATION = '21.013171,105.822266'
#radius = 2000
#keyword = "beer"

parser = argparse.ArgumentParser()
parser.add_argument("radius", help="bán kính", type=int)
parser.add_argument("keyword", help="từ khóa", type=str)
args = parser.parse_args()

session = requests.Session()


def api_key():
    with open("gg_api_key.txt", 'rt') as f:
        key = f.readline()
    return key


def places(radius, keyword):
    result = []
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json' #NOQA
    params = {
        "location": LOCATION,
        "radius": radius,
        "keyword": keyword,
        "key": api_key()
    }

    resp = session.get(url, params=params).json()
    result.extend(resp["results"])
    while "next_page_token" in resp:
        time.sleep(10)
        params.update({"pagetoken": resp["next_page_token"]})
        resp_next = session.get(url, params=params).json()
        result.extend(resp_next)
        if len(result) > 50:
            break
    print(f"have {len(result)} places")
    return result


def geojson_file(datas):
    geojson_map = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates":[float(data['geometry']['location']['lng']), float(data['geometry']['location']['lat'])]  # NOQA
                },
                "properties": {
                "Address": data['vicinity'],
                "name": data['name']
                }
            } for data in datas]}
    with open('pymi_beer.geojson', 'wt') as f:
        json.dump(geojson_map, f, ensure_ascii=False, indent=4)


def main():
    radius = args.radius
    keyword = args.keyword
    place = places(radius, keyword)
    map_geojson = geojson_file(place)


if __name__ == "__main__":
    main()
