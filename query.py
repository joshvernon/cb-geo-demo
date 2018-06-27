from couchbase.views.params import SpatialQuery

from cb_utils import connect

if __name__ == '__main__':
    lower_left = (-98.555659, 29.509246)
    upper_right = (-98.551410, 29.511178)
    bucket = connect()
    spatial_query = SpatialQuery(start_range=lower_left, end_range=upper_right)
    for row in bucket.query('main', 'stops', use_devmode=True, query=spatial_query):
        print(row.value)
        