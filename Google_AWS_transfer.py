#!/usr/bin/Python3


folder_id = input('Enter the URL of the Google folder which is the parent of all files and folder to transfer: ')  # takes the Google URL
folder_id = folder_id.rsplit('/', 1)[-1]  # strips rest of url to keep just the Google ID
root_dict = {'id':folder_id,'folder_name':''}


import Google_API_Metadata


folder_name_list = []

if __name__ == '__main__':
    print('Collecting folder id list')
    Google_API_Metadata.get_root_folder(folder_id, folder_name_list)
    Google_API_Metadata.get_all_folders(folder_name_list)
    Google_API_Metadata.merge(folder_name_list, root_dict)
    print('Generating file metadata list')
    Google_API_Metadata.get_file_list()
print('Files Transferred')
print('done!')