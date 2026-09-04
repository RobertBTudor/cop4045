#Tries all posible combinations for a,b,c from 1 to n (inclusive). If it satisfies the pythagorean theorm it gets appended to the list as a tuple. 
def find_Pythagorean(n):
    triples = []
    
    for a in range(1, n+1):
        for b in range(1, n+1):
            for c in range(1, n+1):
                if a**2 + b**2 == c**2:
                        triples.append((a,b,c))
    return triples

user_n = int(input("Enter a value n: "))
print(find_Pythagorean(user_n))