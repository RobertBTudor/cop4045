import math
import matplotlib.pyplot as plt

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

    #--- Creating the graph ---
    #Creates the chart using matplotlib. First sort by the amount of roots to choose the domain size (xmin/xmax),
    #Then creates a graph using 150 points. I customized the graph to show all 150 points and made them less thick (similar to the example)
    if ((b**2) - (4*a*c)) > 0:
        xmin = x1 - 5
        xmax = x2 + 5

    elif ((b**2) - (4*a*c)) == 0:
        xmin = x1 - 5
        xmax = x1 + 5

    else:
        xopt = -b / (2*a)
        xmin = xopt - 5
        xmax = xopt + 5

    x = [xmin + i * (xmax - xmin) / 149 for i in range(150)]

    y = []
    for value in x:
        y.append(a * value**2 + b * value + c)

    plt.plot(x, y, "o-", markersize = 2)
    plt.axhline(0)
    plt.show()