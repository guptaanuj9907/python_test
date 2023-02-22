import os
import json
import logging
import datetime
import requests

# owner_and_repo = "razorpay/vishnu"
owner_and_repo = "guptaanuj9907/python_test"

def get_pr_number():
    """
    Method returns the PR number whenever PR is opened or reopened
    """
    # try:
    print("-----Geting the PR number-----")
    if os.getenv('GITHUB_EVENT_NAME') == "pull_request":
        print("GITHUB_EVENT_NAME :",os.getenv('GITHUB_EVENT_NAME'))
        ref = os.getenv('GITHUB_REF')
        pr_number = ref.split("/")
        print("GITHUB REF :",str(ref))
        print("PR no",str(pr_number[2]))
        return pr_number[2]
    elif os.getenv('GITHUB_EVENT_NAME') == "issue_comment":
        print("GITHUB_EVENT_NAME :",os.getenv('GITHUB_EVENT_NAME'))
        pr_number = os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER")
        print("pr number from pr_number GITHUB_EVENT_PULL_REQUEST_NUMBER",pr_number)
        # return arr[2]
        return pr_number
    # except Exception as e:
    #     print("Error in get_pr_num",str(e))

def get_list_of_file_changed():
    """
    Method returns the list of file path under file changed
    """
    # try:
    print("-----Geting the list of file path under file changed-----")
    token = os.getenv('GIT_TOKEN')
    header = {'Authorization': 'token ' + token}
    url = "https://api.github.com/repos/"+owner_and_repo+"/pulls/" + str(get_pr_number()+"/files")
    print(url)
    response = requests.get(url=url, headers=header)
    print(response)
    file_list = [file['filename'] for file in response.json()]
    print(file_list)
    parent_dir=[]
    for path in file_list:
        parent_dir.append(os.path.dirname(path))
    return parent_dir
    # except Exception as e:
    #     print("Error in get_list_of_file_changed",str(e))

def close_pr():
    """
    Method closes the opened PR
    """
    # try:
    print("-----Closing the PR-----")
    token = os.getenv('GIT_TOKEN')
    header = {'Authorization': 'token ' + token}
    url = "https://api.github.com/repos/"+owner_and_repo+"/pulls/" + str(get_pr_number())
    payload = {"state":"closed"}
    response = requests.patch(url=url, headers=header, data = json.dumps(payload))
    # except Exception as e:
    #     print("Error in close_pr",str(e))


def get_block_directory_list():
    """
    Method returns the block directory list from RDS
    """
    # try:
    print("-----Geting the block directory list-----")
    import boto3
    import csv
    import io

    # S3 bucket and file information
    bucket_name = 'test-state-bucket2'
    file_key = 'sdlc_block_directory_list.csv'
    
    # Create an S3 client
    s3 = boto3.client('s3')
    # Get the object containing the file
    s3_object = s3.get_object(Bucket=bucket_name, Key=file_key)
    # print("s3_object")
    # print(s3_object)

    # Read the contents of the file
    file_contents = s3_object['Body'].read().decode('utf-8')
    # print("file_contents")

    reader = csv.DictReader(io.StringIO(file_contents))
    filtered_data = [row for row in reader if row['status'] == 'blocked']
    # print("filtered_data",filtered_data)
    # Extract the 'block_directory','email' and "github_id "fields
    blocked_directories = [row['block_directory'] for row in filtered_data]
    print("blocked_directories",blocked_directories)
    emails = [row['email'] for row in filtered_data]
    print("emails",emails)
    github_id = [row['github_id'] for row in filtered_data]
    print("github_id",github_id)

    return blocked_directories,emails,github_id


def compare_file_changed_and_block_directory(file_changed,block_directory,emails,github_id):
    """
    Methos compare file path under file changed and blocker directory
    Returns boolean
    """
    # try:
    print("-----Comparing file changed and block directory file path-----")
    file_present=False
    user_email=None
    user_github_id=None
    for i in range(len(block_directory)):
        if block_directory[i] in file_changed:
            user_email=emails[i]
            user_github_id=github_id[i]
            file_present=True
            break
    return file_present,user_email,user_github_id


def comment_plan():
    pass

def main():
    """
    When PR is created this Method
    1.Get the list of file path under file changed
    2.Get the list of block directories
    3.Compare 2 and 3
    4.If file changed belong to block directory then Close the PR only if it is not created by PR owner 
    5.If file changed doesnot belong to block directory  run from 1. to 4. again whenever atlantis plan will run
    """
    # try:
    print('GITHUB_REPOSITORY_OWNER :',os.getenv('GITHUB_REPOSITORY_OWNER'))
    print('GITHUB_ACTOR :',os.getenv('GITHUB_ACTOR'))
    print('GITHUB_TRIGGERING_ACTOR',os.getenv('GITHUB_TRIGGERING_ACTOR'))
        
    print("PR is created..")
    #getting list of file path in file changed
    print("Getting list of file paths of file changed")
    file_changed=get_list_of_file_changed() 
    print("file_changed = ",file_changed)
    #getting the block directory list
    print("Getting the list of block directories")
    block_dir,emails,github_id=get_block_directory_list()
    print("block directories list = ",block_dir)
    print("Checking block directory with file change file path")
    file_present,user_email,user_github_id=compare_file_changed_and_block_directory(file_changed=file_changed,block_directory=block_dir,emails=emails,github_id=github_id)
    print("Is file changed file path present in block directory :",file_present)
    if file_present:
        print("File change file path is present in BLOCK DIRECTORY")
        if os.getenv('GITHUB_REPOSITORY_OWNER') != user_github_id:
        #have to check if the PR raiser is same person who created the drift then do nothing else close the pr
            print("Closing the PR")
            close_pr()
        else:
            print("PR is not being closed since it created by drift creator : {}".format(user_github_id))
    else:
        print("File change file path is NOT present in BLOCK DIRECTORY")
        print("No Drift !!!!!!!!!!!!!...Trigger the cron job again when someone run atlantis plan")
        comment_plan()
    # except Exception as e:
    #     print("Error in get_pr_num",str(e))
    

if __name__ == "__main__":
    main()