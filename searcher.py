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
    words = title.split()
    keys = []

    for word in words:
        if word != "THE" and word != "AND" and len(word)>2:
            keys.append(word)

    return keys

def paid_search(title):
    path = "/Users/leabroudo/Desktop/moviescraper/chromedriver"
    driver = webdriver.Chrome(path)
    driver.set_window_position(-10000,0)
        
    name = ""
    for word in title.split():
        name += word + "+"

    driver.get("https://www.google.com/search?q="+name+"movie+where+to+watch")
    
    try:
        incomplete = driver.find_element_by_class_name("dUFb4e")
        driver.execute_script("arguments[0].click();", incomplete)
    except NoSuchElementException:
        pass
    
    try:
        found_title = driver.find_element_by_xpath('//div[@class="SPZz6b"]/div[1]/span').text
    except NoSuchElementException:
        print("There is no streaming availability of this movie.")
        driver.quit()
        return 

    try: 
        streamers = driver.find_elements_by_class_name("hl")
        prices = driver.find_elements_by_xpath('//div[@class="ulLPN"]')
    except NoSuchElementException:
        pass
    try:
        streamers = driver.find_elements_by_class_name("i3LlFf")
        prices = driver.find_elements_by_xpath('//div[@class="V8xno"]')
    except NoSuchElementException:
        print("There is no streaming availability of this movie.")
        driver.quit()
        return 

    if not streamers:
        print("There is no streaming availability of this movie.")
        driver.quit()
        return 

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
            continue
        
        movie_indiv = key_words(movie["title"])
        for key in target_indiv:
            if key in movie_indiv:
                similar.append(movie)

    if not found:
        print("\nNo titles matched your search.")
        print("\nSearching for movie availability on other services...")
        paid_search(target) 
        
    if similar:
        view = input("\nWould you like to view the availability of similar movies? (y/n) ")
        if view != "y":
            return 
            
        ind = 0
        while ind < len(similar):
            print(beautify(similar[ind]))
                
            ind += 1

            if ind % 5 == 0:
                more = input("View more similar movies? (y/n) ")
                if more == "n":
                    return 

search()