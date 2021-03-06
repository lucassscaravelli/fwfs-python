import os
import time
import requests

from upm import pyupm_jhd1313m1 as lcd

lcd_refer = lcd.Jhd1313m1(0, 0x3E, 0x62)
sleep_seconds = 1
file_path = 'file.txt'
firebase_url = 'projeto-embarcado.firebaseio.com'


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


def write_lcd(txt):
    print('Writing {} on LCD...'.format(txt))
    lcd_refer.setCursor(0, 0)
    lcd_refer.setColor(255, 0, 0)
    lcd_refer.write('Value: {}'.format(txt))


actual_file_modification_time = get_modified_time()

while True:

    print("Reading file {}".format(file_path))
    new_file_modified_time = get_modified_time()

    if new_file_modified_time != actual_file_modification_time:
        print("Changes detected....")
        actual_file_modification_time = new_file_modified_time
        file_content = get_file_text_content()
        write_lcd(file_content)
        send_to_firebase(file_content)

    time.sleep(sleep_seconds)
