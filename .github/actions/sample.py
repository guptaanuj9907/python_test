import os
import json
import logging
import datetime
import requests

def get_pr_number():
    try:
        ref = os.getenv('GITHUB_REF')
        arr = ref.split("/")
        return arr[2]
    except Exception as e:
        print("Error in get_pr_num",str)

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

def trigger_cron():
    #This method should trigger the con whenever PR is created
    pass

def flow():
    #triggering cron whenever PR is created
    print("PR is created..Triggering cron")
    trigger_cron() 
    print("Triggered Cron")
    #getting list of file path in file changed
    print("Getting list of file paths of file changed")
    file_changed=get_list_of_file_changed() 
    print("file_changed = ",file_changed)
    #getting the list of directory for eg iam and s3 to compare with file changed path
    print("Getting the list of directory for eg IAM and S3")
    directory=get_directory()
    print("Directory name = ",directory)
    #comparing filechanged file path and directory to check for eg iam or s3
    print("Comparing file path of file changed with directory")
    s3_iam_dir_present=compare_file_changed_and_directory(file_changed=file_changed,directory=directory)
    print("IAM or S3 directory present in file changed path = ",s3_iam_dir_present)
    return s3_iam_dir_present,file_changed
    


def comment_plan():
    pass

def main():
    
    #triggering cron whenever PR is created
    print("PR is created..Triggering cron")
    trigger_cron() 
    print("Triggered Cron")
    #getting list of file path in file changed
    print("Getting list of file paths of file changed")
    file_changed=get_list_of_file_changed() 
    print("file_changed = ",file_changed)
    #getting the block directory list
    print("Getting the list of block directories")
    block_dir=get_block_directory_list()
    print("block directories list = ",block_dir)
    print("Checking IAM and S3 directory present in file changed file path")
    print("compare_file_changed_and_block_directory = ",compare_file_changed_and_block_directory(file_changed=file_changed,block_directory=block_dir))
    print("Checking block directory with file change file path")
    if compare_file_changed_and_block_directory(file_changed=file_changed,block_directory=block_dir):
        print("File change file path is present in BLOCK DIRECTORY")
        print("Closing the PR")
        # close_pr()
    else:
        print("File change file path is NOT present in BLOCK DIRECTORY")
        print("No Drift !!!!!!!!!!!!!!...Trigger the cron job again when some ran atlantis paln")
        comment_plan()
    




def main1():
    # 1. trigger cron 2. compare iam and s3 directory  with file changed
    s3_iam_dir_present,file_changed=flow()
    #getting the block directory list
    print("Getting the list of block directories")
    block_dir=get_block_directory_list()
    print("block directories list = ",block_dir)
    print("Checking IAM and S3 directory present in file changed file path")
    print("compare_file_changed_and_block_directory = ",compare_file_changed_and_block_directory(file_changed=file_changed,block_directory=block_dir))
    if s3_iam_dir_present:
        print("IAM and S3 directory is present in file changed file path")
        print("Checking block directory with file change file path")
        if compare_file_changed_and_block_directory(file_changed=file_changed,block_directory=block_dir):
            print("File change file path is present in BLOCK DIRECTORY")
            print("Closing the PR")
            close_pr()
        else:
            print("File change file path is NOT present in BLOCK DIRECTORY")
            print("No Drift !!!!!!!!!!!!!!!...Trigger the cron job again when some ran atlantis paln")
            comment_plan()
    else:
        print("IAM and S3 directory is NOT present in file changed file path")
        print("No need to do anything !!!!!!!!")

if __name__ == "__main__":
    main()