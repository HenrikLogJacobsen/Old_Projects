import pygame, os
from tkinter import *
import math


class Player:
    def __init__(self, rect_info):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.speed = 5
        self.playing = True

        self.width = -1
        self.height = -1
        scale = .2
        self.set_dim(rect_info, scale)

    def set_dim(self, dim_array, scale):
        self.width = round(dim_array[2] * scale)
        self.height = round(dim_array[3] * scale)

    def move_forward(self):
        self.x += int(self.speed * math.cos(((self.angle - 90)*math.pi)/180))
        self.y += int(self.speed * math.sin(((self.angle - 90)*math.pi)/180))


class SelectLevel:
    def __init__(self):
        self.level_root = Tk()
        self.level_root.title("DashGame")
        level_label = Label(self.level_root, text="Choose Level")
        level_label.grid(row=0, column=0)
        self.level_dir = StringVar(self.level_root)
        levels = os.listdir("data/")
        self.level_dir.set(levels[0])
        level_drop = OptionMenu(self.level_root, self.level_dir, *levels)
        level_drop.grid(row=0, column=1)

        button = Button(self.level_root, text="Start", command=self.quit)
        button.grid(columnspan=2)
        self.level_root.mainloop()

    def quit(self):
        global dir
        dir = str("data/"+self.level_dir.get())
        self.level_root.destroy()


class Program:
    def __init__(self, sprite_array, sound_array):
        SelectLevel()
        global dir
        props = open(dir+"/properties.txt", "r").readlines()
        props = props[0].split()
        props = [int(i) for i in props]
        self.box_array = []
        b = open(dir+"/boxes.txt", "r").readlines()
        for line in b:
            self.box_array.append(line.split())
        self.process_boxes()

        self.coin_array = []
        c = open(dir+"/coins.txt", "r").readlines()
        for line in c:
            self.coin_array.append(line.split())

        self.sounds = sound_array
        pygame.init()
        self.screen_w = 750
        self.screen_h = 750
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))

        self.pImg = pygame.image.load(sprite_array[0])
        self.player = Player(self.pImg.get_rect())
        self.pImg = pygame.transform.scale(self.pImg, (self.player.width, self.player.height))
        self.a_player = self.pImg

        self.player.x, self.player.y = props

        pressing = False
        self.da = 4
        while True:
            pygame.time.delay(30)
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break

            if pygame.mouse.get_pressed()[0] == 0:
                pressing = False
                self.player.angle += self.da
                self.player.angle %= 360
                self.a_player = pygame.transform.rotate(self.pImg, -self.player.angle + 270)
                self.player.set_dim(self.a_player.get_rect(), 1)
            else:
                if not pressing:
                    self.da *= -1
                pressing = True

            # ***** GAME DRAW *****
            self.player.move_forward()

            if self.picking_coin():
                self.coin_picked()

            if self.player_hit() and self.player.playing:
                self.game_stop()
                print("Game over")
                pygame.mixer.Sound(self.sounds[2]).play()
                self.player.playing = False

            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        self.screen.fill((255, 255, 255))
        for box in self.box_array:
            pygame.draw.rect(self.screen, (0, 0, 0), (int(box[0]) - int(self.player.x),
                                                      int(box[1]) - int(self.player.y),
                                                      int(box[2]) - int(box[0]),
                                                      int(box[3]) - int(box[1])))
        for coin in self.coin_array:
            pygame.draw.circle(self.screen, (255, 255, 0), (int(coin[0]) - int(self.player.x),
                                                            int(coin[1]) - int(self.player.y)), 5)
        self.screen.blit(self.a_player, self.find_player_pos())

    def process_boxes(self):
        b = self.box_array
        for i in range(len(self.box_array)):
            if b[i][0] > b[i][2]:
                x1 = b[i][0]
                self.box_array[i][0] = b[i][2]
                self.box_array[i][2] = x1
            if b[i][1] > b[i][3]:
                y1 = b[i][1]
                self.box_array[i][1] = b[i][3]
                self.box_array[i][3] = y1

    def find_player_pos(self):
        return (self.screen_w/2) - (self.player.width/2), (self.screen_h/2) - (self.player.height/2)

    def coin_picked(self):
        if len(self.coin_array) < 1:
            print("You won")
            pygame.mixer.Sound(self.sounds[1]).play()
            self.game_stop()
            self.player.playing = False
        else:
            print("You picked up a coin!")
            pygame.mixer.Sound(self.sounds[0]).play()

    def picking_coin(self):
        rad = 5
        pos = self.find_player_pos()
        for i in range(len(self.coin_array)):
            if (pos[0] + self.player.x + self.player.width >= int(self.coin_array[i][0]) - rad and
                    pos[0] + self.player.x <= int(self.coin_array[i][0]) + rad and
                    pos[1] + self.player.y + self.player.height >= int(self.coin_array[i][1]) - rad and
                    pos[1] + self.player.y <= int(self.coin_array[i][1]) + rad):
                del self.coin_array[i]
                return True
        else:
            return False

    def player_hit(self):
        pos = self.find_player_pos()
        rad = 7
        for box in self.box_array:
            if (pos[0] + self.player.x + self.player.width - rad >= int(box[0]) and
                    pos[0] + self.player.x + rad <= int(box[2]) and
                    pos[1] + self.player.y + self.player.height - rad >= int(box[1]) and
                    pos[1] + self.player.y + rad <= int(box[3])):
                return True
        return False

    def game_stop(self):
        self.player.speed = 0
        self.da = 0


# ****** INIT *****
imgs = ["playerCarImg.png"]
imgs = ["media/" + s for s in imgs]
sounds = ["coin_sound.ogg", "win.wav", "lose.wav", "retro_music.wav", "engine.wav", "explosion.mp3"]
sounds = ["sound/" + s for s in sounds]

dir = ""

p = Program(imgs, sounds)



