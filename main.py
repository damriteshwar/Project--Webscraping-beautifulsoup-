#Downloading and Importing Request
!pip install requests --upgrade --quiet
import requests
#Downloading and Importing BeautifulSoup
!pip install beautifulsoup4 --quiet --upgrade
from bs4 import BeautifulSoup
#Downloading and Importing Pandas
!pip install pandas --quiet --upgrade
import pandas as pd

#Download the webpage using requests
main_url = 'https://www.imdb.com/chart/top'
response = requests.get(main_url)
#The .status_code property can be used to check if the response was successful. A successful response will have an HTTP status code between 200 and 299.
response.status_code 
 #To know the length of the webpage
len(response.text)
page_contents = response.text
#first thousand characters of the webpage
page_contents[:1000]
#Writing the html page to a file locally, i.e. a replica of real html page
with open('top_rated.html', 'w') as f:  
    f.write(page_contents)

#Using Beautiful Soup to parse and extract information
soup = BeautifulSoup(page_contents, 'html.parser')  #Now 'soup' contains entire html in parsed format

#HERE we create a list of MOVIE NAMES 
parent = soup.find_all('td', {'class' : 'titleColumn'})
movie_names = []
cast = []
for item in parent:
    movie_names.append(item.find('a').text)
    cast.append(item.find('a')['title'])
    
#HERE we create a list of MOVIE URL 
movie_urls = []
base_url = 'https://www.imdb.com/'
for item in parent:
    a = item.find('a')
    movie_urls.append(base_url + item.find('a')['href'])
movie_urls[0]

# creating Dictionary 
movies_dict = {
    'Movie Name' : movie_names,
    'Cast' : cast,
    'Movie URLs' : movie_urls
}

movies_df = pd.DataFrame(movies_dict)
 
movie_page = movie_urls[0]  
movie_page
response = requests.get(movie_page)

response.status_code
soup2 = BeautifulSoup(response.text, 'html.parser')

#Release Year
year1 = soup2.find('li', class_="ipc-inline-list__item")  #To fetch the Release Year of the movie
print(year1)

#Rating
rating1 = soup2.find('span',class_='sc-7ab21ed2-1 jGRxWM')  
rating1
#This is the rating of the movie
if rating1 == None:
    rating = 'NA'
else: 
 rating = rating1.text
rating  

#Reviewer's : Number of reviews
reviewers1 = soup2.find('div',class_="sc-7ab21ed2-3 dPVcnq")   
reviewers1
if reviewers1 == None:
    number_of_reviews = 'NA'
else :
 number_of_reviews = reviewers1.text
number_of_reviews 

names = soup2.find_all('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt")
names

#To fetch the director name
director = names[0].a.text  
director

#This is to fetch the Two lead actors in a movie
lead1 = names[2].find_all('a')   
lead = []  #This is the list of two lead actors in the movie
for item in range(len(lead1)):
    lead.append(lead1[item].text)
#Now Converting Python List into a String
    
# initializing delimiter 
delim = "|"
  
# join() used to join with delimiter
lead_actors = delim.join(lead)

print(lead_actors)

#This is to find the image URL of movie poster
img = soup2.find('a', {'class' : 'ipc-lockup-overlay ipc-focusable'})  
image_url = base_url+img['href']
image_url

 #This is to fetch the Genre of the movie
gen = soup2.find('div', class_=['ipc-chip-list sc-16ede01-4 bMBIRz','ipc-chip-list sc-16ede01-5 ggbGKe']) #  #Used two classes for fetching all records
b = gen.find_all('span')
genre1 = []            #This is a list of the Genre of the movie( Generally 3 genres are sepcified for each movie)
for item in range(len(b)):
    genre1.append(b[item].text) 
delim = "|"
genre = delim.join(genre1)  # -1 here is to not take the 'release date' along with the genre
genre

#This is to fetch the summary of the movie
summary = soup2.find('span', {'class' : 'sc-16ede01-2 gXUyNh'}) 
summary.text.strip()

#Creating all helper function that gets you desired webpage by taking page number as argument
def get_page_info(url):                  #This is the function to get BeautifulSoup object for any given URL
    page_url = url
    response = requests.get(page_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(page_url))
    # Parse the `response' text using BeautifulSoup
    soup2 = BeautifulSoup(response.text, 'html.parser')
    return soup2

def get_rating(page_info):
  rating1 = page_info.find('span',class_='sc-7ab21ed2-1 jGRxWM')        #Rating of the movie
  if rating1 == None:
    movie_rating_info = 'NA'
  else: 
    movie_rating_info = rating1.text
  return movie_rating_info

def get_reviewers(page_info):
  reviewers1 = page_info.find('div',class_="sc-7ab21ed2-3 dPVcnq")                #Number of reviews of the movie
  if reviewers1 == None:
    number_of_reviews_info = 'NA'
  else :
    number_of_reviews_info = reviewers1.text
  return number_of_reviews_info

def get_img_url(page_info):
  img = page_info.find('a', {'class' : 'ipc-lockup-overlay ipc-focusable'})  #This is to find the image URL of movie poster
  image_url_info = base_url+img['href']
  return image_url_info

def get_lead_actors(page_info):
  names = page_info.find_all('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt")
  director = names[0].a.text    #Names of Director
  lead1 = names[2].find_all('a')   #This is to fetch the Two lead actors in a movie
  lead = []  #This is the list of two lead actors in the movie
  for item in range(len(lead1)):
    lead.append(lead1[item].text)
  #Now Converting Python List into a String
  delim = "|"    # initializing delimiter
  lead_actors_info = delim.join(lead)  # join() used to join with delimiter
  return director, lead_actors_info

def get_genre(page_info):
  gen = page_info.find('div', class_=['ipc-chip-list sc-16ede01-4 bMBIRz','ipc-chip-list sc-16ede01-5 ggbGKe'])  #This is to fetch the Genre of the movie
  b = gen.find_all('span')
  genre1 = []            #This is a list of the Genre of the movie( Generally 3 genres are sepcified for each movie)
  for item in range(len(b)):
      genre1.append(b[item].text) 
  delim = "|"
  genre_info = delim.join(genre1)  # -1 here is to not take the 'release date' along with the genre
  return genre_info

def get_summary(page_info):
  summary_info = page_info.find('span', {'class' : 'sc-16ede01-2 gXUyNh'}).text  #This is to fetch the summary of the movie
  return summary_info

def get_movie_info(movie_url):
    
    soup2 = get_page_info(movie_url)       #We call this function to get BeautifulSoup object for Movie URL in the argument
    year_of_release = soup2.find('li', class_="ipc-inline-list__item").a.text  #Year of release of the movie
    
    movie_rating = get_rating(soup2)
    number_of_reviews = get_reviewers(soup2)
    director = get_lead_actors(soup2)[0]
    lead_actors = get_lead_actors(soup2)[1]
    image_url = get_img_url(soup2)
    genre = get_genre(soup2)
    summary = get_summary(soup2)

    return year_of_release, movie_rating, number_of_reviews, director, lead_actors, image_url, genre, summary

#Creating a dictionary for all the values that we have fetched from the webpage
movie_dict = {                  
    'year_of_release' : [],
    'movie_rating' : [],
    'number_of_reviews' : [],
    'director' : [],
    'lead_actors' : [],
    'image_url' : [],
    'genre' : [],
    'summary' : []
    
}

for movie in range(len(movie_urls)):               #To get the values for dictionary created above by calling get_movie_info function for all URLs
    details = get_movie_info(movie_urls[movie])
    movie_dict['year_of_release'].append(details[0])
    movie_dict['movie_rating'].append(details[1])
    movie_dict['number_of_reviews'].append(details[2])
    movie_dict['director'].append(details[3])
    movie_dict['lead_actors'].append(details[4])
    movie_dict['image_url' ].append(details[5])
    movie_dict['genre'].append(details[6])
    movie_dict['summary'].append(details[7])
    
#Converting dictionary created from code above to a Dataframe
movie_details_df = pd.DataFrame(movie_dict)  

 #Merging the 1st Dataframe that we had created for Information from Most Popular Movies Page with the data frame now created which has all the information for each movie
df1 = movies_df
df2 = movie_details_df
final_df = pd.concat([df1,df2], axis = 1)   


#Converting the final Dataframe to a CSV File
final_df.to_csv('top_rated_movies.csv', index=None) 


