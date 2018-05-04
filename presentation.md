# Working with geodata in Couchbase - ~~GeoRodeo 2018 lightning talk~~

## Install and configure couchbase in a docker container
1. Follow the relevant instructions to install and run [docker](https://docs.docker.com/install) for your operating system.
2. Follow the instructions on the [Do a Quick Install](https://developer.couchbase.com/documentation/server/current/getting-started/do-a-quick-install.html) page to pull down and initialize the couchbase/sandbox:5.0.0-beta docker container.
3. Optional: Complete the rest of the tutorial in the [Getting Started](https://developer.couchbase.com/documentation/server/current/getting-started/start-here.html) section of the couchbase docs to get a very basic familiarity with couchbase and N1QL.

## Set up the couchbase Python SDK
### Install prerequisite packages
The below [instructions](https://developer.couchbase.com/documentation/server/current/sdk/python/start-using-sdk.html) were completed on Fedora 27 and will vary by OS.
```
$ sudo dnf install python2-devel python3-devel libcouchbase-devel libcouchbase-tools
```
For Linux the header (*-devel) packages are needed to properly build the Python SDK.
### Get the Python code and set up the virtualenv with the Python SDK.
If the prerequisite packages aren't present you'll likely see an error here when pip tries to build the couchbase SDK.
```shell
$ git clone https://github.com/joshvernon/cb-geo-demo.git
Cloning into 'cb-geo-demo'...
remote: Counting objects: 30, done.
remote: Compressing objects: 100% (23/23), done.
remote: Total 30 (delta 10), reused 22 (delta 6), pack-reused 0
Receiving objects: 100% (30/30), 8.11 KiB | 8.11 MiB/s, done.
Resolving deltas: 100% (10/10), done.
$ cd cb-geo-demo/
$ pipenv install
Installing dependencies from Pipfile.lock (c60920)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 6/6 — 00:00:01
To activate this project's virtualenv, run the following:
 $ pipenv shell
 ```
 ### Verify the SDK is working correctly
 ```
$ pipenv run python -c "import couchbase; print(couchbase.__version__)"
2.3.5
```

## Download and explore the [sample GeoJSON dataset](https://hub.arcgis.com/datasets/VIATransit::via-bus-stops-2018)
```
$ curl -s https://opendata.arcgis.com/datasets/02f9703331e2486b84c02f7a1988bf26_0.geojson | python -m json.tool > via_stops_2018.geojson
```
```json
{
    "features": [
        {
            "geometry": {
                "coordinates": [
                    -98.51548460103818,
                    29.58578131134629
                ],
                "type": "Point"
            },
            "properties": {
                "FID": 1,
                "FREQUENT": " ",
                "LOCATION": "BLANCO OPPOSITE DEER CREST",
                "OBJECTID": 1,
                "ROUTES": "002",
                "STOP_ID": "33646"
            },
            "type": "Feature"
        },
        {
            "geometry": {
                "coordinates": [
                    -98.51287801739547,
                    29.55217295061742
                ],
                "type": "Point"
            },
            "properties": {
                "FID": 2,
                "FREQUENT": " ",
                "LOCATION": "BLANCO & SIR WINSTON CHURCHILL",
                "OBJECTID": 2,
                "ROUTES": "002",
                "STOP_ID": "93376"
            },
            "type": "Feature"
        },
        ...
    ],
    "type": "FeatureCollection"
}
```

## Set up the viastops couchbase bucket to hold the geojson features
1. Hit http://localhost:8091 in a browser, and login to the couchbase console.
2. Click buckets on the left hand side of the page.
![Couchbase console dashboard page with Buckets menu item circled](/images/dashboard.png)
3. Click "ADD BUCKET" near the top right of the screen.
![Couchbase console Buckets page with ADD BUCKET link circled](/images/add-bucket.png)
4. In the Add Data Bucket dialog, enter viastops for the bucket Name. You can leave the default bucket memory quota of 200 MB and the Bucket Type of couchbase. You can leave the Advanced settings as-is, or change them to your liking. Click the "Add Bucket" button.

![Couchbase console Add Data Bucket dialog with "viastops" entered in the Name field and and memory quota of 200 MB and bucket type of Couchbase](/images/add-bucket-dialog.png)

5. You should now see the new (empty) viastops bucket.
![Buckets page after adding new bucket showing empty viastops bucket](/images/new-bucket.png)

## Load the geojson features into the viastops bucket
We'll use the [load_geojson.py](/load_geojson.py) script to download the VIA stops geojson FeatureCollection (again), parse the FeatureCollection object into individual features, and load each feature as a document into the `viastops` couchbase bucket. We are going to use each stop's `STOP_ID` value as its document key. 

**IMPORTANT NOTE**: You'll need to change the `CB_USER` and `CB_PASSWORD` constants to reference your own couchbase account, which must have the appropriate accesses to the `viastops` bucket.
```
$ pipenv run python load_geojson.py
```
Refresh the Buckets page in the couchbase console and you should now see several thousand features in the `viastops` bucket.
![Buckets page after adding features to viastops bucket](/images/viastops-with-features.png)

## Create the spatial view
![](/images/indexes.png)
![](/images/views.png)
![](/images/views-2.png)
![](/images/create-spatial-view.png)
![](/images/edit.png)
![](/images/spatial-index-code-1.png)
![](/images/spatial-index-code-2.png)

## Perform a spatial query on the view
[Map](https://arcg.is/1CebOf)
```
$ curl -g -u yourusername "http://localhost:8092/viastops/_design/dev_main/_spatial/points?stale=false&connection_timeout=60000&skip=0&full_set=true&start_range=[-98.555659,29.509246]&end_range=[-98.551410,29.511178]"
Enter host password for user 'yourusername':
{"total_rows":0,"rows":[
{"id":"91237","key":[[-98.55471617413822,-98.55471617413822],[29.51027820335144,29.51027820335144]],"value":{"FID":2993,"OBJECTID":4993,"STOP_ID":"91237","LOCATION":"HORIZON HILL & CALLAGHAN","ROUTES":"602","FREQUENT":" "},"geometry":{"type":"Point","coordinates":[-98.55471617413822,29.51027820335144]}},
{"id":"89986","key":[[-98.55445492363533,-98.55445492363533],[29.51036265510136,29.51036265510136]],"value":{"FID":2972,"OBJECTID":4972,"STOP_ID":"89986","LOCATION":"HORIZON HILL & CALLAGHAN","ROUTES":"602","FREQUENT":" "},"geometry":{"type":"Point","coordinates":[-98.55445492363533,29.51036265510136]}},
{"id":"91227","key":[[-98.55361989096805,-98.55361989096805],[29.51011003032731,29.51011003032731]],"value":{"FID":2990,"OBJECTID":4990,"STOP_ID":"91227","LOCATION":"CALLAGHAN & HORIZON HILL","ROUTES":"602","FREQUENT":" "},"geometry":{"type":"Point","coordinates":[-98.55361989096805,29.51011003032731]}}
]
}
```