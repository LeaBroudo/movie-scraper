from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


url = "/Users/leabroudo/Desktop/moviescraper/chromedriver"
driver = webdriver.Chrome(url)

driver.get("https://www.hulu.com/start/content?video_type=movie")
page_movies = driver.find_elements_by_class_name("beaconid")


for movie in page_movies: #must remove (year made) from some
    print(movie.text)
