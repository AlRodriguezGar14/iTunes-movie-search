# iTunes Search

iTunes Search is a python script that search in the different marketplaces of iTunes if a movie is available or not. You can search for movies individually or in batches.


## Usage

When launching the script, I will ask you for an input. These are the three ways you can use it:

- Write the name of the movie and press enter. This will search of the movie in the US marketplace.

- Write the name of the movie and separated with a slash (-), the code of the country you want to search in. This will search in other marketplaces.

    *movie -country*

    Where country can be -es for Spain, -fr for France, -gb for UK, etc.

- Write as many movies as you want, each separated with a coma. This will batch search for movies in the US marketplace and let you know which are the potential matches. Please, keep in mind that if the name is not exact the same, this can fail. It's just a helpful starting point. 
    
    If you want to batch search in a marketplace that is not the US, then add a slash with the country code after the list.

    *movie1, movie2, movie3, movie4 -es*


If there are matches, the app will also create a CSV file with the strong and soft matches. This file overwrites the previos one (if the same name) to avoid unnoticed or unwanted over-accumulation.

Strong matches = There is a match with the exact title.
Soft matches = There is a match with similar title.
