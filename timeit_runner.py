import timeit

BASE_SETUP_CODE = "from cb_utils import connect;bucket = connect()"
UFS_SETUP_CODE = "from load_geojson import get_features,"\
"upsert_features_sequential;{0};features = get_features()".format(BASE_SETUP_CODE)

FUNCTION_CONFIGS = {
    'upsert_features_sequential': UFS_SETUP_CODE
}

def run_timeit(function_name, repeat_count, *args,):
    if function_name not in FUNCTION_CONFIGS.keys():
        return

    # Setup the code to run.
    setup_code = FUNCTION_CONFIGS[function_name]
    stmt_code = "{0}({1})".format(function_name, ', '.join(args))

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
    run_timeit('upsert_features_sequential', 5, 'bucket', 'features')
    