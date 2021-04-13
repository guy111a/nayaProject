


import datetime 
import os
import re
# import sys
from google.cloud import storage

path='/tmp'

def create_file_path():
	year = datetime.datetime.now().strftime("%Y")
	month = datetime.datetime.now().strftime("%m")
	file_path = f"/botLogBkp/{year}/{month}"
	return file_path


def upload_to_gcs(file):
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/guy/Documents/gcloud_cred.json" #Set gloud credentials.
	client = storage.Client() #Set gcloud client.
	bucket = client.get_bucket('naya_project_01') #Specify gcloud bucket.
	filename = re.sub(r"\/.*\/(.*\.\w{1,4})",r'\1',file)
	blob = bucket.blob(f"{create_file_path()[1:]}/{filename}") #Set filename format (uploads/year/month/filename).
	blob.upload_from_filename(file)
	blob.make_public()
	url = blob.public_url
	print(f"Image URL - {url}")

if __name__ == '__main__':
    for file in os.listdir(path):
        if file.endswith(".tar.gz"):
            print(f"moving '{file}' to bucket")
            upload_to_gcs(f'{path}/{file}')
            print(f'removing file {path}/{file}')
            os.unlink(f'{path}/{file}')

