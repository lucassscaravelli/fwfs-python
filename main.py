import os
import time
import requests

sleep_seconds = 1
file_path = 'file.txt'
firebase_url = '<firebase_project_name>.firebaseio.com'


def get_modified_time():
    return os.stat(file_path).st_mtime


def get_file_text_content():
    file_o = open(file_path)
    return file_o.read()


def send_to_firebase(txt):
    url = "https://{}/messages.json".format(firebase_url)
    print("Sending {} to {}".format(txt, url))
    r = requests.post(url, json={'txt': txt})
    print("Response:", r.status_code, r.content)


actual_file_modification_time = get_modified_time()

while True:

    print("Reading file {}".format(file_path))
    new_file_modified_time = get_modified_time()

    if new_file_modified_time != actual_file_modification_time:
        print("Changes detected....")
        actual_file_modification_time = new_file_modified_time
        send_to_firebase(get_file_text_content())

    time.sleep(sleep_seconds)
