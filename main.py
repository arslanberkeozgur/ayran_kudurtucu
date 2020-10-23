import pygame
import random

pygame.mixer.init()

WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load('ayran.jpg'), (WIDTH, HEIGHT))
KITTY = pygame.transform.scale(pygame.image.load('cat.png'), (30, 30))

meow1 = pygame.mixer.Sound('meow1.wav')
meow2 = pygame.mixer.Sound('meow2.wav')
meow3 = pygame.mixer.Sound('meow3.wav')
meow4 = pygame.mixer.Sound('meow4.wav')
meow5 = pygame.mixer.Sound('meow5.wav')
meow6 = pygame.mixer.Sound('meow6.wav')

meows = [meow1, meow2, meow3, meow4, meow5, meow6]

pygame.display.set_caption('Snake')
GRID = 40
FPS = 15
clock = pygame.time.Clock()


class Snake:
    part_count = 1


    def __init__(self):
        self.coordinates = [[380, 380]]

    def draw(self):
        for i in range(self.part_count):
            pygame.draw.rect(WIN,(240,0,0), (int(self.coordinates[i][0]), int(self.coordinates[i][1]), int(WIDTH / GRID), int(HEIGHT / GRID)))

    def move(self):
        vx = 0
        vy = 0
        if UP:
            vx = 0
            vy = -1
        elif DOWN:
            vx = 0
            vy = 1
        elif RIGHT:
            vx = 1
            vy = 0
        elif LEFT:
            vx = -1
            vy = 0
        if self.part_count > 1:
            for i in range(1, self.part_count):
                self.coordinates[self.part_count - i] = self.coordinates[self.part_count - (i + 1)].copy()
        self.coordinates[0][0] += vx * (WIDTH / GRID)
        self.coordinates[0][1] += vy * (HEIGHT / GRID)

        if self.coordinates[0][0] > WIDTH:
            self.coordinates[0][0] = 0
        if self.coordinates[0][0] < 0:
            self.coordinates[0][0] = WIDTH
        if self.coordinates[0][1] > HEIGHT:
            self.coordinates[0][1] = 0
        if self.coordinates[0][1] < 0:
            self.coordinates[0][1] = HEIGHT


    def grow(self):
        self.coordinates.append([self.coordinates[self.part_count - 1][0], self.coordinates[self.part_count - 1][1]])
        self.part_count += 1


    def check_death(self):
        if self.part_count >= 5:
            for i in range(1, self.part_count):
                if self.coordinates[0] == self.coordinates[i]:
                    pygame.time.delay(1000)
                    self.coordinates = [[380, 380]]
                    self.part_count = 1
                    for i in range(3):
                        self.grow()
                    return

    def get_kitty(self, obj):
        coord = [self.coordinates[0][0] + 10, self.coordinates[0][1] + 10]
        if int(((obj.x + 15 - coord[0])**2 + (obj.y + 15 - coord[1])**2)**0.5) < 20:
            meow = random.choice(meows)
            meow.play()
            return True


class Kitty:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        WIN.blit(KITTY, (self.x, self.y))


snake = Snake()
kitty = []


def main():
    run = True
    cat_on_screen = False
    global UP
    global DOWN
    global RIGHT
    global LEFT
    UP = False
    DOWN = False
    RIGHT = False
    LEFT = False


    def draw():
        WIN.blit(BG, (0,0))
        snake.draw()
        for cat in kitty:
            cat.draw()
        pygame.display.update()

    for i in range(3):
        snake.grow()

    while run:
        clock.tick(FPS)

        if not cat_on_screen:
            cat = Kitty(random.randrange(40, WIDTH - 40), random.randrange(40, HEIGHT - 40))
            kitty.append(cat)
            cat_on_screen = True

        snake.move()

        for cat in kitty:
            if snake.get_kitty(cat):
                kitty.remove(cat)
                snake.grow()
                cat_on_screen = False

        snake.check_death()

        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not RIGHT:
                        LEFT = True
                        UP = False
                        DOWN = False
                if event.key == pygame.K_UP:
                    if not DOWN:
                        UP = True
                        RIGHT = False
                        LEFT = False
                if event.key == pygame.K_RIGHT:
                    if not LEFT:
                        RIGHT = True
                        DOWN = False
                        UP = False
                if event.key == pygame.K_DOWN:
                    if not UP:
                        DOWN = True
                        LEFT = False
                        RIGHT = False


main()




