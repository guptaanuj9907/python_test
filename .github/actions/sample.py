import os
import json
import logging
import datetime
import requests

def get_pr_number():
    ref = os.getenv('GITHUB_REF')
    arr = ref.split("/")
    print("ref "+str(ref))
    print(arr)
    return arr[2]

def get_list_of_file_changed():
    token = os.getenv('GIT_TOKEN')
    header = {'Authorization': 'token ' + token}
    url = "https://api.github.com/repos/guptaanuj9907/python_test/pulls/" + str(get_pr_number()+"/files")
    response = requests.get(url=url, headers=header)
    file_list = [file['filename'] for file in response.json()]
    parent_dir=[]
    for path in file_list:
        parent_dir.append(os.path.dirname(path))
    return parent_dir

def close_pr():
    token = os.getenv('GIT_TOKEN')
    header = {'Authorization': 'token ' + token}
    url = "https://api.github.com/repos/guptaanuj9907/python_test/pulls/" + str(get_pr_number())
    payload = {"state":"closed"}
    response = requests.patch(url=url, headers=header, data = json.dumps(payload))

def get_directory():
    dir=[]
    with open(".github/directory_name") as file:
        for line in file:
            dir.append(line.strip())
    return dir
        
def compare_file_changed_and_directory(file_changed,directory):
    directory_present=False
    for file_path in directory:
        if file_path in file_changed:
            directory_present=True
            break
    return directory_present

def get_block_directory_list():
    block_dir=[]
    with open(".github/block_dir_list") as file:
        for line in file:
            block_dir.append(line.strip())
    return block_dir

def compare_file_changed_and_block_directory(file_changed,block_directory):
    file_present=False
    for file_path in file_changed:
        if file_path in block_directory:
            file_present=True
            break
    return file_present


def main():
    file_changed=get_list_of_file_changed()
    print("file_changed = ",file_changed)
    directory=get_directory()
    print("iam s3 directory name = ",directory)
    s3_iam_dir_present=compare_file_changed_and_directory(file_changed=file_changed,directory=directory)
    print("s3_iam_dir_present = ",s3_iam_dir_present)
    block_dir=get_block_directory_list()
    print("block directories list = ",block_dir)
    print("compare_file_changed_and_block_directory = ",compare_file_changed_and_block_directory(file_changed=file_changed,block_directory=block_dir))
    if s3_iam_dir_present:
        if compare_file_changed_and_block_directory(
            file_changed=file_changed,block_directory=block_dir):
            close_pr()
        else:
            print("No Drift !!!!!!!!!!!!!!")
            print("Trigger the cron job again")
    



            



    





    



    
   







if __name__ == "__main__":
    main()