import os
import webbrowser
from flask import  render_template

# Replace this with the full path to your HTML file
import os


cwd = os.getcwd()
print("Current working directory:", cwd)

# html_file_path = '/Users/anuj.gupta/Desktop/sdlc/python_test/python_test/s3/index.html'

html_file_path=cwd+"/s3/index.html"

pull_request_number=123

webbrowser.open('file://' + os.path.realpath(html_file_path) + f'?pull_request_number={pull_request_number}')

# webbrowser.open(html_file_path)

render_template('index.html')

