Oracle Cloud Infrastructure Object Storage fsspec implementation

Background:

Pandas recently switched their underlying file system mechanism to read data using a project called (fsspec)[https://github.com/intake/filesystem_spec]. 

`fsspec` implements an abstract file system. Reading a csv from s3 for example is handled by Pandas now because `s3://bucket/file` is understood by fsspec.  Similarly, Google /Microsoft/etc have added URI's for their own s3-like cloud storage offerings. Currently in `fsspec` there are the following URI handlers:

 - s3://... -> s3fs.S3FileSystem (requires pip install s3fs)
 - az://... -> adlfs.AzureBlobFileSystem (requires pip install adlfs)
 - dbfs://... -> fsspec.implementations.dbfs.DatabricksFileSystem (requires DataBricks)
 - gcs://...  -> gcsfs.GCSFileSystem (requires pip install gcsfs)
 - gdrive://... -> gdrivefs.GoogleDriveFileSystem (requires pip install gdrivefs)
 - Many more listed here: https://github.com/intake/filesystem_spec/blob/master/fsspec/registry.py

This project adds:

 - oci://... -> ocifs.OCIFileSystem (through `pip install ocifs`)


And the end result is that a user anywhere can run the following:

```import pandas as pd```
```import ocifs```
```df = pd.read_csv("oci://my_bucket@my_namespace/myobject.csv", storage_options={"config": "~/.oci/config"})```
