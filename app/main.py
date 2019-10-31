from flask import Flask, render_template, request
import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import random
from pytube import YouTube
from pytube import Playlist


def extractLinks(url):
    links = []
    if(url.startswith("http://") or url.startswith("https://")):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            link = link.get('href')
            if(link is not None and (link.startswith("http://") or link.startswith("https://"))):
                links.append(link)
        return links
    else:
        return("Incorrect URL !!")
# Emails


def extractEmails(urlstr):
    url = urlstr
    if(url.startswith("http://") or url.startswith("https://")):
        proc = []
        mail = []
        try:
            response = requests.get(url)
            if( response.status_code == 200):
                soup = BeautifulSoup(response.text, 'html.parser')
                links = [a.attrs.get('href') for a in soup.select('a[href]')]
                for i in links:
                    if(("contact" in i or "Contact")or("Career" in i or "career" in i))or('about' in i or "About" in i)or('Services' in i or 'services' in i):
                        proc.append(i)
                proc = set(proc)
                for j in proc:
                    if(j.startswith("http") or j.startswith("www")):
                        r = requests.get(j)
                        if(r.status_code == 200):
                            data = r.text
                            soup = BeautifulSoup(data, 'html.parser')
                            for name in soup.find_all('a'):
                                k = name.text
                                a = bool(
                                    re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', k))
                                if('@' in k and a == True):
                                    k = k.replace(" ", '').replace('\r', '')
                                    k = k.replace('\n', '').replace('\t', '')
                                    if(len(mail) == 0)or(k not in mail):
                                        print(k)
                                    mail.append(k)
                    else:
                        newurl = url+j
                        r = requests.get(newurl)
                        if(r.status_code == 200):
                            data = r.text
                            soup = BeautifulSoup(data, 'html.parser')
                            for name in soup.find_all('a'):
                                k = name.text
                                a = bool(
                                    re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', k))
                                if('@' in k and a == True):
                                    k = k.replace(" ", '').replace('\r', '')
                                    k = k.replace('\n', '').replace('\t', '')
                                    if(len(mail) == 0)or(k not in mail):
                                        print(k)
                                    mail.append(k)
                mail = set(mail)
                return mail
            else:
                return("error")
        except Exception as e:
            if(len(mail) != 0):
                return mail
            else:
                return(e)
    else:
        return("Incorrect URL !! ")


def images(urlstr):
    url = urlstr
    if(url.startswith("http://") or url.startswith("https://")):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for img in soup.find_all('img'):
                src = img.get('src')
                print(src)
                name = random.randrange(1, 10000)
                imgname = str(name)
                lk = url+"/"+src
                print("llll", lk)
                # wget.download(lk)
                urllib.request.urlretrieve(lk, imgname)
        except Exception as e:
            return(e)
    else:
        return("Incorrect URL !! ")


app = Flask(__name__, template_folder='template')


@app.route('/', methods=['POST', 'GET'])
def home():
    print(request.form)
    return render_template('index.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if(request.method == 'POST'):
        print("request from", request.form)
        if(len(request.form) != 0 or request.form['address'] or request.form['category']):
            url = request.form['address']
            category = request.form['category']
            if(category == "links"):
                print("========>Links<======== ")
                links = extractLinks(url)
                print("linksssssss",links)
                if(type(links) != list):
                    return render_template('error.html')
                else:
                    return render_template('links.html', links=links)
            elif(category == "emails"):
                print("============>Emails<==========")
                emails = extractEmails(url)
                print("emails",emails, type(emails))
                if(isinstance(emails, set) or isinstance(emails, list)):
                    print(("success!!"))
                    return render_template('emails.html', emails=emails)
                else:
                    return render_template('error.html')
            elif(category == "images"):
                print("===============>Images<=============")
                img = images(url)
                if(img):
                    return render_template('error.html')
                else:
                    return render_template('status.html')
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')
    # return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)

    # elif(category == "vidoes"):
    # 	try:
    # 		video = vidoes(url)
    # 		YouTube('https://www.youtube.com/watch?v=BzcBsTou0C0').streams.first().download()
    # 		return render_template('status.html')
    # 	except Exception as e:
    # 		return render_template('error.html')
