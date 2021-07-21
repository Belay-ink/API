# Created By: 
# Belay Reggassa - 07/21/21

# Args 1/2 - Knowledge Base API username/password

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
#print(payload)

url_test = "https://surfsedev.service-now.com/api/now/table/kb_knowledge"
url_prod = "https://surf.service-now.com/api/now/table/kb_knowledge"
nextBuildNumberPath = "/var/lib/jenkins/jobs/osimage-management-centos/nextBuildNumber" #"/Users/medharatnasais.karri/Desktop/bealy/nextBuildNumber"
JENKINS_JOB_FOLDER= "/var/lib/jenkins/jobs/osimage-management-centos/builds" #"/Users/medharatnasais.karri/Desktop/bealy/builds"


def get_console_log():
    ###################
    #Get the latest successful build 
    ###################
    latestBuildNumber = open(nextBuildNumberPath, 'r')
    latestBuildNumberValue = int(latestBuildNumber.read()) - 1
    latestBuildNumber.close()
    #######################
    #Get the log file from the latest build directory
    #######################
    job_path = JENKINS_JOB_FOLDER + ''.join('/'+ str(latestBuildNumberValue) + '/log')
    print(job_path)
    console_text_file = open(job_path, 'r')
    file_content = console_text_file.read()
    #for line in file_content:
        #line_split = re.split("{}|{}".format(PRE_STR, POST_STR), line)
       # if len(line_split) < 2:
            #console_text_string += line
           # continue
        #console_text_string += line_split[0]
       # console_text_string += line_split[2]
    console_text_file.close()
    return file_content



def main():
    #Get the latest console log text
    latest_build_console_text =get_console_log() #requests.get(console_text_url)
    
    #Process the console log for the POST request 
    html_string_for_post = latest_build_console_text.replace("\n", "<br/>").replace("","<br/>").replace('"',"'")
    
    #Prepare the console log for the POST request 
    final_payload = payload.replace("<REPLACED_TEXT>", html_string_for_post)
    print(final_payload)
    
    #Post the request to the Knowledge API 
    response = requests.post(url_test, data=final_payload.encode('utf-8'), headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
    print(response)

if __name__ == "__main__":
    main()
