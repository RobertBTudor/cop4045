import csv

def read_casts(filename):
    # (title, year) -> [director, actor1, ..., actor5]
    casts = {}
    file = open(filename, 'r', encoding='utf-8')
    for row in csv.reader(file):
        casts[(row[0], row[1])] = row[2:]
    file.close()
    return casts


def top_entries(entries, limit=10):
    # Sort a list of tuples by their last value (highest first) and keep only the top ones
    ranking = sorted(entries, key=lambda entry: entry[-1], reverse=True)
    return ranking[:limit]


def display_top_collaborations(casts, limit=10):
    #Count how many times each director/actor pair worked together in a movie that is also on the top rated list
    collaborations = {}
    file = open('imdb-top-rated.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        movie = (row[1], row[2])
        if movie not in casts:
            continue
        director = casts[movie][0]
        for actor in casts[movie][1:]:
            pair = (director, actor)
            collaborations[pair] = collaborations.get(pair, 0) + 1
    file.close()

    # Build the ranking as a list of (director, actor, count) tuples
    entries = [(director, actor, count) for (director, actor), count in collaborations.items()]

    print('Top collaborations (top rated movies)')
    for entry in top_entries(entries, limit):
        print(entry)


def display_top_actors(casts, limit=10):
    # add up the box office of every movie each actor played in
    totals = {}
    file = open('imdb-top-grossing.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        movie = (row[1], row[2])
        if movie not in casts:
            continue
        box_office = int(row[3])
        for actor in casts[movie][1:]:
            totals[actor] = totals.get(actor, 0) + box_office
    file.close()

    entries = list(totals.items())  # (actor, total) tuples

    print('Top actors (top grossing movies)')
    for actor, money in top_entries(entries, limit):
        print(actor, '-', '${:,}'.format(money))


def main():
    casts = read_casts('imdb-top-casts.csv')
    display_top_collaborations(casts, 10)
    print()
    display_top_actors(casts, 10)


main()