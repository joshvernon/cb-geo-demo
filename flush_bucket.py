from cb_utils import connect

if __name__ == '__main__':
    bucket = connect()
    bucket.flush()