## sympan - Python library for downloading data from S3

This is a simple Python library for downloading any content from S3, locally.
It is based on boto3 and joblib. It is really a simple library,
but it is very useful. It uses parallel programming in Python,
as well as boto3.client and boto3.resource. 

## Installation
Make sure you have Python 3.7 installed.

```bash install.sh``` will do the job.

```
pip install sympan

```

will also do the job if you don't want to clone it first.



## Usage


```

from sympan.handlers import S3Handler

from credentials import (AWS_ACCESS_KEY_ID,
                         AWS_SECRET_ACCESS_KEY,
                         REGION_NAME)

if __name__ == '__main__':
    s3 = S3Handler(aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                   region_name=REGION_NAME)

    s3.download_locally(s3_url= "s3://url/path/to/folder/or/file/",
                        destination_folder="local/path/to/destination/folder",
                        n_jobs=2)
```
Here credentials.py is a file where you 
need to put your AWS credentials. The structure in 
destination folder will be the same as in S3 url. Try it!:) 