import pgzrun
import math
import random

WIDTH = 800

HEIGHT = 600

game_state = 'MENU'

coins = []

button_start = Rect(300, 300, 200, 50)
button_sound = Rect(300, 370, 200, 50)
button_exit = Rect(300, 440, 200, 50)

sound_on = True
music.play('tema')



class AnimatedActor(Actor):
    def __init__(self,idle_images,move_images,pos):
        super().__init__(idle_images[0], pos)
        self.idle_frames = idle_images
        self.move_frames = move_images
        self.frame_timer = 0.0
        self.current_frame = 0
        self.target_pos = list(pos)
        self.is_moving = False
    def update_animation(self):
        if self.is_moving == True:
            active_frames = self.move_frames
        else:
            active_frames = self.idle_frames
        self.frame_timer += 1
        if self.frame_timer > 10:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(active_frames):
                self.current_frame = 0
        self.image = active_frames[self.current_frame]
    def move_towards(self, speed):
        dx =  self.target_pos[0] - self.x 
        dy =  self.target_pos[1] - self.y
        distance = math.hypot(dx,dy)
        if distance > speed:
            self.is_moving = True
            angle = math.atan2(dy,dx)
            self.x += math.cos(angle) * speed
            self.y += math.sin(angle) * speed
        else:
            self.is_moving = False

class Enemy(AnimatedActor):
    def __init__(self, idle_images, move_images, pos):
        super().__init__(idle_images, move_images, pos)
        self.vision_radius = 200
    def update_ai(self, target):
        dx = target.x - self.x 
        dy = target.y - self.y 
        distance = math.hypot(dx,dy)
        if distance < self.vision_radius:
            self.target_pos = [target.x,target.y]
            self.move_towards(2)
        else:
            self.is_moving = False


def draw():
    if game_state == 'MENU':
        screen.fill((0,0,0))
        screen.draw.text("MENU", center=(400, 200), color="white", fontsize=60)
        screen.draw.filled_rect(button_start, "green")
        screen.draw.text("START", center=button_start.center, color="black")
        screen.draw.filled_rect(button_exit, "green")
        screen.draw.text("EXIT", center=button_exit.center, color="black")
        screen.draw.filled_rect(button_sound, "green")
        screen.draw.text("SOUND", center=button_sound.center, color="black")
    elif game_state == 'GAME':
        screen.fill((0,191,255))
        hero.draw()
        monster.draw()
        for coin in coins:
            coin.draw()

hero = AnimatedActor(['hero_idle_1','hero_idle_2'],['hero_move_1','hero_move_2'],(400,300))

monster = Enemy(['monster_idle_1','monster_idle_2'],['monster_move_1','monster_move_2'],(200,200))

coin = Actor('coin_image', (600, 400))

def restat_level():
    hero.pos = (400, 300)
    hero.target_pos = [400, 300]
    monster.pos = (200, 200)
    monster.target_pos = [200, 200]
    coins.clear()
    for i in range(5):
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        coins.append(Actor('coin_image', (x, y)))


def update():
    global game_state
    if game_state == 'GAME':
        hero.update_animation()
        hero.move_towards(3)
        monster.update_ai(hero)
        monster.update_animation()
        for coin in coins:
            if hero.colliderect(coin):
                coins.remove(coin)
        if len(coins) == 0:
            game_state = 'MENU'
            restat_level()
        if hero.colliderect(monster):
            game_state = 'MENU'
            restat_level()

def on_mouse_down(pos, button):
    global game_state
    global sound_on
    if game_state == 'MENU':
        if button_start.collidepoint(pos): game_state = 'GAME'
        elif button_exit.collidepoint(pos): exit()
        elif button_sound.collidepoint(pos): 
            sound_on = not sound_on
            if sound_on:
                music.unpause()
            else:
                music.pause()
       

    elif game_state == 'GAME':
        hero.target_pos = list(pos)
        sounds.click.play()


restat_level()
pgzrun.go()