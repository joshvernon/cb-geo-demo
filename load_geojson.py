import requests

GEOJSON_URL = 'https://opendata.arcgis.com/datasets/02f9703331e2486b84c02f7a1988bf26_0.geojson'

def download_features(url=GEOJSON_URL):
    response = requests.get(url)
    if response.status_code == 200:
        feature_collection = response.json()
        features = feature_collection['features']
        print(len(features))
        return features
    else:
        response.raise_for_status()

if __name__ == '__main__':
    download_features()