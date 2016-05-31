# key:value pair of number of movies made by studios
studios = {}

with open("2013clean.csv") as clean:
	movies = clean.readlines()
	for movie in movies:
		movie = movie.strip()
		movie = movie.split(',')
		if len(movie) > 2: #throw out bad lines
			if movie[1] not in studios:
				studios[movie[1]] = 1
			else:
				studios[movie[1]] += 1

# sort dict by values and print the studio with the most movies made
sortedStudios = sorted(studios, key = studios.get)
sortedStudios.reverse()
sortedMovieCount = sorted(studios.values())
sortedMovieCount.reverse()

print sortedStudios[0], sortedMovieCount[0]
