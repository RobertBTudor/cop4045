# Part a) the function works by slicing the string into n sized pieces. For each slice (substring), 
# The nested loop will iterate through the rest of the strin, slicing it in n sized pieces to see if there is a matching substring.
# If there are no duplicated substrings it returns no duplicated substrings found
def find_dup_strs(s, n):
    for i in range(len(s)-n+1):
        substring = s[i:i+n]
        
        for j in range(i+1, len(s)-n+1):
            if s[j:j+n] == substring:
                return substring
    return "No duplicated substrings found"
             
string = input("Enter string: ")
num = int(input("Enter substring size: "))
print(find_dup_strs(string, num))