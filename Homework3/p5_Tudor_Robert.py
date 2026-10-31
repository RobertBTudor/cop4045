import turtle


def draw_leaf_straight(level: int, length: float) -> None:
    """Draw a recursive leaf,

    Parameters: level - the recursion level; length - the length of the lower stem
    Precondition: level >= 0 and length > 0
    Postcondition: the turtle ends where it started, facing the same way
    """
    turtle.forward(length)
    if level > 0:
        turtle.left(45)
        draw_leaf_straight(level - 1, length * 0.35)
        turtle.right(90)
        draw_leaf_straight(level - 1, length * 0.35)
        turtle.left(45)
        draw_leaf_straight(level - 1, length * 0.85)
    turtle.backward(length)

def draw_leaf_curved(level: int, length: float) -> None:
    """Draw a recursive leaf that bends 15 degrees right at each level

    Parameters: level - the recursion level; length - the length of the lower stem
    Precondition: level >= 0 and length > 0
    Postcondition: the turtle ends where it started, facing the same way
    """
    turtle.forward(length)
    if level > 0:
        turtle.left(45)
        draw_leaf_curved(level - 1, length * 0.35)
        turtle.right(90)
        draw_leaf_curved(level - 1, length * 0.35)
        turtle.left(45)
        turtle.right(15)
        draw_leaf_curved(level - 1, length * 0.85)
        turtle.left(15)
    turtle.backward(length)



def setup_turtle() -> None:
    """Turn off the animation delay and move the turtle to the bottom, facing up"""
    turtle.delay(0)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.up()
    turtle.goto(0, -320)
    turtle.left(90)
    turtle.down()


def main() -> None:
    """Draw the leaf"""
    setup_turtle()
    draw_leaf_curved(6, 120)
    turtle.done()


if __name__ == '__main__':
    main()
    