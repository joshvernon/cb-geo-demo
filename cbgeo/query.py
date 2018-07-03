from couchbase.views.params import SpatialQuery

from utils import connect
        
def query_bounding_box(bucket, lower_left, upper_right):
    spatial_query = SpatialQuery(start_range=lower_left, end_range=upper_right)
    view = bucket.query('main', 'stops', use_devmode=True, query=spatial_query)
    raw_result = [(row.geometry, row.value) for row in view]
    return raw_result

if __name__ == '__main__':
    lower_left = (-98.555659, 29.509246)
    upper_right = (-98.551410, 29.511178)
    bucket = connect()
    raw_result = query_bounding_box(bucket, lower_left, upper_right)
    print(raw_result)
