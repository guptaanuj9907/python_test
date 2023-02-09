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
    
    print("-----Geting the PR number-----")
    ref = os.getenv('GITHUB_REF')
    arr = ref.split("/")
    print("GITHUB REF :",str(ref))
    print("PR no",str(arr[2]))
    pr_number = os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER")
    print("pr number from pr_number GITHUB_EVENT_PULL_REQUEST_NUMBER",pr_number)
    return arr[2]


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
    #     logging.error("Error in get_list_of_file_changed",str(e))

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
    #     logging.error("Error in close_pr",str(e))


def get_block_directory_list():
    """
    Method returns the block directory list from RDS
    """
    # try:
    print("-----Geting the block directory list-----")
    block_dir=[]
    with open(".github/block_dir_list") as file:
        for line in file:
            block_dir.append(line.strip())
    return block_dir
    # except Exception as e:
    #     logging.error("Error in get_block_directory_list",str(e))

def compare_file_changed_and_block_directory(file_changed,block_directory):
    """
    Methos compare file path under file changed and blocker directory
    Returns boolean
    """
    # try:
    print("-----Comapring file changed and block directory file path-----")
    file_present=False
    for file_path in file_changed:
        if file_path in block_directory:
            file_present=True
            break
    return file_present
    # except Exception as e:
    #     logging.error("Error in compare_file_changed_and_block_directory",str(e))

def trigger_cron():
    """
    Method trigger cron whenver PR is opened
    """
    try:
        print("-----Triggering Cron-----")
    #This method should trigger the con whenever PR is created
        pass
    except Exception as e:
        logging.error("Error in trigger_cron",str(e))

def comment_plan():
    pass

def main():
    """
    When PR is created this Method
    1.Trigger the cron
    2.Get the list of file path under file changed
    3.Get the list of block directories
    4.Compare 2 and 3
    5.Close the PR if 4. returns true else trigger from 1. to 4. again
    whenever atlantis plan will run
    """
    # try:
    print("Atlantis plan is triggered..Triggering cron")
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
        close_pr()
    else:
        print("File change file path is NOT present in BLOCK DIRECTORY")
        print("No Drift !!!!!!!!!!!!!...Trigger the cron job again when someone run atlantis plan")
        comment_plan()
    # except Exception as e:
    #     logging.error("Error in get_pr_num",str(e))
    

if __name__ == "__main__":
    main()
    #3