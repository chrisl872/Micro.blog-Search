import bs4 as bs
from urllib.request import urlopen
import urllib
from flask import Flask
from flask import jsonify
app = Flask(__name__)
@app.route('/<string:query>/')
def search(query):
    query = query.replace(" ", "%20")
    response = urlopen('https://micro.blog/discover/search?q=' + query)
    html = response.read()
    soup = bs.BeautifulSoup(html, 'lxml')
    users = soup.find_all('div', {'class': 'discover_user'})
    users_string = ""

    for user in users:
        users_string += str(user)
    users_bs = bs.BeautifulSoup(users_string, 'lxml')
    users_names = users_bs.find_all('a', href=True)
    users_gravatar = users_bs.find_all('img', src=True)
    users_array = []
    gravatars = []
    for gravatar in users_gravatar:
        gravatars.append(str(gravatar['src']))
    for users_name in users_names:
        if users_name.string != None:
            users_array.append({'full_name': users_name.string.strip(), 'handle': users_name["href"].replace('/', '@'), 'image': ''})
    for i, user_dict in enumerate(users_array):
        user_dict["image"] = gravatars[i]
    return jsonify({"users": users_array})

app.run()