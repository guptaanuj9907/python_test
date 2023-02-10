import os
import requests

def auto_merge():
  ## Get the value of GITHUB_REPOSITORY and extract the owner
  print("ENV = ")
  print(os.environ)
  # owner_and_repo = "razorpay/vishnu"
  owner_and_repo = "guptaanuj9907/python_test"

  # Get the pull request number
  pull_request_number = os.environ['GITHUB_EVENT_PULL_REQUEST_NUMBER']

#write a logic to check whether atlantis apply ran successfully or not
#if it ran successfully then run atlantis plan and check the drift
#if their is not drift merge it
#else raise a jira ticket 

  token = os.getenv('GIT_TOKEN')
  header = {'Authorization': 'token ' + token,"Accept": "application/vnd.github+json"}
  url = "https://api.github.com/repos/"+owner_and_repo+"/pulls/" + str(pull_request_number)+"/merge"
  print(url)
  data = {
      "commit_title": "Merge pull request",
      "commit_message": "Merging pull request"
  }
  response = requests.put(url=url, headers=header,json=data)
  print(response)
  if response.status_code == 200:
      print("Merge successful")
  else:
      print("Merge failed")

if __name__ == "__main__":
    auto_merge()

    ####