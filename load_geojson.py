from datetime import datetime

import requests

import cb_utils

GEOJSON_URL = 'https://opendata.arcgis.com/datasets/02f9703331e2486b84c02f7a1988bf26_0.geojson'

def get_features(url=GEOJSON_URL):
    response = requests.get(url)
    if response.status_code == 200:
        feature_collection = response.json()
        features = feature_collection['features']
        return features
    else:
        response.raise_for_status()

def upsert_features_sequential(bucket, features):
    for feature in features:
        # Get the value of the STOP_ID field,
        # which we'll use as the document key.
        document_id = feature['properties']['STOP_ID']
        feature['properties']['modified'] = int(datetime.now().timestamp()) * 1000
        # feature['modified'] = int(datetime.now().timestamp()) * 1000
        # props_to_remove = ('properties', 'type')
        # list(map(feature.pop, props_to_remove))
        result = bucket.upsert(document_id, feature)
        if not result.success:
            print('Failed to upsert feature {0}'.format(document_id))

if __name__ == '__main__':
    features = get_features()
    bucket = cb_utils.connect()
    upsert_features_sequential(bucket, features)
    