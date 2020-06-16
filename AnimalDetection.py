import cv2
import numpy as np
import datetime

#ObjectStorage
import ibm_boto3
from ibm_botocore.client import Config, ClientError

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from playsound import playsound
import json
from watson_developer_cloud import VisualRecognitionV3

#CloudantDB
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import requests


COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "WIb0bdrcTUI8pXDHngmT0FL_Zrmq_wS4BJSr7EF9cc6h" # eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_RESOURCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/5f9df5d928e54541a638b45c0093d608:e91d6362-75be-4dd0-b467-7beff833a393::"



# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)


#Provide CloudantDB credentials such as username,password and url

client = Cloudant("9badadc3-9e1a-45a6-84a2-0a72603bd382-bluemix", "0d6a2e404d79dc22cea8bf1c54b716c963ac8c3bad199970dc29807da5db0771", url="https://9badadc3-9e1a-45a6-84a2-0a72603bd382-bluemix:0d6a2e404d79dc22cea8bf1c54b716c963ac8c3bad199970dc29807da5db0771@9badadc3-9e1a-45a6-84a2-0a72603bd382-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()

#Provide your database name

database_name = "normal"

my_database = client.create_database(database_name)

if my_database.exists():
    print(f"'{database_name}' successfully created.")


def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))


def multi_part_upload1(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))



def alert():
    playsound('./alert.mp3')
    
    r=requests.get('https://www.fast2sms.com/dev/bulk?authorization=35hbkAxuqIzViLR60yfWaBmZ48NjnSMOpDYcHPod7T9sGeCJtrqHBvgenV3hCxtYIWwmu1pjz2s8d97J&sender_id=FSTSMS&message=An animal entered restricted area&language=english&route=p&numbers=8088048673')
    print(r.status_code)

def live_streaming():
    while (cap.isOpened()):
        ret,frame=cap.read()
        out.write(frame)
        cv2.imshow("Videocapture",frame)

        check,frame=cap.read()#here frame stores color image
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        picname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        cv2.imwrite(picname+".jpg",frame)
        
        multi_part_upload("dppoojary1", picname+".jpg", picname+".jpg")
        json_document={"link":COS_ENDPOINT+"/"+"dppoojary1"+"/"+picname+".jpg"}
        new_document = my_database.create_document(json_document)

        if new_document.exists():
            print(f"Document successfully created.")

        

        with open(picname+".jpg", 'rb') as images_file:
            classes = visual_recognition.classify(
                images_file,
                threshold='0.7',
                classifier_ids='Project_1966178948').get_result()#if we need general change it to general
        dicti=json.dumps(classes, indent=2)
        #dicti=json.dumps(classes, indent=2)
        result=json.loads(dicti)
        x=result["images"]
        y=x[0]
        a=y["classifiers"]
        b=a[0]
        c=b["classes"]
        d=c[0]
        temp=d["class"]
        

        if temp=="Animal.zip":

            database_name1 = "animals"

            my_database1 = client.create_database(database_name1)

            if my_database1.exists():
                    print(f"'{database_name1}' successfully created.")
            

            multi_part_upload1("dppoojary1", picname+".jpg", picname+".jpg")
            json_document1={"link":COS_ENDPOINT+"/"+"dppoojary1"+"/"+picname+".jpg"}
            new_document1 = my_database1.create_document(json_document1)

            if new_document1.exists():
                print(f"Document successfully created.")
                alert()
            
            continue


authenticator = IAMAuthenticator('zeCn1MvliNiZ2T6Q1Ly7l5EKiKZlpgMVK0ILiq8_coKw')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/63b74a21-c68b-42e7-bb85-4b3e558b0c4c')

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='8S6t-LvA6549a9sBZvOjmlmSepRKVlLhTRBwcQ06gxN3')

cap=cv2.VideoCapture(0)

rec=cv2.VideoWriter_fourcc(*'XVID')

out=cv2.VideoWriter('output.avi',rec,20.0,(640,480))

print(cap.isOpened())

#while (cap.isOpened()):

with open('live.mp3', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                'Live video streaming opening,',
                voice='en-US_AllisonV3Voice',
                accept='audio/mp3'
        ).get_result().content)

playsound('live.mp3')

while (cap.isOpened()):
    live_streaming()
    


    Key=cv2.waitKey(1)
    if Key==ord('q'):
        #release the camera
        cap.release()
        #destroy all windows
        cv2.destroyAllWindows()
        break
