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
    print("downloaded: " + mediaa.pk)


def get_medias(user_to_dl):
    if media_count[user_to_dl.username] < user_to_dl.media_count:
        path = Path(user_to_dl.username + "/")
        if not path.exists():
            path.mkdir()
        medias = cl.user_medias(int(cl.user_id_from_username(user_to_dl.username)), user_to_dl.media_count)
        media_count[user_to_dl.username] = user_to_dl.media_count
        print(media_count[user_to_dl.username])
        for media in medias:
            dl(media, path)
            time.sleep(10)
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
        story_count[user_to_dl.username] = len(stories)
        print(media_count[user_to_dl.username])
        for story in stories:
            time.sleep(10)
            try:
                client.story_download(int(story.pk), Path(user_to_dl.username + "/stories/" + story.pk))
            except instagrapi.exceptions.UnknownError:
                print("Story invalide")
            finally:
                continue
    elif story_count[user_to_dl.username] > len(stories):
        story_count[user_to_dl.username] = len(stories)
        with open('story_count.yml', 'w') as f:
            yaml.dump(story_count, f)


if __name__ == '__main__':
    cl = Client()
    cl.login("pseudo", "mdp")

    with open("media_count.yml") as f:
        media_count = yaml.safe_load(f)
    with open("story_count.yml") as f:
        story_count = yaml.safe_load(f)
    usernames = ["liste pseudo"]
    while True:
        for username in usernames:
            user_id = cl.user_info_by_username(username)
            get_medias(user_id)
            get_stories(user_id, cl)
        with open('story_count.yml', 'w') as f:
            yaml.dump(story_count, f)
        with open('media_count.yml', 'w') as f:
            yaml.dump(media_count, f)
        time.sleep(15)
        print("new run")


