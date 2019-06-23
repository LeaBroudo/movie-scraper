from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json

with open('finalMovieList.json') as json_data:
    all_movies = json.load(json_data)

def beautify(movie):
    length = 25

    final = "\n%s\n" % (movie["title"].upper())
    for streamer in movie:
        if streamer == "title":
            continue
        elif streamer == "hbo":
            final += "HBO" + "."*(length-len(streamer)) + "%s\n" % movie[streamer]
        elif streamer == "iTunes":
            final += "%s" % streamer + "."*(length-len(streamer)) 
            final += "%s\n" % movie[streamer]
        else:
            final += "%s" % streamer.capitalize() + "."*(length-len(streamer)) 
            final += "%s\n" % movie[streamer] 

    return final

def key_words(title):
    keys = title.split()
    for word in keys:
        if word == "THE" or word == "AND" or len(word)<3:
            keys.remove(word)
    return keys

def paid_search(title):
    path = "/Users/leabroudo/Desktop/moviescraper/chromedriver"
    driver = webdriver.Chrome(path)
    driver.set_window_position(-10000,0)
        
    name = ""
    for word in title.split():
        name += word + "+"

    driver.get("https://www.google.com/search?q="+name+"movie")
    
    try:
        incomplete = driver.find_element_by_class_name("dUFb4e")
        driver.execute_script("arguments[0].click();", incomplete)
    except NoSuchElementException:
        pass
    
    found_title = driver.find_element_by_xpath('//div[@class="SPZz6b"]/div[1]/span').text
    
    streamers = driver.find_elements_by_class_name("hl")
    prices = driver.find_elements_by_xpath('//div[@class="ulLPN"]')
    
    if not streamers:
        streamers = driver.find_elements_by_class_name("i3LlFf")
        prices = driver.find_elements_by_xpath('//div[@class="V8xno"]')

    if not streamers:
        print("There is no streaming availability of this movie.")
        driver.quit()
        return 


    print(len(streamers),len(prices))

    catalog = {"title" : found_title}
    for i in range(len(streamers)):
        catalog[streamers[i].text] = prices[i].text

    if catalog:
        print("The following movie was found:")
        print(beautify(catalog))
    else:
        print("No other streaming options available.")
    
    driver.quit()

def search():
    target = input("\nEnter a movie to search: ").strip().upper()
    target_indiv = key_words(target)
    found = False
    similar = []

    for movie in all_movies:
        if not found and target == movie["title"]:
            print(beautify(movie))
            found = True
        
        movie_indiv = key_words(movie["title"])
        count = 0
        for key in target_indiv:
            if key in movie_indiv:
                count += 1
            if count > 2:
                similar.append(movie)
                

    if not found:
        print("\nNo titles matched your search.")
        print("\nSearching for movie availability on other services...")
        paid_search(target) 
        
        view = input("\nWould you like to view the availability of similar movies? (y/n) ")
        if view == "y" and similar:
            for movie in similar:
                print(beautify(movie))
        elif view == "y" and not similar:
            print("\nSorry, no similar movies found.\n")


search()