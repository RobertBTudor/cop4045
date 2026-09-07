import math
import matplotlib.pyplot as plt

# This function takes the function expression, domain, and number of samples
# It creates evenly spaced x values across the domain and evaluates the function
# at each x value, displays the x and y values in a table, and plots the function
def plot_function(fun_str, domain, ns):
    xmin, xmax = domain

    # Create exactly ns x values that are evenly distributed from xmin to xmax
    # xmin is first and xmax is last point so we use ns-1 intervals inbetween them
    xs = [xmin + i * (xmax - xmin) / (ns - 1) for i in range(ns)]

    #Evaluate the function for every x so that each x has a y value
    ys = []
    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    print(f"{'x':>8} {'y':>8}")
    print("-" * 25)

    #Print each x value together with its corresponding y value.
    for i in range(ns):
        print(f"{xs[i]:+10.4f} {ys[i]:+10.4f}")

    # Set up the plot and label it.
    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.show()

fun_str = input("Enter function with variable x: ")
ns = int(input("Enter number of samples: "))
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))

plot_function(fun_str, (xmin, xmax), ns)
