#Part a) -----------------------------------
#iterate through all combinations of abcd from 1 to 10, keeping only distinct sets of four integers where a^2 + b^2 equals c^2 + d^2
solutions = [ (a, b, c, d) 
             for a in range(1, 11) 
             for b in range(1, 11) 
             for c in range(1, 11) 
             for d in range(1, 11) 
             if len({a, b, c, d}) == 4 and a**2 + b**2 == c**2 + d**2 
             ] 
print(solutions)

#Part b) -----------------------------------
#Filter strings in words with fewer than 5 characters and convert each matching word to a (lowercase, length) tuple

words = ['One', 'SEVEN', 'three', 'two', 'Ten'] 
result = [(word.lower(), len(word)) for word in words if len(word) < 5] 
print(result)

#Part c) -----------------------------------
#Split each full name into components and format them using the first, middle initial, and last name
names = ["Christopher Ashton Kutcher", "Elizabeth Stamina Fey"]
formatted_names = [ f"{first} {middle[0]}. {last}" for first, middle, last in (name.split() for name in names)]
print (formatted_names)

#Part d) -----------------------------------
# Compare every pair of words from lst1 and lst2, if their lowercase characters are identical when sorted = anagram
lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

anagrams = [
    (w1, w2)
    for w1 in lst1
    for w2 in lst2
    if sorted(w1.lower()) == sorted(w2.lower())
]
print(anagrams)

#Part e) -----------------------------------
# Create a dictionary mapping each string from s to its key value length pair
s = ['one', 'two', 'three']

length_dict = {word: len(word) for word in s}
print(length_dict)

#Part f) -----------------------------------
# Enumerate text to collect indexs and character values as key value pairs for letters that are vowels.
text = "Hello world"

vowel_dict = {
    idx: char
    for idx, char in enumerate(text)
    if char.lower() in "aeiou"
}
print(vowel_dict)

