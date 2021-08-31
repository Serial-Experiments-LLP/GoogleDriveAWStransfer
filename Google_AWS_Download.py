import get_credentials

import httplib2

from apiclient import discovery

import pandas as pd

import io

from io import BytesIO

import boto3
from botocore.exceptions import ClientError, ProxyConnectionError

from datetime import datetime

from googleapiclient.http import MediaIoBaseDownload

import requests



logfile = open("logfile"+datetime.today().strftime('%Y-%m-%d-%H_%M_%S')+".txt", "w+")#logfile to pick up any download errors


S3_BUCKET = input('Enter the S3 bucket for transfer: ')#takes the Google URL
S3_PATH = input('Input S3 path to folder for upload e.g. (Test/): ')

def downloadFileList(files):
    """downloads files based on Google ID and holds them in memory, then transfers to S3 bucket. Picks up mimetype of files,
    if google cloud formats converts to open office equivalent, if anything else downloads as is.
    Google Drive API has a 10MB limit for Google Native doc, if initial download fails then direct download url is used via request module, as no limit applies to this"""
    credentials = get_credentials.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    s3 = boto3.client('s3')
    for index, row in files.iterrows():
        filename = row['file_name']
        mimeType = row['mimeType']
        ID = row['google_id']
        Google_Modified_Date = row['date_last_modified']
        Google_Created_Date = row['date_created']
        Google_Parent_ID = row['google_parent_id']
        Google_MD5 = row['checksum_md5']

        if mimeType == 'application/vnd.google-apps.folder':
            pass
        elif mimeType == 'application/vnd.google-apps.document':
            filename = filename + '.odt'
            Key = "{}{}".format(S3_PATH, filename)
            try:
                s3_response = s3.head_object(Bucket=S3_BUCKET, Key=Key)
                if s3_response['ResponseMetadata']['HTTPStatusCode']==200:
                    print(f"{Key} already exists. Skipping")
                    pass
            except:
                try:
                    request = service.files().export_media(fileId=ID, mimeType='application/vnd.oasis.opendocument.text')
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print
                        ("Download %d%%." % int(status.progress() * 100))
                    s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                except:
                    try:
                        headers = {'Authorization': 'Bearer {}'.format(credentials.access_token), 'User-Agent': 'Mozilla/5.0'}
                        request = "https://docs.google.com/document/d/" + ID + '/export?format=odt'
                        response = requests.get(request, headers=headers)
                        fh = io.BytesIO()
                        fh.write(response.content)
                        s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                    except:
                        print('Issue downloading ' + filename + ' file has not been downloaded')
                        print('Issue downloading ' + filename + ' file has not been downloaded', file=logfile)
                        pass
        elif mimeType == 'application/vnd.google-apps.spreadsheet':
            filename = filename + '.ods'
            Key = "{}{}".format(S3_PATH, filename)
            try:
                s3_response = s3.head_object(Bucket=S3_BUCKET, Key=Key)
                if s3_response['ResponseMetadata']['HTTPStatusCode']==200:
                    print(f"{Key} already exists. Skipping")
                    pass
            except:
            
                try:
                    request = service.files().export_media(fileId=ID, mimeType='application/x-vnd.oasis.opendocument.spreadsheet')
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print
                        ("Download %d%%." % int(status.progress() * 100))
                    
                    s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                except:
                    try:
                        headers = {'Authorization': 'Bearer {}'.format(credentials.access_token), 'User-Agent': 'Mozilla/5.0'}
                        request = "https://docs.google.com/spreadsheets/d/" + ID + '/export?format=ods'
                        response = requests.get(request, headers=headers)
                        fh = io.BytesIO()
                        fh.write(response.content)
                        s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                    except:
                        print('Issue downloading ' + filename + ' file has not been downloaded')
                        print('Issue downloading ' + filename + ' file has not been downloaded', file=logfile)
                        pass
        elif mimeType == 'application/vnd.google-apps.presentation':
            filename = filename + '.odp'
            Key = "{}{}".format(S3_PATH, filename)
            try:
                s3_response = s3.head_object(Bucket=S3_BUCKET, Key=Key)
                if s3_response['ResponseMetadata']['HTTPStatusCode']==200:
                    print(f"{Key} already exists. Skipping")
                    pass
            except:
                try:
                    request = service.files().export_media(fileId=ID, mimeType='application/vnd.oasis.opendocument.presentation')
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print
                        ("Download %d%%." % int(status.progress() * 100))
                    s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                except:
                    try:
                        headers = {'Authorization': 'Bearer {}'.format(credentials.access_token), 'User-Agent': 'Mozilla/5.0'}
                        request = "https://docs.google.com/presentation/d/"+ID+'/export/odp'
                        response = requests.get(request, headers=headers)
                        fh = io.BytesIO()
                        fh.write(response.content)
                        s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                    except:
                        print('Issue downloading '+filename+' file has not been downloaded')
                        print('Issue downloading ' + filename + ' file has not been downloaded', file=logfile)
                        pass
        elif mimeType == 'application/vnd.google-apps.drawing':
            filename = filename + '.png'
            Key = "{}{}".format(S3_PATH, filename)
            try:
                s3_response = s3.head_object(Bucket=S3_BUCKET, Key=Key)
                if s3_response['ResponseMetadata']['HTTPStatusCode']==200:
                    print(f"{Key} already exists. Skipping")
                    pass
            except:
                try:
                    request = service.files().export_media(fileId=ID, mimeType='image/png')
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print
                        ("Download %d%%." % int(status.progress() * 100))
                    s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                except:
                    try:
                        headers = {'Authorization': 'Bearer {}'.format(credentials.access_token), 'User-Agent': 'Mozilla/5.0'}
                        request = "https://docs.google.com/drawings/d/" + ID + '/export/png'
                        response = requests.get(request, headers=headers)
                        fh = io.BytesIO()
                        fh.write(response.content)
                        s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                    except:
                        print('Issue downloading ' + filename + ' file has not been downloaded')
                        print('Issue downloading ' + filename + ' file has not been downloaded', file=logfile)
                        pass
        elif mimeType == 'application/vnd.google-apps.jam':
            filename = filename + '.pdf'
            Key = "{}{}".format(S3_PATH, filename)
            try:

                s3_response = s3.head_object(Bucket=S3_BUCKET, Key=Key)
                if s3_response['ResponseMetadata']['HTTPStatusCode']==200:
                    print(f"{Key} already exists. Skipping")
                    pass
            except:

                try:
                    request = service.files().export_media(fileId=ID, mimeType='application/pdf')
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print
                        ("Download %d%%." % int(status.progress() * 100))
                    s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                except:
                    try:
                        headers = {'Authorization': 'Bearer {}'.format(credentials.access_token), 'User-Agent': 'Mozilla/5.0'}
                        request = "https://jamboard.google.com/d/" + ID + '/export?format=pdf'
                        response = requests.get(request, headers=headers)
                        fh = io.BytesIO()
                        fh.write(response.content)
                        s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                    except:
                        print('Issue downloading ' + filename + ' file has not been downloaded')
                        print('Issue downloading ' + filename + ' file has not been downloaded', file=logfile)
                        pass
        else:
            Key = "{}{}".format(S3_PATH, filename)
            try:
                s3_response = s3.head_object(Bucket=S3_BUCKET, Key=Key)
                if s3_response['ResponseMetadata']['HTTPStatusCode']==200:
                    print(f"{Key} already exists. Skipping")
                    pass
            except:
                try:
                    request = service.files().get_media(fileId=ID)
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print
                        ("Download %d%%." % int(status.progress() * 100))
                    s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID)
                except:
                    request = service.files().get_media(fileId=ID)
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print
                        ("Download %d%%." % int(status.progress() * 100))
                    s3Upload(fh, filename, Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5,
                            mimeType, ID)


def s3Upload(fh,filename,Google_Modified_Date, Google_Created_Date, Google_Parent_ID, Google_MD5, mimeType, ID): #takes file held in memory and transfers to S3 bucket. Also takes Google Drive metadata and adds it to S3 as user added metadata
    s3_resource = boto3.resource('s3')
    if Google_MD5 == None:
        Google_MD5 = 'No MD5 as this file is a converted Google Doc'
    Google_Parent_ID = ', '.join(Google_Parent_ID)
    Key = "{}{}".format(S3_PATH, filename)
    print('Uploading: ',filename,'to S3 bucket')
    s3_resource.Bucket(S3_BUCKET).put_object(
        Key=Key,
        Body=fh.getvalue(),
        Metadata={'Google-Last-Modified-Date': Google_Modified_Date, 'Google-Created-Date': Google_Created_Date, 'Google-MimeType': mimeType, 'Google-MD5': Google_MD5, 'Google-ID': ID, 'Google-Parent-ID': Google_Parent_ID}
    )
    fh.close()
