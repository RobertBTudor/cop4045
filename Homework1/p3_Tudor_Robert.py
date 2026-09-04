# Part a) the function works by slicing the string into n sized pieces. For each slice (substring), 
# The nested loop will iterate through the rest of the string, without overlap
# Slicing it in n sized pieces to see if there is a matching substring, and returns it.
# If there are no duplicated substrings it returns empty string
def find_dup_str(s, n):
    for i in range(len(s)-n+1):
        substring = s[i:i+n]
        
        for j in range(i+n, len(s)-n+1):
            if s[j:j+n] == substring:
                return substring
    return ""
             
# Part b) This function finds the largest duplicate substring in a string
# It works by iterating through the string, and calling the find_dup_str function, increasing n each time
# It compares the current substring to the largest, then saves the larger one in max_substring and returns it.
def find_max_dup(s):
    max_substring = ""
    for i in range(1, len(s)+1):
        substring = find_dup_str(s, i)
        if len(substring) > len(max_substring):
            max_substring = substring
    return max_substring

s = input("Enter string: ")
num = int(input("Enter substring size: "))
print(find_dup_str(s, num))
print(find_max_dup(s))
