from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
import undetected_chromedriver as uc

movie_list = [
]

def getMoviesFromList(movie_file_path):
    file = open(movie_file_path, 'r')
    file_content = file.readlines()
    for movie in file_content:
        movie.replace('\n', '')
        movie_list.append(movie)

getMoviesFromList('./movies.txt')

movies_array = []

def get_movie_poster(movie, driver):
    print('- Getting the ' + movie + ' poster...\n')
    driver.get('https://www.google.com.br/imghp?hl=pt-BR&ogbl')
    sleep(3)
    search_input = driver.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    search_input.send_keys(movie + ' poster hd')
    search_input.send_keys(Keys.RETURN)

    driver.find_element('xpath', '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img').click()
    sleep(3)
    poster_url = driver.find_element('xpath', '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img').get_attribute('src')
    print('- ' + movie + ' poster collected.\n')
    return poster_url

def get_movie_trailer(movie, driver):
    print('- Getting the ' + movie + ' trailer...\n')
    driver.get('https://www.youtube.com/')
    sleep(3)
    driver.find_element('xpath', '//*[@id="search-input"]/input').send_keys(movie + ' trailer HD')
    driver.find_element('xpath', '//*[@id="search-icon-legacy"]').click()
    sleep(3)
    link_element = driver.find_element('xpath', '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a')
    print('- ' + movie + ' trailer collected.\n')
    return link_element.get_attribute('href')
    

def get_movie_info(movie):
    options = Options()
    options.headless = True
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print('\n========= Starting the data collection of ' + movie + ' ============\n')
    driver.get("https://www.imdb.com/")
    driver.find_element('xpath', '//*[@id="suggestion-search"]').send_keys(movie)
    driver.find_element('xpath', '//*[@id="suggestion-search-button"]').click()
    driver.find_element('xpath', '/html/body/div[2]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]/div[2]/div[1]/a').click()

    # Getting the basic movie info

    movie_description = driver.find_element('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p').text
    movie_year = driver.find_element('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[1]').text
    movie_rating = driver.find_element('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[2]/a').text
    movie_time_duration = driver.find_element('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]').text
    print('- Basic info of ' + movie + ' collected.\n')

    movie_genres = []
    genres_elements = driver.find_elements('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div/div[2]/a')
    for genre in genres_elements:
        movie_genres.append(genre.text)
    print('- Genres of ' + movie + ' collected.\n')

    movie_directors = []
    movie_directors_quantity = driver.find_elements('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[4]/div/div/ul/li[1]/div/ul/li')
    for movie_director in range(0, len(movie_directors_quantity)):
        director = driver.find_element('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[4]/div/div/ul/li[1]/div/ul/li[' + str(movie_director + 1) + ']/a').get_attribute('textContent')
        movie_directors.append(director)
    print('- Directors of  ' + movie + ' collected.\n')

    movie_stars = []
    movie_stars_quantity = driver.find_elements('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[4]/div/div/ul/li[3]/div/ul/li')
    for movie_star in range(0, len(movie_stars_quantity)):
        star = driver.find_element('xpath', '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[4]/div/div/ul/li[3]/div/ul/li[' + str(movie_star+1) + ']/a').get_attribute('textContent')
        movie_stars.append(star)
    print('- Stars of ' + movie + ' collected.\n')

    # Getting the movie Poster
    movie_poster = get_movie_poster(movie, driver=driver)

    # Getting the movie trailer link
    movie_trailer = get_movie_trailer(movie, driver=driver)

    movies_array.append({
        'movie_name': movie,
        'movie_year': movie_year,
        'movie_rating' : movie_rating,
        'movie_duration': movie_time_duration,
        'movie_genres': movie_genres,
        'movie_directors': movie_directors,
        'movie_stars': movie_stars,
        'movie_description': movie_description,
        'movie_poster': movie_poster,
        'movie_trailer': movie_trailer
    })

    print('- ' + movie + ' scraping completed.\n')
    print('====== Status: ' + str(len(movies_array)) + '/' + str(len(movie_list)) + ' completed. =====\n')
    driver.quit()

for movie in movie_list:
    get_movie_info(movie)


with open('movies.json', 'w') as final:
    json.dump(movies_array, final, indent=2) 

print('=== Process completed ===')