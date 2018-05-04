import requests
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

from secrets3 import CB_USER, CB_PASSWORD

GEOJSON_URL = 'https://opendata.arcgis.com/datasets/02f9703331e2486b84c02f7a1988bf26_0.geojson'

def get_features(url=GEOJSON_URL):
    response = requests.get(url)
    if response.status_code == 200:
        feature_collection = response.json()
        features = feature_collection['features']
        return features
    else:
        response.raise_for_status()

def upsert_features(bucket, features):
    for feature in features:
        # Get the value of the STOP_ID field,
        # which we'll use as the document key.
        document_id = feature['properties']['STOP_ID']
        result = bucket.upsert(document_id, feature)
        if not result.success:
            print('Failed to upsert feature {0}'.format(document_id))


if __name__ == '__main__':
    features = get_features()
    cluster = Cluster('couchbase://localhost')
    authenticator = PasswordAuthenticator(CB_USER, CB_PASSWORD)
    cluster.authenticate(authenticator)
    bucket = cluster.open_bucket('viastops')
    upsert_features(bucket, features)
    