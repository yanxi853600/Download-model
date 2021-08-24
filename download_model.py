# !pip install afs2-model
from afs import models
from botocore.client import Config
import boto3

import requests
import json
from requests.structures import CaseInsensitiveDict

def get_access_token():   
    url = "https://" 
    
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    data = "{ \"username\": \"\", \"password\": \"\", \"userDetail\": true}"
    #data =json.loads(data)
    access_token = requests.post(url, data=data, headers=headers)
    access_token=json.loads(access_token.text)
    access_token = access_token.get("accessToken")
    return access_token


model_name = "V2_ckpt_48.pth"
token_url = 'http://'
token = get_access_token()
head = {"Authorization": "Bearer "+token}


# 解析json，找到 owner
instance_id=requests.get("http://", headers=head)
instance_id_data=json.loads(instance_id.text) 
data_id=instance_id_data.get("resources")
instance_id = data_id[0].get("owner")

# 解析json，找到 model's name的 uuid = model_rep_id
model_rep_url = requests.get('http://', headers=head)
rep_url_data=json.loads(model_rep_url.text) 
rep_url=rep_url_data.get("resources")
for i in range(10):
    if rep_url[i].get("name") == model_name :
        model_rep_url = rep_url[i].get("uuid")

#  解析json，找到 uuid
model_id_url = requests.get('http://', headers=head)
model_url_data = json.loads(model_id_url.text) 
model_url_data = model_url_data.get("resources")
model_id_url = model_url_data[0].get("uuid")

myUrl = 'https://'+str(instance_id)+'/model_repositories/'+str(model_rep_url)+'/models/'+str(model_id_url)+'?alt=media'
model = requests.get(myUrl, headers=head)
print("get the url of model download.")

f = open('./'+rep_url[i].get("name"), 'wb')
f.write(model.content)
f.close()
print("model is download succefully.")
