import timeit

BASE_SETUP_CODE = "from cbgeo.utils import connect;bucket = connect()"
UFS_SETUP_CODE = "from cbgeo.loader import get_features,"\
"upsert_features;{0};features = get_features()".format(BASE_SETUP_CODE)
QBB_SETUP_CODE = "from cbgeo.query import query_bounding_box;{0}".format(BASE_SETUP_CODE)

FUNCTION_CONFIGS = {
    'upsert_features': UFS_SETUP_CODE,
    'query_bounding_box': QBB_SETUP_CODE,
}

def run_timeit(function_name, repeat_count, *args,):
    if function_name not in FUNCTION_CONFIGS.keys():
        return

    # Setup the code to run.
    setup_code = FUNCTION_CONFIGS[function_name]
    stmt_code = "{0}({1})".format(function_name, ', '.join(args))

    # Run timeit.
    print('Running timeit. Hang tight...\nsetup_code: {0}\n'\
          'stmt_code: {1}'.format(setup_code, stmt_code))
    results = timeit.repeat(
        stmt=stmt_code,
        setup=setup_code,
        repeat=repeat_count,
        number=1
    )

    # Print the results.
    for i, result in enumerate(results, 1):
        print('Trial {0:d}: {1:.7f} s'.format(i, result))

if __name__ == '__main__':
    run_timeit('upsert_features', 5, 'bucket', 'features')

    # Bounding box query where bounding box has relatively small area.
    run_timeit('query_bounding_box', 5, 'bucket',
               '(-98.555659, 29.509246)', '(-98.551410, 29.511178)')
    
    # Bounding box has a larger area
    run_timeit('query_bounding_box', 5, 'bucket',
               '(-98.571223, 29.370413)', '(-98.386344, 29.545823)')
