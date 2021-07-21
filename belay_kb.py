# Args 1/2 - Service Account for DevOps username/password
# Args 3/4 - Knowledge Base API username/password
# Args 5/6 - Service Account for Jenkins username/password

import sys
import json
import requests
import os
import time
from requests.auth import HTTPBasicAuth

payload = json.dumps({
    "description": "Jenkins OS Image Management Log",
    "template": "standard",
    "short_description": "OS Image Management Log for the Security team for image approval - Knowledge Base Article",
    "text": "<REPLACED_TEXT>",
    "kb_knowledge_base": "IT Knowledge",
    "u_bservice": "Knowledge Base",
    "u_display_categories": "Systems"
})
print(payload)

url_test = "https://surfsedev.service-now.com/api/now/table/kb_knowledge"
url_prod = "https://surf.service-now.com/api/now/table/kb_knowledge"

JOB_PATH = "/tmp/opt/jenkins/"
NEW_FILES = os.listdir(JOB_PATH)

def main():
    #knowladge Api Credentials 
    base_url = "https://uswpldevops01.corp.service-now.com:8443"
    latest_build_number = requests.get(base_url + "/job/osimage-management-centos/lastSuccessfulBuild/buildNumber"))
    # print("response from latest build number: ", latest_build_number.text)
    
    console_text_url = base_url + "/job/osimage-management-centos/" + latest_build_number.text + "/consoleText"
    # print(console_text_url)
    
    latest_build_console_text = requests.get(console_text_url)
    # print("response from latest console text: ", latest_build_console_text.text)
    
    
    html_string_for_post = latest_build_console_text.text.replace("\n", "<br/>").replace("","<br/>").replace('"',"'")
    # print(html_string_for_post)
    final_payload = payload.replace("<REPLACED_TEXT>", html_string_for_post)
    print(final_payload)
    #ADM Credentials  
    response = requests.post(url_test, data=final_payload.encode('utf-8'), headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
    print(response)

if __name__ == "__main__":
    main()

