# Copyright 2017, 2013, 2011 Pearson Education, Inc., W.F. Punch & R.J.Enbody
"""Predator-Prey Simulation
five classes are defined: animal, predator, prey, human, and island
where island is where the simulation is taking place,
i.e. where the predator and prey interact (live).
A list of predators and prey are instantiated, and
then their breeding, eating, and dying are simulted.
"""
import random
import time
#import pylab # replaced by:
import matplotlib.pyplot as plt


class Island (object):
    """Island
       n X n grid where zero value indicates not occupied."""
    def __init__(self, n: int, prey_count: int = 0, predator_count: int = 0, count_humans: int = 0) -> None:
        '''Initialize grid to all 0's, then fill with animals

        Parameters: n - grid size; prey_count, predator_count, count_humans - starting animals
        Precondition: the total animal count fits on the n x n grid
        '''
        # print(n,prey_count,predator_count)
        self.grid_size = n
        self.grid = []
        for i in range(n):
            row = [0]*n    # row is a list of n zeros
            self.grid.append(row)
        self.init_animals(prey_count,predator_count,count_humans)

    def init_animals(self, prey_count: int, predator_count: int, count_humans: int) -> None:
        ''' Put some initial animals on the island

        Parameters: prey_count, predator_count, count_humans - how many of each to place
        Postcondition: the animals are placed in random empty cells
        '''
        count = 0
        # while loop continues until prey_count unoccupied positions are found
        while count < prey_count:
            x = random.randint(0,self.grid_size-1)
            y = random.randint(0,self.grid_size-1)
            if not self.animal(x,y):
                new_prey=Prey(island=self,x=x,y=y)
                count += 1
                self.register(new_prey)
        count = 0
        # same while loop but for predator_count
        while count < predator_count:
            x = random.randint(0,self.grid_size-1)
            y = random.randint(0,self.grid_size-1)
            if not self.animal(x,y):
                new_predator=Predator(island=self,x=x,y=y)
                count += 1
                self.register(new_predator)
        count = 0
        # same while loop but for count_humans
        while count < count_humans:
            x = random.randint(0,self.grid_size-1)
            y = random.randint(0,self.grid_size-1)
            if not self.animal(x,y):
                new_human=Human(island=self,x=x,y=y)
                count += 1
                self.register(new_human)

    def clear_all_moved_flags(self) -> None:
        ''' Animals have a moved flag to indicated they moved this turn.
        Clear that so we can do the next turn
        '''
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        '''Return size of the island: one dimension.
        '''
        return self.grid_size

    def register(self, animal: 'Animal') -> None:
        '''Register animal with island, i.e. put it at the
        animal's coordinates
        '''
        x = animal.x
        y = animal.y
        self.grid[x][y] = animal

    def remove(self, animal: 'Animal') -> None:
        '''Remove animal from island.'''
        x = animal.x
        y = animal.y
        self.grid[x][y] = 0

    def animal(self, x: int, y: int) -> 'Animal | int':
        '''Return animal at location (x,y), 0 if empty, -1 if off the island'''
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        else:
            return -1  # outside island boundary

    def __str__(self) -> str:
        '''String representation for printing.
           (0,0) will be in the lower left corner.
        '''
        s = ""
        for j in range(self.grid_size-1,-1,-1):  # print row size-1 first
            for i in range(self.grid_size):      # each row starts at 0
                if not self.grid[i][j]:
                    # print a '.' for an empty space
                    s+= "{:<2s}".format('.' + "  ")
                else:
                    s+= "{:<2s}".format((str(self.grid[i][j])) + "  ")
            s+="\n"
        return s

    def count_prey(self) -> int:
        ''' count all the prey on the island'''
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x,y)
                if animal:
                    if isinstance(animal,Prey):
                        count+=1
        return count

    def count_predators(self) -> int:
        ''' count all the predators on the island'''
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x,y)
                if animal:
                    if isinstance(animal,Predator) and not isinstance(animal,Human):
                        count+=1
        return count

    def count_humans(self) -> int:
        ''' count all the humans on the island'''
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x,y)
                if animal:
                    if isinstance(animal,Human):
                        count+=1
        return count


class Animal(object):
    """An animal on the island that can move and breed"""

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "A") -> None:
        '''Create an animal at (x,y)

        Parameters: island - the island it lives on; x, y - its position; s - its symbol
        '''
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved=False

    def position(self) -> tuple[int, int]:
        '''Return coordinates of current position.
        '''
        return self.x, self.y

    def __str__(self) -> str:
        '''Return the animal's symbol'''
        return self.name

    def check_grid(self, type_looking_for: type = int) -> tuple[int, int] | int:
        ''' Look in the 8 directions from the animal's location
        and return the first location that presently has an object
        of the specified type. Return 0 if no such location exists

        Parameters: type_looking_for - the exact type to find (int means an empty cell)
        '''
        # neighbor offsets
        offset = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]
        result = 0
        for i in range(len(offset)):
            x = self.x + offset[i][0]  # neighboring coordinates
            y = self.y + offset[i][1]
            if not 0 <= x < self.island.size() or \
               not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x,y))==type_looking_for:
                result=(x,y)
                break
        return result

    def move(self) -> None:
        '''Move to an open, neighboring position '''
        if not self.moved:
            location = self.check_grid(int)
            if location:
                # print('Move, {}, from {},{} to {},{}'.format( \
                #     type(self),self.x,self.y,location[0],location[1]))
                self.island.remove(self)   # remove from current spot
                self.x = location[0]       # new coordinates
                self.y = location[1]
                self.island.register(self) # register new coordinates
                self.moved=True

    def breed(self) -> None:
        ''' Breed a new Animal.If there is room in one of the 8 locations
        place the new Prey there. Otherwise you have to wait.

        Precondition: the subclass sets breed_clock and breed_time
        '''
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                # print('Breeding Prey {},{}'.format(self.x,self.y))
                the_class = self.__class__
                new_animal = the_class(self.island,x=location[0],y=location[1])
                self.island.register(new_animal)

    def clear_moved_flag(self) -> None:
        '''Reset the moved flag for the next turn'''
        self.moved=False


class Prey(Animal):
    """Prey just moves and breeds"""

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "O") -> None:
        '''Create a prey at (x,y) and start its breed clock

        Parameters: island, x, y, s - same as Animal
        Precondition: Prey.breed_time is set in main
        '''
        Animal.__init__(self,island,x,y,s)
        self.breed_clock = self.breed_time
        # print('Init Prey {},{}, breed:{}'.format(self.x, self.y,self.breed_clock))

    def clock_tick(self) -> None:
        '''Prey only updates its local breed clock
        '''
        self.breed_clock -= 1
        # print('Tick Prey {},{}, breed:{}'.format(self.x,self.y,self.breed_clock))


class Predator(Animal):
    """A predator eats prey and dies if it starves"""

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "X") -> None:
        '''Create a predator at (x,y) and start its breed and starve clocks

        Parameters: island, x, y, s - same as Animal
        Precondition: breed_time and starve_time are set in main
        '''
        Animal.__init__(self,island,x,y,s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time
        # print('Init Predator {},{}, starve:{}, breed:{}'.format( \
        #     self.x,self.y,self.starve_clock,self.breed_clock))

    def clock_tick(self) -> None:
        ''' Predator updates both breeding and starving

        Postcondition: the predator is removed from the island if it starved
        '''
        self.breed_clock -= 1
        self.starve_clock -= 1
        # print('Tick, Predator at {},{} starve:{}, breed:{}'.format( \
        #     self.x,self.y,self.starve_clock,self.breed_clock))
        if self.starve_clock <= 0:
            # print('Death, Predator at {},{}'.format(self.x,self.y))
            self.island.remove(self)

    def hunt(self, food_type: type) -> None:
        '''Look for one of the 8 locations with a food_type animal. If found
        move to that location, remove the food and reset the starve clock

        Parameters: food_type - the class of animal to eat
        Precondition: the predator has not moved this turn
        '''
        location = self.check_grid(food_type)
        if location:
            # print('Eating: pred at {},{}, prey at {},{}'.format( \
            #     self.x,self.y,location[0],location[1]))
            self.island.remove(self.island.animal(location[0],location[1]))
            self.island.remove(self)
            self.x=location[0]
            self.y=location[1]
            self.island.register(self)
            self.starve_clock=self.starve_time
            self.moved=True

    def eat(self) -> None:
        '''Predator hunts for Prey if it hasn't moved yet this turn'''
        if not self.moved:
            self.hunt(Prey)


class Human(Predator):
    """A human is a predator that hunts predators every hunt_time ticks and does not kill prey"""

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "H") -> None:
        '''Create a human at (x,y) and start its breed, starve and hunt clocks

        Parameters: island - the island it lives on; x, y - its position; s - its symbol
        Precondition: Human.breed_time, starve_time and hunt_time are set in main
        '''
        super().__init__(island,x,y,s)
        self.hunt_clock = self.hunt_time

    def clock_tick(self) -> None:
        '''Update the breed, starve and hunt clocks

        Postcondition: the human is removed from the island if it starved
        '''
        self.hunt_clock -= 1
        super().clock_tick()

    def eat(self) -> None:
        '''Every hunt_time ticks, hunt for a Predator next to the human

        Postcondition: the hunt clock is reset when it is time to hunt
        '''
        if not self.moved and self.hunt_clock <= 0:
            self.hunt_clock = self.hunt_time
            self.hunt(Predator)


###########################################
def main(predator_breed_time: int = 6, predator_starve_time: int = 3, initial_predators: int = 10,
         prey_breed_time: int = 3, initial_prey: int = 50,
         human_breed_time: int = 10, human_starve_time: int = 15, human_hunt_time: int = 2,
         initial_humans: int = 5,
         size: int = 10, ticks: int = 1000, stable_ticks: int = 20) -> None:
    ''' main simulation. Sets defaults, runs event loop, plots at the end

    Parameters: breed, starve and hunt times and starting counts for each animal,
                the island size, the max number of ticks to run and how many ticks
                in a row all three populations must stay the same to count as converged
    Postcondition: the island is printed at the start and end, and the populations are plotted
    '''
    # initialization values
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    # for graphing
    predator_list=[]
    prey_list=[]
    human_list=[]

    # make an island
    isle = Island(size,initial_prey, initial_predators, initial_humans)
    print('Island at the start:')
    print(isle)

    # number of ticks in a row that no population has changed
    unchanged = 0

    # event loop.
    #   For all the ticks, for every x,y location.
    #   If there is an animal there, try eat, move, breed and clock_tick
    for i in range(ticks):
        # important to clear all the moved flags!
        isle.clear_all_moved_flags()
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x,y)
                if animal:
                    if isinstance(animal,Predator):
                        animal.eat()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()

        # record info for display, plotting
        prey_count = isle.count_prey()
        predator_count = isle.count_predators()
        human_count = isle.count_humans()

        # check if all three populations are the same as the last tick
        if i > 0 and prey_count == prey_list[-1] and \
           predator_count == predator_list[-1] and human_count == human_list[-1]:
            unchanged += 1
        else:
            unchanged = 0

        prey_list.append(prey_count)
        predator_list.append(predator_count)
        human_list.append(human_count)
        # print out every 10th cycle, see what's going on
        if not i%10:
            print(prey_count, predator_count, human_count)

        # stop once the populations have converged to constant values
        if unchanged >= stable_ticks:
            print('Populations converged after', i+1, 'ticks. Stopping.')
            break
        # print the island, hold at the end of each cycle to get a look
        # print('*'*20)
        # print(isle)
        # ans = input("Return to continue")

    print('Island at the end:')
    print(isle)

    # plot all three populations over time
    plt.plot(predator_list, label='Predators')
    plt.plot(prey_list, label='Prey')
    plt.plot(human_list, label='Humans')
    plt.xlabel('Time (ticks)')
    plt.ylabel('Population')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main(predator_starve_time=8, predator_breed_time=4,
     human_hunt_time=6, human_starve_time=30, human_breed_time=15, initial_humans=3)


