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


def main():
    token = os.getenv('GIT_TOKEN')
    head = {'Authorization': 'token ' + token}
    url = "https://api.github.com/repos/razorpay/vishnu/pulls/" + str(get_pr_number())
    payload = {"state":"closed"}
    r = requests.patch(url=url, headers=head, data = json.dumps(payload))
    print("token"+" "+str(token))
    print("url"+" "+url)







if __name__ == "__main__":
    main()