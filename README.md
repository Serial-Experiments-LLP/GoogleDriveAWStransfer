# Important Disclaimer

v0.5 of the code was tested with a sample folder on Google Drive. We are yet to test this on real data that needs to be transferred.

It is highly recommended that you test this script with a sample folder of your own to know what this code does before you use it to transfer your actual files.

**Do not use this script without fully understanding what it does. Your files might be at risk. We are not responsible for any data loss**

# What has been changed?

The original script (v0.0) was not preserving the Google Drive folder structure after transfering data to S3. We have made the changes to get this missing functionality (v0.5)


# Setup Notes

After cloning this repo, create a folder called 'credentials' and save your client_secret.json file in it. This will change to a more secure method in a future release.

Notes beyond this are exactly what the original author had written in his repo.

________________________________________________________________________________

# GoogleDriveAWStransfer (Currently a test script)
Script to use Google Drive API to collect files and metadata and move to an S3 bucket

Script to pull metadata from Google Drive API, including MD5 checksum
Using authentication from Google Quickstart Python script. To run follow authentication instructions written in the Python Code. For AWS S3 certification it uses the boto3 AWS python client library, you will need a config file set up, as described here - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

To run download all files and run Google_AWS_Transfer.py. On running the script will ask for the Google Drive folder URI which is the parent for any files or sub-folders. It will also ask for an S3 bucket for files to be copied to. Finally it asks for an S3 path 

The script will then collect metadata for all files listed under the parent folder or held in any sub-folders. It will then download the files and hold them in memory, and then move them to the S3 bucket. For any Google Native formats, (e.g Google Docs, Google Sheets), these will be downloaded as an export format (export format used are listed below). For all other formats these are downloaded as they were.

Google Docs - Open Document Text format (.odt)
Google Sheets - Open Document Spreadsheets (.ods)
Google Slides - Open Document Presentation (.odp)
Google Draw - Portable Network Graphic (.png)
Google Jam - Portable Document Format (.pdf)

If any files fail to download an error message will be printed and saved to a log file.

As well as transferring the files it will also collect some metadata from Google Drive and store it as user generated metadata for the S3 objects. Google Metadata fields and their new S3 user defined metadata fields listed below.

id = x-amz-meta-google-id
parents = x-amz-meta-google-parent-id
mimeType = x-amz-google-mimeType
md5checksum = x-amz-google-md5 (this is only for non-Google native formats, for Google native formats the message 'No MD5 as this file is a converted Google Doc'
createdTime = x-amz-google-created-date
modifiedTime = x-amz-meta-google-last-modified-date

