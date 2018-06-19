import timeit

def run_timeit(function_name, repeat_count=5):
    if function_name not in ('upsert_features_sequential'):
        return

    # Setup the code to run.
    setup_code = "from load_geojson import get_features, {0};"\
    "from cb_utils import connect;"\
    "features = get_features();"\
    "bucket = connect()".format(function_name)
    stmt_code = "{0}(bucket, features)".format(function_name)

    # Run timeit.
    print('Running timeit. Hang tight...')
    results = timeit.repeat(
        stmt=stmt_code,
        setup=setup_code,
        repeat=repeat_count,
        number=1
    )

    # Print the results.
    print('Function: {0}'.format(function_name))
    for i, result in enumerate(results, 1):
        print('Trial {0:d}: {1:.3f} s'.format(i, result))

if __name__ == '__main__':
    run_timeit('upsert_features_sequential')
    