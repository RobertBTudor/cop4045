import math

#Continuous loop that runs until the break condition (triggered by the user pressing enter key for coeficcient a)
while True:
    a = input("Enter value for a: ")
    if a == "":
        break

    b = input("Enter value for b: ")
    c = input("Enter value for c: ")

    a = float(a)
    b = float(b)
    c = float(c)

    if ((b**2) - (4*a*c)) < 0:
        print("no real solutions")

    elif ((b**2) - (4*a*c)) == 0:
        x1 = (-b + math.sqrt((b**2) - (4*a*c))) / (2*a) 
        print("one real solution:", x1)

    elif ((b**2) - (4*a*c)) > 0:
        x1 = (-b + math.sqrt((b**2) - (4*a*c))) / (2*a) 
        x2 = (-b - math.sqrt((b**2) - (4*a*c))) / (2*a) 
        print("Two real solutions: ", x1, " and ", x2)



