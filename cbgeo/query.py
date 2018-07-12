from couchbase.views.params import SpatialQuery

def query_bounding_box(bucket, lower_left, upper_right):
    spatial_query = SpatialQuery(start_range=lower_left, end_range=upper_right)
    view = bucket.query('main', 'stops', use_devmode=True, query=spatial_query)
    return view
