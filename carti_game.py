import tkinter as tk

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5
JUMP_HEIGHT = 15
GRAVITY = 0.8

# Platform settings
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 20

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Playboi Carti Platformer")
        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='black')
        self.canvas.pack()

        self.player_parts = []
        # Head
        head = self.canvas.create_oval(100, SCREEN_HEIGHT - PLAYER_HEIGHT - 100, 100 + PLAYER_WIDTH, SCREEN_HEIGHT - PLAYER_HEIGHT - 100 + PLAYER_WIDTH, fill='peachpuff', outline='black')
        self.player_parts.append(head)
        # Body
        body = self.canvas.create_rectangle(110, SCREEN_HEIGHT - PLAYER_HEIGHT - 100 + PLAYER_WIDTH, 140, SCREEN_HEIGHT - 100, fill='pink', outline='black')
        self.player_parts.append(body)
        # Arms
        arm1 = self.canvas.create_line(110, SCREEN_HEIGHT - PLAYER_HEIGHT - 100 + PLAYER_WIDTH + 10, 100, SCREEN_HEIGHT - PLAYER_HEIGHT - 100 + PLAYER_WIDTH + 20, fill='peachpuff', width=3)
        self.player_parts.append(arm1)
        arm2 = self.canvas.create_line(140, SCREEN_HEIGHT - PLAYER_HEIGHT - 100 + PLAYER_WIDTH + 10, 150, SCREEN_HEIGHT - PLAYER_HEIGHT - 100 + PLAYER_WIDTH + 20, fill='peachpuff', width=3)
        self.player_parts.append(arm2)
        # Legs
        leg1 = self.canvas.create_line(115, SCREEN_HEIGHT - 100, 115, SCREEN_HEIGHT - 80, fill='blue', width=3)
        self.player_parts.append(leg1)
        leg2 = self.canvas.create_line(135, SCREEN_HEIGHT - 100, 135, SCREEN_HEIGHT - 80, fill='blue', width=3)
        self.player_parts.append(leg2)
        # Hair (long wavy)
        hair = self.canvas.create_arc(95, SCREEN_HEIGHT - PLAYER_HEIGHT - 100 - 10, 155, SCREEN_HEIGHT - PLAYER_HEIGHT - 100 + 10, start=0, extent=180, fill='black', outline='black')
        self.player_parts.append(hair)

        self.platforms = []
        # Ground
        ground = self.canvas.create_rectangle(0, SCREEN_HEIGHT - 50, PLATFORM_WIDTH, SCREEN_HEIGHT - 50 + PLATFORM_HEIGHT, fill='blue')
        self.platforms.append(ground)

        # Platform 1
        platform1 = self.canvas.create_rectangle(300, SCREEN_HEIGHT - 150, 300 + PLATFORM_WIDTH, SCREEN_HEIGHT - 150 + PLATFORM_HEIGHT, fill='blue')
        self.platforms.append(platform1)

        # Platform 2
        platform2 = self.canvas.create_rectangle(500, SCREEN_HEIGHT - 250, 500 + PLATFORM_WIDTH, SCREEN_HEIGHT - 250 + PLATFORM_HEIGHT, fill='blue')
        self.platforms.append(platform2)

        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

        self.root.bind('<KeyPress>', self.key_press)
        self.root.bind('<KeyRelease>', self.key_release)

        self.update()

    def key_press(self, event):
        if event.keysym == 'w' and self.on_ground:
            self.vel_y = -JUMP_HEIGHT
        elif event.keysym == 'a':
            self.vel_x = -PLAYER_SPEED
        elif event.keysym == 'd':
            self.vel_x = PLAYER_SPEED

    def key_release(self, event):
        if event.keysym in ('a', 'd'):
            self.vel_x = 0

    def update(self):
        # Gravity
        if not self.on_ground:
            self.vel_y += GRAVITY

        # Move
        for part in self.player_parts:
            self.canvas.move(part, self.vel_x, self.vel_y)

        # Get player coords (using body)
        x1, y1, x2, y2 = self.canvas.coords(self.player_parts[1])

        # Check collisions
        self.on_ground = False
        for p in self.platforms:
            px1, py1, px2, py2 = self.canvas.coords(p)
            if x2 > px1 and x1 < px2:
                if y2 > py1 and y1 < py2:
                    if self.vel_y > 0:  # falling
                        dy = py1 - y2
                        for part in self.player_parts:
                            self.canvas.move(part, 0, dy)
                        self.on_ground = True
                        self.vel_y = 0
                    elif self.vel_y < 0:  # jumping
                        dy = py2 - y1
                        for part in self.player_parts:
                            self.canvas.move(part, 0, dy)
                        self.vel_y = 0

        # Keep on screen
        x1, y1, x2, y2 = self.canvas.coords(self.player_parts[1])
        if x1 < 0:
            dx = -x1
            for part in self.player_parts:
                self.canvas.move(part, dx, 0)
        if x2 > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - x2
            for part in self.player_parts:
                self.canvas.move(part, dx, 0)
        if y1 < 0:
            dy = -y1
            for part in self.player_parts:
                self.canvas.move(part, 0, dy)
        if y2 > SCREEN_HEIGHT:
            dy = SCREEN_HEIGHT - y2
            for part in self.player_parts:
                self.canvas.move(part, 0, dy)
            self.on_ground = True
            self.vel_y = 0

        self.root.after(16, self.update)  # ~60 FPS

def main():
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()