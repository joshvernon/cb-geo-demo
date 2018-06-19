from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

from secrets3 import CB_USER, CB_PASSWORD

def connect(username=CB_USER, password=CB_PASSWORD):
    cluster = Cluster('couchbase://localhost')
    authenticator = PasswordAuthenticator(CB_USER, CB_PASSWORD)
    cluster.authenticate(authenticator)
    bucket = cluster.open_bucket('viastops')
    return bucket
