import turtle as t
import random

# Setup
t.setup(900, 300)
t.tracer(0, 0)
t.hideturtle()
t.penup()

# Game State Flag
game_over = False

# Initial positions
bx = -300
by = 0
pu1x = 300 # Initial X position of the pipe set

# Bird properties
bird_velocity = 0
gravity = -0.5
jump_strength = 10
bird_radius = 15

# Pipe properties
pipe_width = 40
pipe_height = 90
gap_size = 100

# The bottom limit of the screen/ground for collision reference
GROUND_Y = -140
CEILING_Y = 140

def bird():
    global bird_velocity, by, game_over
    
    if not game_over:
        bird_velocity += gravity
        by += bird_velocity
        
        # Ground collision
        if by <= GROUND_Y + bird_radius:
            by = GROUND_Y + bird_radius
            bird_velocity = 0
            game_over = True
        
        # Ceiling collision
        if by >= CEILING_Y - bird_radius:
            by = CEILING_Y - bird_radius
            bird_velocity = 0
            game_over = True

    # Draw bird
    t.goto(bx, by - bird_radius) # Position Y at bottom edge for circle center
    t.pendown()
    t.fillcolor("yellow")
    t.begin_fill()
    t.circle(bird_radius)
    t.end_fill()
    t.penup()

def jump(x=0, y=0):
    global bird_velocity, game_over
    if not game_over:
        bird_velocity = jump_strength

def draw_rect_pipe(px, py_top_left, height):
    """Generic function to draw a single pipe rectangle downwards from top-left corner."""
    t.goto(px, py_top_left)
    t.setheading(0)
    t.pendown()
    t.fillcolor("green")
    t.begin_fill()
    t.forward(pipe_width)
    t.right(90)
    t.forward(height)
    t.right(90)
    t.forward(pipe_width)
    t.right(90)
    t.forward(height)
    t.end_fill()
    t.penup()

def twopipes(px, upper_pipe_bottom_y):
    """Draw both pipes based on the Y coordinate where the gap starts."""
    # The 'upper_pipe_y' variable from your original code was actually the Y coordinate of the *top* of the pipe graphic.
    # The bottom of the upper graphic is the top of the gap.
    
    # Upper pipe starts drawing at the top of the gap, going up by pipe_height
    draw_rect_pipe(px, upper_pipe_bottom_y + pipe_height, pipe_height)
    
    # Lower pipe starts drawing below the gap, going down by pipe_height
    lower_pipe_top_y = upper_pipe_bottom_y - gap_size
    draw_rect_pipe(px, lower_pipe_top_y, pipe_height)


def check_pipe_collision():
    global bx, by, pu1x, upper_pipe_y, game_over, bird_radius
    
    pipe_left = pu1x
    pipe_right = pu1x + pipe_width
    
    # Calculate the Y boundaries of the gap
    gap_top_y = upper_pipe_y # This variable name is confusing, it's actually the bottom of the top pipe
    gap_bottom_y = upper_pipe_y - pipe_height - gap_size + pipe_height # Simplified: gap_top_y - gap_size

    # Check X-axis overlap
    if bx + bird_radius > pipe_left and bx - bird_radius < pipe_right:
        
        # Check Y-axis overlap
        # If the bird is above the gap top OR below the gap bottom, there is a collision
        if by + bird_radius > gap_top_y or by - bird_radius < gap_bottom_y:
            game_over = True
            return True
    return False

def update_game():
    global pu1x, upper_pipe_y, game_over
    
    if game_over:
        t.goto(0, 0)
        t.color("red")
        t.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
        t.update()
        return
    
    t.clear()
    
    pu1x -= 10
    
    if pu1x < -450:
        pu1x = 450
        # Random height for upper pipe *bottom* Y (where the gap starts)
        upper_pipe_y = random.randint(0, 100) # Restricted range to make lower pipes more reachable for testing
    
    # Pass the Y coordinate of where the gap should start
    twopipes(pu1x, upper_pipe_y)
    
    bird()
    
    check_pipe_collision()
    
    t.update()
    
    t.ontimer(update_game, 33)

# Initial random height for first pipe (Y coord of the bottom of the top pipe)
upper_pipe_y = random.randint(0, 100)

# Set up mouse click for jumping
t.onscreenclick(jump)

# Set up keyboard for jumping
t.listen()
t.onkeypress(jump, "space")
t.onkeypress(jump, "Up")

# Start the game loop
update_game()

t.mainloop()
