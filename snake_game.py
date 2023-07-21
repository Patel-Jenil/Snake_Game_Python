try:
    from tkinter import *
except ImportError: # python 2 
    from Tkinter import * # ignore warning

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100 # Initial Speed
SPACE_SIZE = 50
BODY_PARTS = 3 # Initial Body parts
SNAKE_HEAD_COLOR = "DARK GREEN"
SNAKE_COLOR = "#00FF00" # Green
FOOD_COLOR = "#FF0000" # Red
BACKGROUND_COLOR = "#000000" # Black


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(0, BODY_PARTS):
            self.coordinates.append((0, 0))

        for x, y in self.coordinates[:1]: # Make Head
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_HEAD_COLOR, tag="snake")
            self.squares.append(square)

        for x, y in self.coordinates[1:]: # Make remaining Body
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        global valid_food_index
        x, y = valid_food_index.pop()
        valid_food_index.add((x,y))
        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):

    global valid_food_index
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    if x < 0:
        x = GAME_WIDTH - SPACE_SIZE
    elif x >= GAME_WIDTH:
        x = 0
    if y < 0:
        y = GAME_HEIGHT - SPACE_SIZE
    elif y >= GAME_HEIGHT:
        y = 0
    canvas.itemconfig(snake.squares[0], fill=SNAKE_COLOR) # Changing the cuurent Head color to Body color 
    snake.coordinates.insert(0, (x, y))
    valid_food_index.discard((x,y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_HEAD_COLOR) # Adding new Head

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        valid_food_index.add((snake.coordinates[-1]))
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        mainWindow.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0] # Check Head if it's colliding with each other
    return (x,y) in snake.coordinates[1:]


def game_over():
    global new_game_button, exit_game_button
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/4, font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
    mainWindow.bind('<Return>', lambda event: new_game())
    new_game_button = Button(canvas, text="New Game", font=('consolas',20), foreground='red', bg='grey', relief='raised' ,command=new_game)
    new_game_button.place(relx=0.5, rely=0.4, anchor=CENTER)
    exit_game_button = Button(canvas, text="Quit", font=('consolas',20), foreground='red', bg='grey', relief='raised' ,command=exit_game)
    exit_game_button.place(relx=0.5, rely=0.5, anchor=CENTER)

def new_game():
    global score, canvas, direction, mainWindow, valid_food_index
    mainWindow.unbind("<Return>")
    canvas.delete("gameover")
    new_game_button.destroy()
    exit_game_button.destroy()
    valid_food_index = {(i,j) for i in range(0,GAME_WIDTH,SPACE_SIZE) for j in range(0,GAME_HEIGHT,SPACE_SIZE)}
    valid_food_index.discard((0,0))
    score = 0
    label.config(text="Score:{}".format(score))
    direction = 'down'
    snake = Snake()
    food = Food()

    next_turn(snake, food)

    mainWindow.mainloop()


def exit_game():
    mainWindow.destroy()
    mainWindow.quit()
    

if __name__ == '__main__':
    mainWindow = Tk()
    mainWindow.title("Snake game")
    mainWindow.resizable(False, False)

    score = 0
    direction = 'down'
    valid_food_index = set()
    label = Label(mainWindow, text="Score:{}".format(score), font=('consolas', 40))
    label.pack()

    canvas = Canvas(mainWindow, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    mainWindow.update()

    window_width = mainWindow.winfo_width()
    window_height = mainWindow.winfo_height()
    screen_width = mainWindow.winfo_screenwidth()
    screen_height = mainWindow.winfo_screenheight()

    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2)) - 35

    mainWindow.geometry(f"{window_width}x{window_height}+{x}+{y}")

    mainWindow.bind('<Left>', lambda event: change_direction('left'))
    mainWindow.bind('<Right>', lambda event: change_direction('right'))
    mainWindow.bind('<Up>', lambda event: change_direction('up'))
    mainWindow.bind('<Down>', lambda event: change_direction('down'))
    mainWindow.bind('<Return>', lambda event: new_game())
    mainWindow.bind('<Escape>', lambda event: exit_game())

    new_game_button = Button(canvas, text="New Game", font=('consolas',20), foreground='red', bg='grey', relief='raised' ,command=new_game)
    new_game_button.place(relx=0.5, rely=0.4, anchor=CENTER)
    exit_game_button = Button(canvas, text="Quit", font=('consolas',20), foreground='red', bg='grey', relief='raised' ,command=exit_game)
    exit_game_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    mainWindow.mainloop()