def html_content():
    import os
    import webbrowser
    from jinja2 import Template
    import os

    cwd = os.getcwd()
    print("Current working directory:", cwd)

    html_file_path=cwd+"/.github/html_content"
    pull_request_number=123
    

    with open(html_file_path+"/index.html") as f:
        template = Template(f.read())

    # Define the values to be passed to the template
    pull_request_number = 56745
    drift = "driftttttt"

    # Render the template with the values
    output_html = template.render(pull_request_number=pull_request_number, drift=drift)

    # Print the rendered HTML
    print(output_html)

    # Save the HTML content to a file
    with open(html_file_path+"/output.html", 'w') as f:
        f.write(output_html)

    # Open the file in a web browse
    # webbrowser.open("file://"+html_file_path+"/output.html")
    webbrowser.open("file://"+html_file_path+"/output.html")
