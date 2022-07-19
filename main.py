from pathlib import Path

import instagrapi.exceptions
from instagrapi import Client
import time
import yaml

media_count = {}
story_count = {}


def dl(file, path):
    mediaa = file
    if mediaa.media_type == 1:
        cl.photo_download(int(mediaa.pk), path)
    elif mediaa.media_type == 2:
        if mediaa.product_type == "feed":
            cl.video_download(int(mediaa.pk), path)
        elif mediaa.product_type == "igtv":
            cl.igtv_download(int(mediaa.pk), path)
        elif mediaa.product_type == "clips":
            cl.clip_download(int(mediaa.pk), path)
    elif mediaa.media_type == 8:
        cl.album_download(int(mediaa.pk), path)
    print("downloaded media: " + mediaa.pk)


def get_medias(user_to_dl):
    if media_count[user_to_dl.username] < user_to_dl.media_count:
        path = Path(user_to_dl.username + "/")
        if not path.exists():
            path.mkdir()
        medias = cl.user_medias(int(user_to_dl.pk))
        x = 0
        for media in medias:
            if x <= (len(medias) - media_count[user_to_dl.username]):
                dl(media, path)
                print(str(x) + "/" + str(len(medias) - media_count[user_to_dl.username]))
                time.sleep(5)
            x = x + 1
        media_count[user_to_dl.username] = user_to_dl.media_count
        with open('media_count.yml', 'w') as f:
            yaml.dump(media_count, f)

    elif media_count[user_to_dl.username] > user_to_dl.media_count:
        media_count[user_to_dl.username] = user_to_dl.media_count
        with open('media_count.yml', 'w') as f:
            yaml.dump(media_count, f)


def get_stories(user_to_dl, client):
    stories = client.user_stories(user_to_dl.pk)
    if story_count[user_to_dl.username] < len(stories):
        path = Path(user_to_dl.username + "/stories/")
        if not path.exists():
            path.mkdir()
        x = 1
        for story in stories:
            if x > story_count[user_to_dl.username]:
                try:
                    client.story_download(int(story.pk), Path(user_to_dl.username + "/stories/" + story.pk))
                    print("downloaded story: " + story.pk + " " + str(x) + "/" + str(len(stories)))
                    time.sleep(5)
                except instagrapi.exceptions.UnknownError:
                    print(client.story_info(int(story.pk)))
                    print("Story invalide")
                finally:
                    x = x + 1
                    continue
            else:
                x = x + 1
        story_count[user_to_dl.username] = len(stories)
        with open('story_count.yml', 'w') as f:
            yaml.dump(story_count, f)

    elif story_count[user_to_dl.username] > len(stories):
        story_count[user_to_dl.username] = len(stories)
        with open('story_count.yml', 'w') as f:
            yaml.dump(story_count, f)


if __name__ == '__main__':
    cl = Client()
    verif = input("A2F code verification (google authenticator): ")
    cl.login("pseudo", "password", verification_code=str(verif))

    print(cl.user_id)

    with open("media_count.yml") as f:
        media_count = yaml.safe_load(f)
    with open("story_count.yml") as f:
        story_count = yaml.safe_load(f)
    usernames = ["liste pseudo"]
    ids = []
    for username in usernames:
        ids.append(cl.user_id_from_username(username))
        if username not in media_count:
            media_count[username] = 0
        if username not in story_count:
            story_count[username] = 0
    while True:
        for id_ in ids:
            get_medias(cl.user_info(id_))
            get_stories(cl.user_info(id_), cl)
            print("data of " + cl.user_info(id_).username + " checked")
        with open('story_count.yml', 'w') as f:
            yaml.dump(story_count, f)
        with open('media_count.yml', 'w') as f:
            yaml.dump(media_count, f)
        time.sleep(15)


