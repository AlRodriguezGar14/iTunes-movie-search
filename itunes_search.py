#!/usr/bin/env python3

import requests
import dateutil.parser
import csv 

class Movie():
    def __init__(self, title, synopsis, url, preview, release):
        self.title = title
        self.synopsis = synopsis
        self.url = url
        self.preview = preview
        self.release = release

    def print_values(self):
        print(f"\n\n#######################################\n\t{self.title}\n{self.synopsis}\n\nTo iTunes Store -> {self.url}\n\nPreview -> {self.preview}\n\nRelease Date -> {self.release}\n=======================================\n")


class Search_movies:
    def __init__(self, inp):
        self.address = "default",
        self.title = "default",
        try:
            self.marketplace = inp.strip().split('-')[1]
        except:
            self.marketplace = "default"
        self.title_list = inp.strip().split('-')[0]
        self.input = self.title_list.strip().split(',')
        self.list_of_movies = []
        self.multiple_search_urls = []
        self.multiple_titles = []
        self.potential_match = ""

    def get_url_single(self):
        self.title = self.input[0].split(' ')
        country_tag = "us" if self.marketplace == "default" else self.marketplace
        self.marketplace = f"&country={country_tag}"

        self.address = f"https://itunes.apple.com/search?term={'+'.join(self.title).lower()}{self.marketplace}&media=movie"

    ## For now, multiple search is only for US marketplace
    def get_url_multiple(self):
        country_tag = "us" if self.marketplace == "default" else self.marketplace
        self.marketplace = ""
        self.marketplace = f"&country={country_tag}"
        for title in self.input:
            splitted = title.lower().split()
            self.multiple_titles.append(' '.join(splitted))

            each_address = f"https://itunes.apple.com/search?term={'+'.join(splitted).lower()}{self.marketplace}&media=movie"
            self.multiple_search_urls.append(each_address)

    def print_address(self):
        print(self.address)
    
    def get_json(self, address_to_get_from):
        return requests.get(str(address_to_get_from)).json()

    def clean_data(self, response):
## Save in a list all the movies provided by apple
        for title in response['results']:
            
            if 'longDescription' not in title: 
                title['longDescription'] = "No description available"
            elif 'previewUrl' not in title:
                title['previewUrl'] = "No preview available"
            elif 'trackViewUrl' not in title:
                title['trackViewUrl'] = 'TrackViewUrl not available' 

            date = dateutil.parser.parse(title['releaseDate'])
            formatted_date = date.strftime('%Y')
            
            self.list_of_movies.append(Movie(title['trackName'], title['longDescription'] or "No Description available", title['trackViewUrl'], title['previewUrl'], formatted_date))


class Print_movies:
    def __init__(self, list_of_movies, multiple_titles):
        self.list_of_movies = list_of_movies
        self.multiple_titles = multiple_titles
        self.exact_matches = []

    def print_each(self):
    # The logic behind this is to display at the bottom of the terminal the title that is closest to the search (the first result given by Apple)
        i = len(self.list_of_movies) - 1
        while i >= 0:
            self.list_of_movies[i].print_values()
            i -= 1

        if len(self.list_of_movies) == 0:
            print("No matches")

    def print_matches_only(self):
        for movie in self.list_of_movies:
            if movie.title.lower() == ' '.join(search_movies.title).lower():
                print(f"\nPotential match for: {movie.title}\nMore info... {movie.url}")
                self.exact_matches.append({'title': movie.title, 'url': movie.url, 'release': movie.release, 'synopsis': movie.synopsis})
                break
            if movie.title.lower() in self.multiple_titles:
                print(f"\nPotential match for: {movie.title}\nMore info... {movie.url}")
                self.exact_matches.append({'title': movie.title, 'url': movie.url, 'release': movie.release, 'synopsis': movie.synopsis})


class Save_output:
    def __init__(self, list_of_movies, multiple_titles, exact_matches):
        self.content_table = './titles_live_on_itunes.csv'
        self.list_of_movies = list_of_movies
        self.multiple_titles = multiple_titles
        self.exact_matches = exact_matches

    def create_table(self):
        self.table = open(self.content_table, 'w')
        self.writer = csv.writer(self.table)
        header = ['Title', 'Release Date', 'URL', 'Synopsis']
        self.writer.writerow(header)
        
    def close_table(self):
        self.table.close()

    def write_all(self):
        self.writer.writerow(['SOFT MATCHES', '', '', ''])
        for movie in self.list_of_movies:
            self.writer.writerow([movie.title, movie.release, movie.url, movie.synopsis])
    
    def write_potential_matches(self):
        self.writer.writerow(['STRONG MATCHES', '', '', ''])

        for title in self.exact_matches:
            self.writer.writerow([title['title'], title['release'], title['url'], title['synopsis']])

        self.writer.writerow(['', '', '', ''])
            


if __name__ == "__main__":

    input = input("search for...\t").replace("&amp;", " ").replace("&apos;", '').replace("&#39;", "").replace("&", " ").replace("'", "").replace(":", "")

    search_movies = Search_movies(input)
    printer = Print_movies(search_movies.list_of_movies, search_movies.multiple_titles)
    save_outouts = Save_output(search_movies.list_of_movies, search_movies.multiple_titles, printer.exact_matches)



# Single search
    if len(input.split(',')) < 2:
        ## Generate a URL
        search_movies.get_url_single()
        
        ## Request to the API
        response = search_movies.get_json(search_movies.address)

        ## Remove the unneccesary data
        search_movies.clean_data(response)

        ## Print each movie
        printer.print_each()


        ## Print the address used for the request
        search_movies.print_address()

# Batch search, only US marketplace
    else:
        search_movies.get_url_multiple()
        for address in search_movies.multiple_search_urls:
            print(address)
            response = search_movies.get_json(address)
            search_movies.clean_data(response)

## Prints if there is a match
    printer.print_matches_only()

## Save the whole data to a csv
    if len(printer.list_of_movies) != 0:
        save_outouts.create_table()
        save_outouts.write_potential_matches()
        save_outouts.write_all()
        save_outouts.close_table()

    
    print(input)



