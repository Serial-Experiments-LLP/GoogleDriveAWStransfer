from re import sub
import get_credentials

import httplib2

from apiclient import discovery

import pandas as pd

import Google_AWS_Download


all_folders = []
file_list = []
folder_name_list = []

def get_root_folder(folder_id, folder_name_list): #get's folder list from original root folder

    credentials = get_credentials.get_credentials()

    http = credentials.authorize(httplib2.Http())

    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(q="mimeType = 'application/vnd.google-apps.folder' and '"+folder_id+"' in parents",

        pageSize=1000, fields="nextPageToken, files(id, mimeType, name)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()

    folders = results.get('files', [])

    if not folders:
        print('No folders found.')

    else:
        for folder in folders:
            print(folder)
            folder_name = folder['name']
            id = folder.get('id')
            temp_dict = {'id':id,'folder_name':folder_name}
            folder_name_list.append(temp_dict)


def get_all_folders(folder_name_list): #creates list of all sub folder under root, keeps going until no folders underneath

    for folder in folder_name_list:
        folder_id = folder['id']
        folder_name = folder['folder_name']
        additional_folders = []
        credentials = get_credentials.get_credentials()

        http = credentials.authorize(httplib2.Http())

        service = discovery.build('drive', 'v3', http=http)
        results = service.files().list(
            q="mimeType = 'application/vnd.google-apps.folder' and '" +folder_id+ "' in parents",

            pageSize=1000, fields="nextPageToken, files(id, mimeType,name)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        items = results.get('files', [])

        for item in items:
            sub_folder_id = item.get('id')
            sub_folder_name = f"{folder_name}/{item['name']}"
            temp_dict = {'id':sub_folder_id,'folder_name':sub_folder_name}
            additional_folders.append(temp_dict)
        if not additional_folders:
            pass
        else:
            all_folders.extend(additional_folders)
            folder_name_list = additional_folders
            get_all_folders(folder_name_list)


def merge(folder_name_list, root_folder_dict): #merges sub folder list with full list
    global full_list
    full_list = all_folders + folder_name_list
    full_list.append(root_folder_dict)


def get_file_list(): #runs over each folder generating file list, for files over 1000 uses nextpagetoken to run additional requests, picks up metadata included in the request
    print(full_list)
    for folder in full_list:
        print(folder)
        folder_id = folder['id']
        folder_name = folder['folder_name']
        credentials = get_credentials.get_credentials()

        http = credentials.authorize(httplib2.Http())

        service = discovery.build('drive', 'v3', http=http)

        page_token = None
        while True:
            results = service.files().list(
                q="'" + folder_id + "' in parents",

                pageSize=1000, fields="nextPageToken, files(name, md5Checksum, mimeType, size, createdTime, modifiedTime, id, parents, trashed)", pageToken=page_token, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()

            items = results.get('files', [])
            for item in items:
                file_name = item['name']
                if folder_name != '':
                    file_name = f"{folder_name}/{file_name}"
                checksum = item.get('md5Checksum')

                size = item.get('size', '-')

                id = item.get('id')

                mimeType = item.get('mimeType', '-')

                createdTime = item.get('createdTime', 'No date')

                modifiedTime = item.get('modifiedTime', 'No date')

                parents = item.get('parents')

                trashed = item.get('trashed')


                file_list.append([file_name, checksum, mimeType, size, createdTime, modifiedTime, id, parents, trashed])

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
    files = pd.DataFrame(file_list,columns=['file_name', 'checksum_md5', 'mimeType', 'size', 'date_created', 'date_last_modified', 'google_id', 'google_parent_id', 'trashed'])
    files.to_pickle('checking.pkl')
    files.drop(files[files['trashed'] == True].index, inplace=True)  # removes files which have True listed in trashed, these are files which had been moved to the recycle bin
    print('Starting file transfer')
    Google_AWS_Download.downloadFileList(files)