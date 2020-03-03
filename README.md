# RINEX FILE GENERATOR

Global Navigation Satellite System (GNSS) refers to a constellation of satellites providing signals from space that transmit positioning and timing data to GNSS receivers.
There is a standardised open-source ASCII file format called RINEX (Receiver Independent Exchange Format) which these observations are made available in.
One of these networks in the NOAA CORS network in the United States. RINEX observation data from each of their base stations is published in 1 hour blocks on their FTP server at ftp://www.ngs.noaa.gov/cors/rinex. You can read more about the network here: http://geodesy.noaa.gov/CORS/

### Prerequisites

You need to install python3.6 or above on your local, for MacOS. if the
script need to run on other OS, please check teqc toolkits, it will
require update to that OS version, otherwise it will get unexpected
issue.

Install Brew then Install Python3

```
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
$ brew install python3
```

Install git

```
brew install git
```
please download the repo by git

```
git clone https://github.com/cooper2008/RinexGenerater.git
```

Install all python libs, under project root dir

```
python3 -m pip install -r requirement.txt
```



### Running Script

-n input Station_ID, 

-r input expandsearch_ratio you can add hours time to give more flexible
time range to perform the search, please input integer etc 1,2,3

-s input start time ISO8601 strings etc 2020-03-01T09:11:22Z

-e input end time ISO8601 strings etc 2020-03-01T09:11:22Z

```
python3 grab_data.py -n 1nsu -r 1 -s 2020-03-01T09:11:22Z -e 2020-03-01T21:11:22Z
```



## Running the unittests

```
python3 testsuite.py
```

### Logging

Log is temporary point to /tmp/RINEXgenerator.log

## Versioning

Ver 1.0

## Further Development

Ver1.1 Serverless Version

1. Plan to use AWS API gateway and Lambda build http restful APIs
2. Serverless Deployment to Lambda and API gateway

## Authors

* **Cooper Guo** - *Initial work* -


## License


## Acknowledgments
