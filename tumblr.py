import argparse
import pytumblr
import random
import json
from infosys import infosys
from bs4 import BeautifulSoup

rand = random.SystemRandom()

infosysKey = 'f771b64c-077c-4acb-8b19-37dd0470e469'#requires 1 space

def getPost(client, user):
    info = client.blog_info(user)
    nposts = info['blog']['posts']

    postnum = rand.randint(0, nposts - 1)

    post = client.posts(user, offset = postnum, limit = 1)
    body = BeautifulSoup(post['posts'][0]['body'])
    return ' '.join(body.stripped_strings)

def getPostWithLimit(client, user, line_limit = 80):
    while True:
        post = getPost(client, user)
        if len(post) <= line_limit:
            return post

def post(text):
    global infosysKey
    info = infosys(infosysKey)
    info.addText(0, text, 'ROTATE')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Post to infosys from tumblr.')
    parser.add_argument("-u", "--user", help="tumblr user to read from")
    parser.add_argument("-c", "--credsFile", help="credentials file")
    args = parser.parse_args() 
    
    creds = json.loads(open(args.credsFile, "r").read())

    client = pytumblr.TumblrRestClient(
        creds['consumerKey'],
        creds['consumerSecret'],
        creds['oauthToken'],
        creds['oauthSecret']
    )

    post(getPostWithLimit(client, args.user))
    
