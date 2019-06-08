from bs4 import BeautifulSoup
import requests
import urllib
import datetime
import time
from datetime import date
import calendar
import re
import urllib.request
abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}


def GetTitle():
    i = 0
    j = 0

    for td in soup.findAll('td', {'class': 'overview-top'}):
        x = td.a.get('title').split(" (",)
        y = x[1].split(")")
        movie.append(Movie(x[0], y[0], None, None, None, None, None))
        for k in td.p.findAll('span'):
            gen = k.get_text()
            if not re.search("|", gen):
                break
            if(gen != "|"):
                movie[i].genre.append(gen)

        i += 1
def GetDay(y, m):
    num =0
    dateofmovie = []
    j=0
    numberofNone=1
    for td in soup.findAll('h4', {'class': 'li_group'}):
        dateofmovie.append((int(re.search(r'\d+', td.a.get('name')).group())))

    for td in soup.findAll('div', {'class': 'list detail'}):

        for line in td:
            if(line.find("h4") != None and line.find("h4") != -1):
                if j>len(movie):
                    break
                
                d = datetime.date(int(y), int(m), dateofmovie[num])
                
                movie[j].date=(d.isoformat())
                j+=1
                

            elif(line.find("h4") == -1):
                continue
            else:
                if (numberofNone == 1):
                    numberofNone += 1
                    continue
                else:
                    num+=1


def GetSynopsis():
    i =0
    for td in soup.findAll('td', {'class': 'overview-top'}):
        for synopsis in td.findAll('div', {'class': 'outline'}):
            if(synopsis.find("a")):
                movie[i].synopsis = synopsis.get_text()

            else:
                movie[i].synopsis = synopsis.get_text()
                #print(synopsis.get_text())
            i +=1

def GetDirector():
    i = 0
    for di in soup.findAll('div', {'class': 'txt-block'}):
        if(di.h5 != None):
            if (di.h5.text == "Director:"):
                #print(di.a.get_text())
                movie[i].director.append(di.a.get_text())
                i+=1
            elif(di.h5.text == "Directors:"):
                for multi in di.findAll('a'):
                    movie[i].director.append(multi.get_text())
                    #print(multi.get_text())
                i+=1
def GetStars():
    i = 0
    for st in soup.findAll('div', {'class': 'txt-block'}):
        if(st.h5 != None):
            if (st.h5.text == None):
                #print(st.a.get_text())
                continue
                i+=1
            elif(st.h5.text == "Stars:"):
                for multi in st.findAll('a'):
                    movie[i].stars.append(multi.get_text())
                    #print(multi.get_text())
                i+=1

def List():
    print("Listing ...")
    for i in range(0, len(movie)):
        print(movie[i].name)
def ListFrom(date):
    print("Listing from:", date)
    for i in range(0, len(movie)):
        if(datetime.datetime.strptime(movie[i].date, '%Y-%m-%d') >= datetime.datetime.strptime(date, '%Y-%m-%d') ):
            print(movie[i].name)

def ListFromTo(dateFrom, dateTo):
    print("Listing from:", dateFrom, " to:",dateTo)
    for i in range(0, len(movie)):
        if (datetime.datetime.strptime(movie[i].date, '%Y-%m-%d') >= datetime.datetime.strptime(dateFrom, '%Y-%m-%d') and
                datetime.datetime.strptime(movie[i].date, '%Y-%m-%d') <= datetime.datetime.strptime(dateTo, '%Y-%m-%d')):
            print(movie[i].name)
def InfoMovie(movieName):
    print("Info ...")
    for i in range(0, len(movie)):
        if(movieName in movie[i].name):
            print(movie[i].name)
            print("Production year: ", movie[i].year)
            print("Release date: ", movie[i].date)
            print("Genre: ", movie[i].genre)
            print("Synopsis: ", movie[i].synopsis)
            print("Director: ", movie[i].director)
            print("Stars: ", movie[i].stars)
def ListGenre(genrem):
    print("Listing ...")
    for i in range(0, len(movie)):
        
        if genrem in movie[i].genre:
            print(movie[i].name)

def findMonth(inpName):
    inpName = inpName[:3]  # first 3 letter of the month
    inpName = inpName.capitalize()  # make upper case of first letter
    month0 = abbr_to_num[inpName]  # convert month to number
    if (month0 < 10):
        month0 = "0" + str(month0)
    else:
        month0 = str(month0)
    return month0

class Movie(object):
  def __init__(self, name, year, date, synopsis, director, stars = None, genre = None):
    self.name = name
    self.date = date
    self.synopsis = synopsis
    self.year = year
    if stars is None:
        self.stars = []
    else:
        self.stars = stars
    if genre is None:
        self.genre = []
    else:
        self.genre = genre
    if director is None:
        self.director = []
    else:
        self.director = director


movie = []
print("Input List:\n--------------\n*INPUT 'month_name'\nLIST\nLIST from:YYYY/MM/DD\nLIST from:YYYY/MM/DD to:YYYY/MM/DD\nINFO:'movive_name'\nLIST genre:'genre'")
inp = input()
fileCheck = False
while(inp != None):
    if(re.search("INPUT", inp)):
        fileCheck = True
        a = inp.split(' ')
        inp = a[1]
        month = findMonth(inp)
        now = datetime.datetime.now()
        year = now.year
        if(int(month)<now.month):
            year+=1


        myUrl = 'https://www.imdb.com/movies-coming-soon/'+str(year)+'-' + month + '/'
        print(myUrl)
        u = urllib.request.urlopen(myUrl)
        x = u.read().decode('UTF-8')
        soup = BeautifulSoup(x, 'html.parser')
        f = open(inp, 'w')
        f.write(soup.text)
        f.close()

        GetTitle()
        GetDay(year, month)
        GetDirector()
        GetStars()
        GetSynopsis()

    elif(inp == "LIST" and fileCheck == True):
        List()
    elif(re.search("LIST from:",inp) and re.search("to:", inp)==False and fileCheck == True):
        a = inp.split(":")
        inp = a[1]
        ListFrom(inp)
    elif(re.search("LIST from:",inp) and re.search("to:", inp) and fileCheck == True):
        a=inp.split(":")
        b = a[1].split(" ")
    
        ListFromTo(b[0], a[2])
        
    elif(re.search("INFO", inp) and fileCheck == True):
        inp.split(" ")
        InfoMovie(inp[1])
        
    elif(re.search("LIST genre:",inp) and fileCheck == True):
        a = inp.split(":")
        inp = a[1]
        ListGenre(inp)
    elif(fileCheck==False):
        print("Please enter first INPUT:'month'")
    else:
        print("Wrong Input!")
    inp = input()



