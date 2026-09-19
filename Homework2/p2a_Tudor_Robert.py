solutions = [ (a, b, c, d) for a in range(1, 11) 
             for b in range(1, 11) 
             for c in range(1, 11) 
             for d in range(1, 11) 
             if len({a, b, c, d}) == 4 and a**2 + b**2 == c**2 + d**2 
             ] 

print(solutions)