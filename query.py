from couchbase.views.params import SpatialQuery

from cb_utils import connect
        
def query_bounding_box(bucket, lower_left, upper_right):
    spatial_query = SpatialQuery(start_range=lower_left, end_range=upper_right)
    view = bucket.query('main', 'stops', use_devmode=True, query=spatial_query)
    for counter, row in enumerate(view, 1):
        print(row.value['LOCATION'])
    print('Processed {0:d} rows.'.format(counter))

if __name__ == '__main__':
    lower_left = (-98.555659, 29.509246)
    upper_right = (-98.551410, 29.511178)
    bucket = connect()
    query_bounding_box(bucket, lower_left, upper_right)
