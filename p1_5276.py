"""
John Fahringer jrf115@zips.uakron.edu
Big Data Programming _ Project1
All rights reserved
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
string = '---------------------------------------------------------------------------------'
def get_year(str_list):
    s = [i.replace('(', '').replace(')', '') for i in str_list]
    s2 = [i.split() for i in s]
    y_list = [list(filter(lambda x: x.isdigit() and len(x) == 4, i)) for i in s2]

    return [int(i[0]) if len(i) > 0 else np.nan for i in y_list]

# Make display smaller
pd.options.display.max_rows = 10
pd.options.display.max_columns = 10

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
usersdata = pd.read_table('movielens/users.dat', sep='::',
                      header=None, names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratingsdata = pd.read_table('movielens/ratings.dat', sep='::',
                        header=None, names=rnames)

mnames = ['movie_id', 'title', 'genres']
moviesdata = pd.read_table('movielens/movies.dat', sep='::',
                       header=None, names=mnames)
#print(moviesdata, ratingsdata, usersdata)


### Show total number of rows with missing values (after join all files), and remove those rows from the DataFrame ###
data = pd.merge(pd.merge(ratingsdata, usersdata), moviesdata)
#print(data)
print("Total number of rows with missing values: ", np.count_nonzero(data.isnull()))
data = data.dropna()
print("Dropped rows, which results in:\n", data)


# Show total number of movies, genres, users, and ratings
print(string, '\n', "Total number of movies", len(moviesdata.index))
movie_by_genre = moviesdata.groupby('genres').size()
#print(string, '\n', 'moviebygenere:', movie_by_genre)
print(string, '\n', "Total number of genres", len(movie_by_genre.index))
print(string, '\n', "Total number of users", len(usersdata.index))
print(string, '\n', "Total number of ratings", len(ratingsdata.index))


### Plot the histograms ... ###
### ... for number of ratings per user
import matplotlib.pyplot as plt

ratings_per_user = ratingsdata.groupby('user_id')['movie_id'].count()
print(string, '\n', '\nratings_per_user\n', ratings_per_user)
plt.hist(ratings_per_user, bins=50)
plt.title("ratings per user")
plt.show()

### ... for number of movies per year
movies_per_year = moviesdata.copy()
movies_per_year['title'] = get_year(movies_per_year['title'])
movies_per_year = movies_per_year.groupby('title')['movie_id'].count()
print(string, '\n', '\nnumber of movies per year\n', movies_per_year)
plt.hist(movies_per_year, bins=50)
plt.title('numberof movies per year')
plt.show()

### ... for number of movies per genre
movies_per_genre = moviesdata.groupby('genres')['movie_id'].count()
print(string, '\n', '\nNumber of movies per genre:\n', movies_per_genre)
""" Notice in movie_by_genre in line 45-46 is similar to how movies_per_genre is built here."""
plt.hist(movies_per_genre, bins=50)
plt.title('number of movies per genre')
plt.show()

### ... for average ratings per movie
avgRatings_per_movie = data.groupby('movie_id')['rating'].mean()
print(string, '\n', '\nAverage rating per movie\n', avgRatings_per_movie)
plt.hist(avgRatings_per_movie, bins=50)
plt.title('Average ratings per Movie')
plt.show()

### ... for average ratings per genra
avgRatings_per_genre = data.groupby('genres')['rating'].mean()
print(string, '\n', '\nAverage ratings per genra\n', avgRatings_per_genre)
plt.hist(avgRatings_per_genre, bins=50)
plt.title('Average ratings per genra')
plt.show()


### Show the number of users whose number of ratings are greater or equal to the median of the number of ratings, ###
medianNumRatings = ratings_per_user.median()
print(string, '\n', "\nMedian of the number of ratings\n", medianNumRatings)
users_numRatingsGreaterOrEqualTo_medianNumRatings = data.groupby('user_id')['rating'].count() >= medianNumRatings
#print("DF of people who do and don't exceed or meet the median (True / False)",  users_numRatingsGreaterOrEqualTo_medianNumRatings)
users_AND_greaterEqual_2_medianNumRatings = pd.DataFrame(ratings_per_user[ratings_per_user > medianNumRatings])
#print("\nUsers AND greaterorequal to median number of ratings:\n", users_AND_greaterEqual_2_medianNumRatings)
print("\nNumber of users whose number of ratings are greater or equal to the Median of the number of ratings\n", len(users_AND_greaterEqual_2_medianNumRatings.index))


### Show the top ten movies with title and genres rated by each user from (1) ###
print(string, '\n')
users_from_usersANDmedianRatings = pd.DataFrame(users_AND_greaterEqual_2_medianNumRatings.index.tolist(), columns=['user_id']) # Makes a DF of a single column 'user_id'
print("\nThe users:\n", users_from_usersANDmedianRatings)
print("The frick::::\n", pd.DataFrame(ratingsdata[['user_id', 'movie_id', 'rating']]))
selectUsers_and_movie_stuff = pd.merge(pd.merge(users_from_usersANDmedianRatings,
                                                pd.DataFrame(ratingsdata[['user_id', 'movie_id', 'rating']])), moviesdata)
print("\nDoes the merge work?\n", selectUsers_and_movie_stuff)
#print("\nDoes this show the top ten?" , users_who_r_greaterEqual_2_medianNumRatings.nlargest(10, 'rating'))