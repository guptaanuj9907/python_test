import os
import requests

# Get the value of GITHUB_REPOSITORY and extract the owner
print("ENV = ")
print(os.environ)
repo = os.environ['GITHUB_REPOSITORY']  #guptaanuj9907/python_test
owner, repository = repo.split("/")

# Get the pull request number
pull_request_number = os.environ['GITHUB_EVENT_PULL_REQUEST_NUMBER']

# Check if atlantis apply ran successfully
# write logic here to determine if atlantis apply ran successfully
atlantis_apply_success = True

if atlantis_apply_success:
  # Fetch the comments on the pull request
  comments_url = "https://api.github.com/repos/{}/"+owner+"/"+repository+"/pulls/{}/comments".format(owner, pull_request_number)
  response = requests.get(comments_url)
  comments = response.json()

  # Look for a comment containing "Apply Failed"
  apply_failed = False
  for comment in comments:
    if "Apply Failed" in comment['body']:
      apply_failed = True
      break

  if not apply_failed:
    # Atlantis apply ran successfully, so run atlantis plan and check the drift
    # You'll need to write your own logic here to run atlantis plan and check the drift
    
    # After the drift has been checked, merge the code
    # You'll need to write your own logic here to perform the merge
    pass
