import csv

def add_user(sn, username, fullname):
    """
    Part a)
    Adds a new user with no friends to the social network.

    Args:
        sn: The social network dictionary.
        username: The username of the new user.
        fullname: The full name of the new user.

    Returns:
        True if the user was added, False if the username already exists.
    """
    try:
        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True

    except Exception as error:
        print(f"Sorry, could not add user '{username}': {error}")
        raise


def add_friend(sn, user1, user2):
    """
    Part b)
    Adds a mutual friend link between two users.

    Args:
        sn: The social network dictionary.
        user1: The username of the first user.
        user2: The username of the second user.

    Returns:
        True if the link was added, False if either user is not found
        or if both usernames are the same.
    """
    try:
        if user1 not in sn or user2 not in sn or user1 == user2:
            return False

        friends1 = sn[user1][1]
        friends2 = sn[user2][1]

        if user2 not in friends1:
            friends1.append(user2)

        if user1 not in friends2:
            friends2.append(user1)

        return True

    except Exception as error:
        print(f"Sorry, could not add friendship between {user1} and {user2}: {error}")
        raise


def get_friends(sn, user1, distance):
    """
    Part c)
    Finds all friends of a user up to a given link distance.

    Args:
        sn: The social network dictionary.
        user1: The username to start from.
        distance: The maximum link distance (a positive integer).

    Returns:
        A list of usernames at distance 1, 2, ...n, distance from user1.
        The list is empty if the username is not found, the distance is
        not positive, or there are no friends to return.
    """
    try:
        if user1 not in sn or distance < 1:
            return []

        # Visited users are tracked to avoid cycles.
        visited = {user1}
        current = sn[user1][1]
        result = []

        # Breadth First Search that collects friends by level up to the given distance while using a set to prevent infinite loops.
        for _ in range(distance):
            next_level = []

            for user in current:
                if user not in visited:
                    visited.add(user)
                    result.append(user)
                    next_level.extend(sn[user][1])

            current = next_level

        return result

    except Exception as error:
        print(f"Sorry, could not find friends for '{user1}': {error}")
        raise


def save_network(filename, sn):
    """
    Part d)
    Saves a social network to a CSV file. Each row holds one user in the
    format: username, full name, friend1, friend2, ...
 
    Args:
        filename: The name of the CSV file to write.
        sn: The social network dictionary.
 
    Raises:
        FileNotFoundError: If the folder for the file does not exist.
        PermissionError: If the file cannot be written.
    """
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
 
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname] + friends)
 
    except FileNotFoundError:
        print(f"Sorry, could not save the network: the path '{filename}' was not found.")
        raise
    except Exception as error:
        print(f"Sorry, could not save the network to '{filename}': {error}")
        raise
 
 
def load_network(filename: str) -> dict:
    """
    Part e)
    Loads a social network from a CSV file created by save_network().
 
    Args:
        filename: The name of the CSV file to read.
 
    Returns:
        The social network dictionary.
 
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a row in the file is missing a username or full name.
    """
    try:
        sn = {}
 
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
 
            for row in reader:
                if len(row) < 2:
                    raise ValueError(f"Invalid row in file: {row}")
 
                sn[row[0]] = (row[1], row[2:])
 
        return sn
 
    except FileNotFoundError:
        print(f"Sorry, could not load the network: the file '{filename}' was not found.")
        raise
    except Exception as error:
        print(f"Sorry, could not load the network from '{filename}': {error}")
        raise
 
 
def main() -> None:
    """
    Part f)
    Creates the example social network and tests all the functions.
    """
    try:
        sn = {
            'alice': ('Alice Smith', ['maria']),
            'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
            'joe': ('Joseph Adams', ['maria', 'eve']),
            'eve': ('Evelyn Cooper', ['joe']),
            'david': ('David Benson', ['maria'])
        }
 
        # Tests add_user
        print(add_user(sn, 'john', 'John Brown'))    # True
        print(add_user(sn, 'john', 'John Brown'))    # False (already exists)
 
        # Tests add_friend
        print(add_friend(sn, 'john', 'alice'))       # True
        print(add_friend(sn, 'john', 'nobody'))      # False (user not found)
 
        # Tests get_friends
        print(get_friends(sn, 'alice', 1))           # ['maria', 'john']
        print(get_friends(sn, 'alice', 2))           # ['maria', 'john', 'joe', 'david']
        print(get_friends(sn, 'nobody', 1))          # []
 
        # Tests save_network and load_network
        save_network('network.csv', sn)
        loaded = load_network('network.csv')
        print(loaded == sn)                          # True (same network after reload)
 
        # Tests the exceptions
        try:
            load_network('test_missing_file.csv')
        except FileNotFoundError:
            print("FileNotFoundError was raised as expected")
 
        try:
            save_network('test_raise_error/network.csv', sn)
        except FileNotFoundError:
            print("FileNotFoundError was raised as expected")
 
    except Exception as error:
        print(f"Sorry, the program could not run: {error}")
        raise
 
 
if __name__ == "__main__":
    main()