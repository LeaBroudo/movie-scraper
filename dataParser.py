import json

with open('movieData.json') as json_data:
    sep_movies = json.load(json_data)

###############~~~MOVIE CLASS~~~###############
class Movie:
    def __init__(self, title):
        self.title = title
        self.hbo = "Unavailable"
        self.hulu = "Unavailable"
        self.netflix = "Unavailable"
        self.amazon = "Unavailable"

    def __repr__(self):
        return "%s" % (self.title)

    def __str__(self):
        return "%s\nHBO...... %s\nHulu..... %s \nNetflix.. %s\nAmazon... %s\n"\
            % (self.title, self.hbo, self.hulu, self.netflix, self.amazon,)

    def set_hbo(self):
        self.hbo = "Available"
    
    def set_hulu(self):
        self.hulu = "Available"
    
    def set_netflix(self):
        self.netflix = "Available"
    
    def set_amazon(self):
        self.amazon = "Available"

###############~~~RAW DATA PARSE FOR LIST~~~###############

def soFar(title):
    for movie in all_movies:
        if title == movie["title"]:
            return movie

all_movies = []
for streamer in sep_movies:
    for title in sep_movies[streamer]:
        title = title.strip().upper()

        movie = soFar(title)
        new = False
        if not movie:
            new = True
            movie = {
                "title" : title,
                "hulu" : "Unavailable",
                "hbo" : "Unavailable",
                "amazon" : "Unavailable",
                "netflix" : "Unavailable"
            }

        movie[streamer] = "Available"
    
        if new:
            all_movies.append(movie)

###############~~~LIST DUMP~~~###############

with open('finalMovieList.json', 'w') as outfile:
    json.dump(all_movies, outfile)



