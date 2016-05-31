victors = {}

with open("worldcup_clean.csv") as clean:
	countries = clean.readlines();
	for country in countries:
		country = country.strip();
		country = country.split(',');
		if country[2] in victors and country[1] == "1":
			victors[country[2]] += 1
		elif country[1] == "1":
			victors[country[2]] = 1
		else:
			continue

print victors
