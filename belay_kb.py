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
JENKINS_JOB_FOLDER="/var/lib/jenkins/"


def get_console_log(full_job_name, build_number):
    job_path = JENKINS_JOB_FOLDER + ''.join(['jobs/' + x for x in full_job_name.split("/")]) + '/builds/' + build_number + '/log'
    console_text_file = open(job_path, 'r')
    file_content = console_text_file.read()
    console_text_string = ""
    #for line in file_content:
        #line_split = re.split("{}|{}".format(PRE_STR, POST_STR), line)
       # if len(line_split) < 2:
            #console_text_string += line
           # continue
        #console_text_string += line_split[0]
       # console_text_string += line_split[2]
    console_text_file.close()
    return file_content

def get_jobinfo_from_url(job_url):
    url_components = job_url.split("/")    # This line splits the url (string) on the backslash characters (string -> array)
    url_components_clean = [comp for comp in url_components if comp != 'job' and comp != '']    # This line cleans the url for 'job' prefixes and empty strings
    build_number = url_components_clean[-1]   # Build number will be the last element in the array
    full_job_name = '/'.join([x for x in url_components_clean[2:-1]])
    return full_job_name, build_number

def main():
    #knowladge Api Credentials 
    #base_url = "https://uswpldevops01.corp.service-now.com:8443"
    
    #latest_build_number = requests.get(base_url + "/job/osimage-management-centos/lastSuccessfulBuild/buildNumber"))
    # print("response from latest build number: ", latest_build_number.text)
    
    #console_text_url = base_url + "/job/osimage-management-centos/" + latest_build_number.text + "/consoleText"
    # print(console_text_url)
    job_url = sys.argv[1]
    full_job_name, build_number = get_jobinfo_from_url(job_url)
    job_name_no_path = full_job_name.split("/")[-1]
    #job_console_log = 
    latest_build_console_text =get_console_log(full_job_name, build_number) #requests.get(console_text_url)
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

