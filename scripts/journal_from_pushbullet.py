from pushbullet import Pushbullet
import datetime
from os import path, makedirs
import json
import requests

API_KEY = "o.uxcqYCwIuKxm1yLAiJrVBj6VokX09r9o"
pb = Pushbullet(API_KEY)

PATH_JOURNAL = R"C:\Users\nolan\OneDrive\Bureau\TM\Journal de bord"

# TM Journal de bord
## Settings (json)
## 2021-09-27 (folder)
### 2021-09-27 (file, txt, pdf, ...)
## 2021-09-28 (folder)

# Create journal if not exist
if not path.exists(PATH_JOURNAL):
    makedirs(PATH_JOURNAL)

setting_path = path.join(PATH_JOURNAL, "settings.json")
# Create settings if not exist
if not path.exists(setting_path):
    fp = open(setting_path, "w")
    fp.write('{"last_date":1696032000}')
    fp.close()

# Load Settings
fp = open(setting_path, "r")
settings = json.loads(fp.read())
fp.close()
print(settings)

# LastDate
last_date = settings["last_date"]
print(last_date)

# Get Messages
pushes = pb.get_pushes(modified_after=last_date)
print(pushes)


# Messages Actions
def create_note(date: str, time: str, title: str | None, body: str):
    if title == None:
        file_name = time
    else:
        file_name = title + " " + time

    fp = open(path.join(PATH_JOURNAL, date, file_name) + ".txt", "w")
    fp.write(body)
    fp.close()


# Messages Actions
def create_link(date: str, time: str, title: str | None, body: str, url: str):
    if title == None:
        file_name = "$" + time
    else:
        file_name = "$" + title + " " + time

    fp = open(path.join(PATH_JOURNAL, date, file_name) + ".txt", "w")
    if body == None:
        fp.write(url)
    else:
        fp.write(url + "\n" + body)
    fp.close()


# Create File
def create_file(
    date: str, time: str, body: str, file_name: str, file_type: str, file_url: str
):
    r = requests.get(file_url)  # get file data
    file_name = (
        "".join(file_name.split(".")[:1]) + " " + time
    )  # name: title (remove .XXX) HHhMMmSSs
    extention = "." + file_type.split("/")[1]  # audio/mp4 -> .mp4

    fp = open(path.join(PATH_JOURNAL, date, file_name) + extention, "wb")
    fp.write(r.content)
    fp.close()


# Loop Messages Lastest to New
for push in pushes[::-1]:
    type = push["type"]
    timestamp = datetime.datetime.fromtimestamp(float(push.get("modified")))
    date = timestamp.date().strftime("%d-%m-%Y")
    time = timestamp.strftime("%Hh%Mm%Ss")
    print(type, timestamp, date)

    day_path = path.join(PATH_JOURNAL, date)
    if not path.exists(day_path):
        makedirs(day_path)

    if type == "note":
        title: str | None = push.get("title")
        body: str | None = push.get("body")
        print(title, body)
        create_note(date, time, title, body)

    if type == "link":
        title: str | None = push.get("title")
        body: str | None = push.get("body")
        url: str | None = push.get("url")
        print(title, body)
        create_link(date, time, title, body, url)

    if type == "file":
        body: str | None = push.get("body")
        file_name: str | None = push.get("file_name")
        file_type: str | None = push.get("file_type")
        file_url: str | None = push.get("file_url")
        print(file_name, file_type, file_url, body)
        create_file(date, time, body, file_name, file_type, file_url)

# update last_date
if len(pushes) != 0:
    fp = open(setting_path, "w")
    settings["last_date"] = timestamp.timestamp()
    fp.write(json.dumps(settings))
    fp.close()
