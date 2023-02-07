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
    r = requests.get(url=url, headers=header)
    print(r.json())
    print("token"+" "+str(token))
    print("url"+" "+url)

def close_pr():
    token = os.getenv('GIT_TOKEN')
    header = {'Authorization': 'token ' + token}
    url = "https://api.github.com/repos/guptaanuj9907/python_test/pulls/" + str(get_pr_number())
    payload = {"state":"closed"}
    r = requests.patch(url=url, headers=header, data = json.dumps(payload))

def main():
    get_list_of_file_changed()
    close_pr()



    
   







if __name__ == "__main__":
    main()