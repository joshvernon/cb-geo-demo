from couchbase.bucket import Bucket
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

from secrets3 import CB_USER, CB_PASSWORD

def connect(username=CB_USER, password=CB_PASSWORD):
    cluster = Cluster('couchbase://localhost')
    authenticator = PasswordAuthenticator(username, password)
    cluster.authenticate(authenticator)
    bucket = cluster.open_bucket('viastops')
    return bucket

def flush_bucket(bucket=connect()):
    if isinstance(bucket, Bucket):
        bucket.flush()
        print('Successfully flushed bucket {0}.'.format(bucket.bucket))