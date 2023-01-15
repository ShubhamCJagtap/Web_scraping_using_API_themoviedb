"""
    Developed By : Shubham Jagtap
    linkedIn : https://www.linkedin.com/in/shubham-jagtap-scj4497/
    
    PLEASE CREATE API ACCOUNT ON  "https://www.themoviedb.org/"
    
    How to use program:
    1. Run the File
    3. Provide API
    2. Provide the language and number of pages
    3. Program will automatically scrape the data and it will store it in following CSV format 
    'Id','original_title','English Title','Overview','Release Date','Genre','Cast','Producer','Director'
    
    
    Enjoy movies scraping

"""
#------------------------------------ IMPORT LIBRARIES

import requests
import csv

def save_file(movies):
    print("Saving in CSV file")
    filename='Movies'+str('.csv')
    with open(filename,'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Id','original_title','English Title','Overview','Release Date','Genre','Cast','Producer','Director'])
        writer.writerows(movies)
#----------------------------------------------------------
def get_data(data,API,genres_dict):
    movie = []
    for i in data['results']:
        try:
            #print("Id ",i['id'])
            #print("title ",i['original_title'])
            #print("English Title",i['title'])
            #print("Overview ",i['overview'])
            #print("Release Date",i['release_date'])
            genre = []
            for j in i['genre_ids']:
                genre.append(genres_dict[j])
            #print(genre)
            id_ = i['id']
            response_1 = requests.get("https://api.themoviedb.org/3/movie/"+str(id_)+"/credits?api_key="+str(API)+"&with_origin_country=IN")
            data_1 = response_1.json()
            response_2 = requests.get("https://api.themoviedb.org/3/movie/"+str(id_)+"/keywords?&api_key="+str(API))
            data_2 = response_2.json()
            keywords = []
            for n in data_2['keywords']:
                keywords.append(n['name'])
            #print(keywords)
            cast = []
            for k in data_1['cast']:
                cast.append(k['name'])
            #print(cast)
            producer = []
            for l in data_1['crew']:
                if l['known_for_department']=='Production':
                    producer.append(l['name'])
            #print(producer)
            director = []
            for m in data_1['crew']:
                if m['known_for_department']=='Directing':
                    director.append(m['name'])
            #print(director)
            movie.append((i['id'],i['original_title'],i['title'],i['overview'],i['release_date'],genre,cast,producer,director))
        except:
            pass
    return movie
#----------------------------------------------------------
# Main Code
API = str(input("Please share your themoviedb API : "))
dataset = []
print('Select Language \n type 1 for Hindi \n type 2 for English\n')
option = int(input())
if option == 1:
    lang = "hi"
elif option == 2:
    lang = "en"
pages = int(input("Enter number of pages you want to scrape (20 movies per page)"))
response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key={}&language=en-US".format(API))
data = response.json()
genres = data['genres']
genres_dict = {}
for i in genres:
    genres_dict[i["id"]] = i["name"]
response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key={}&with_original_language={}".format(API,lang))
if pages>1:
    for i in range(pages+1):
        if i>0:
            response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key={}&with_original_language={}&page={}".format(API,lang,str(i)))
            print("https://api.themoviedb.org/3/discover/movie?api_key={}&with_original_language={}&page={}".format(API,lang,str(i)))
            data = response.json()
            print('getting movies from page ',str(i))
            movies = get_data(data,API,genres_dict)
            dataset = dataset + movies
else:
    response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key={}&with_original_language={}".format(API,lang))
    print("https://api.themoviedb.org/3/discover/movie?api_key={}&with_original_language={}".format(API,lang))
    data = response.json()
    print('getting movies from page 1')
    movies = get_data(data,API,genres_dict)
    dataset = dataset + movies
print("Done !!!")
save_file(dataset)
print('Enjoy!!!')
