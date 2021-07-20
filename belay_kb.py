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

 #URL for KB and end point 
url_test = "https://surfsedev.service-now.com/api/now/table/kb_knowledge"

 
url_prod = "https://surf.service-now.com/api/now/table/kb_knowledge"
 
def main():

 
base_url = "https://uswpldevops01.corp.service-now.com:8443"

 # send a request using ADM cridentials to get the last sucessfull build
latest_build_number = requests.get(base_url + "/job/osimage-management-centos/lastSuccessfulBuild/buildNumber", auth = HTTPBasicAuth(sys.argv[5], sys.argv[6]))

 
# print("response from latest build number: ", latest_build_number.text)


console_text_url = base_url + "/job/osimage-management-centos/" + latest_build_number.text + "/consoleText"

# print(console_text_url)
 #Get the consule text using the KB
latest_build_console_text = requests.get(console_text_url, auth = HTTPBasicAuth(sys.argv[5], sys.argv[6]))

# print("response from latest console text: ", latest_build_console_text.text)


#Automation 
html_string_for_post = latest_build_console_text.text.replace("\n", "<br/>").replace("�","<br/>").replace('"',"'")

 
# print(html_string_for_post)
final_payload = payload.replace("<REPLACED_TEXT>", html_string_for_post)

print(final_payload)

 #post the url using KB cridetials to servicenow page
response = requests.post(url_test, data=final_payload.encode('utf-8'), headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(sys.argv[3], sys.argv[4]))

 
print(response)

if __name__ == "__main__":

 
main()





