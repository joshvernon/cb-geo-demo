# Working with geodata in Couchbase - GeoRodeo 2018 lightning talk

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