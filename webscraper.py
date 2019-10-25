from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

path = "/Users/leabroudo/Desktop/moviescraper/chromedriver"
driver = webdriver.Chrome(path)

def hulu_bot():
    driver.get("https://www.hulu.com/start/content?video_type=movie")
    pg = 1
    hulu_media = []

    while True:
    
        #Wait here for page to fully load
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element_value((By.NAME, "page"), str(pg)) 
        )

        page_movies = driver.find_elements_by_class_name("beaconid")
        for movie in page_movies: #might remove (year made) from some
            if movie.text:
                #print(movie.text)
                hulu_media.append(movie.text)
    
        #print(hulu_media)

        try:
            link = driver.find_element_by_xpath('//li[@id="sosodssfs"][1]/a[1]')
        except NoSuchElementException:
            print("All Movies Found")
            break
    
        driver.execute_script("arguments[0].click();", link)
        print(driver.current_url)
        pg += 1

    return hulu_media
    

def hbo_bot():
    driver.get("https://www.hbo.com/movies/catalog")
    hbo_media = []

    page_movies = driver.find_elements_by_xpath("//p[@class='modules/cards/CatalogCard--title']")

    for movie in page_movies: #might remove (year made) from some
        if movie.text:
            #print(movie.text)
            hbo_media.append(movie.text)
    
    return hbo_media


def amazon_bot():
    driver.get("https://www.amazon.com/Movies-Prime-Eligible-Video/s?i=instant-video&bbn=2858905011&rh=n%3A2858905011%2Cp_85%3A2470955011%2Cp_n_entity_type%3A14069184011&lo=list&dc&qid=1561155189&rnid=14069183011&ref=sr_nr_p_n_entity_type_1")
    amazon_media = []

    while True:

        page_movies = driver.find_elements_by_class_name("a-size-medium")
        for movie in page_movies: #might remove (year made) from some
            if movie.text:
                #print(movie.text)
                amazon_media.append(movie.text)
    
        #print(amazon_media)

        try:
            link = driver.find_element_by_xpath('//li[@class="a-last"]/a[1]')
        except NoSuchElementException:
            print("All Movies Found")
            break
    
        driver.execute_script("arguments[0].click();", link)
        print(driver.current_url)

    return amazon_media


def netflix_bot():
    driver.get("https://flixable.com/genre/movies/?min-rating=0&min-year=1920&max-year=2019&order=title#filterContainer")
    pg = 2
    netflix_media = []

    while True:

        page_movies = driver.find_elements_by_tag_name("strong")
        for movie in page_movies: #might remove (year made) from some
            if movie.text:
                #print(movie.text)
                netflix_media.append(movie.text)
    
        #print(netflix_media)

        try:
            link = driver.find_element_by_link_text(str(pg))
        except NoSuchElementException:
            print("All Movies Found")
            break
    
        driver.execute_script("arguments[0].click();", link)
        print(driver.current_url)
        pg += 1

    return netflix_media

hulu_media = hulu_bot()
hbo_media = hbo_bot()
netflix_media = netflix_bot()
amazon_media = amazon_bot()

sep_movies = {
    "hulu" : hulu_media,
    "hbo" : hbo_media,
    "amazon" : amazon_media,
    "netflix" : netflix_media
}

with open('movieData.json', 'w') as outfile:
    json.dump(sep_movies, outfile)