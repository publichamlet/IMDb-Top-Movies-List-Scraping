#!/usr/bin/env python3

""" Getting the Top 250 Movie details from IMDb website """

import sys, os
import requests
from bs4 import BeautifulSoup
import csv
from time import perf_counter
from moviePage.moviePage import MovieInnerPage


start = perf_counter()

csv_file = 'IMDb_Top_250_Movie_list.csv'
csv_file_path = 'downloads/IMDb_Top_250_Movie_list.csv'

""" Setting the current working directory & creating project directories """
if sys.platform.startswith('linux'):
    os.chdir(os.path.dirname(__file__))

if 'downloads' not in os.listdir():
    os.mkdir('downloads')
    os.mkdir('downloads/html')

""" getting the html data from the website to scrap """
imdb_url = 'https://www.imdb.com/chart/top/'

imdb_req = requests.get(imdb_url)
print(f'Website Status code: {imdb_req.status_code}')

imdb_html = imdb_req.text

""" Parser through the website using BS4 """
imdb_soup = BeautifulSoup(imdb_html, 'html.parser')

""" Checking the object imdb_soup """
print(imdb_soup.title.string == 'Top 250 Movies - IMDb')

""" Creating the csv file """
if csv_file not in os.listdir('downloads'):
    with open(csv_file_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Movie Title', 'Release Year', 'Storyline', 'Movie Genre',
            'Movie Duration', 'IMDb Movie Rating', 'Movie Certification',
            'IMDb Users Votes'])

""" The details required are under section 
        <tbody class='lister-list'>
            <tr> """

moviePage_list = list()

tbody_sec = imdb_soup.find(name='tbody', attrs={'class': 'lister-list'})
tr_secs = tbody_sec.findAll(name='tr')

count = 1

for tr_sec in tr_secs:
    os.system('clear')
    print(f'processing page {count} .............')
    
    td_movNameYear = tr_sec.find(name='td', attrs={'class': 'titleColumn'})
    movieTitle = td_movNameYear.a.string
    movieYear = td_movNameYear.span.string[1:-1]
    
    # if statement for avaoiding the repeated movie details
    if (movieTitle, movieYear) not in moviePage_list: 
        moviePage_list.append((movieTitle, movieYear))
        
        moviePage_url = 'https://imdb.com' + td_movNameYear.a['href']
        moviePage_obj = MovieInnerPage(user_url=moviePage_url)
        
        movieStory = moviePage_obj.movieStory()
        movieCategories = moviePage_obj.movieCategories()
        movieHours = moviePage_obj.movieHours()
        movieRating = moviePage_obj.movieRating()
        movieCert = moviePage_obj.movieCert()
        movieVote = moviePage_obj.movieVote()
        
        movieRow = [movieTitle, movieYear, movieStory, movieCategories,
                        movieHours, movieRating, movieCert, movieVote]
        
        with open(csv_file_path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(movieRow)
        
        moviePage_obj.htmlGenerate()
        count += 1

    else:
        continue

print(
    f'Total time taken to complete the scrapping \
        IMDb website using BS4 & Requests \
            modules{(perf_counter() - start) / 60:.4f}min')
