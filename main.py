import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
from random import random
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self, dim, red_pos, blue_pos, map_img):
        pygame.init()

        self.__dim = dim
        self.screen = pygame.display.set_mode((self.__dim[0]*20+400,self.__dim[1]*20))
        self.fps_controller = pygame.time.Clock()
        
        self.redbasepos = red_pos
        self.bluebasepos= blue_pos
        self.__resources = self.create_map(map_img)
        self.__resources[self.redbasepos[1]][self.redbasepos[0]] = 0
        self.__resources[self.redbasepos[1]][self.bluebasepos[0]] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros((self.__dim[1], self.__dim[0]))
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, self.redbasepos[0]*20, self.redbasepos[1]*20, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, self.bluebasepos[0]*20, self.bluebasepos[1]*20, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[self.redbasepos] = {self.__redbase:True}
        self.__PositionToRobot[self.bluebasepos] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            moves = {}
            if (random()>0.5):
                try:
                    scriptblue.ActBase(self.__bluebase)
                except:
                    print("Bluebase error")
                try:
                    scriptred.ActBase(self.__redbase)
                except:
                    print("Redbase error")
                
                for robo in self.__redbots:
                    try:
                        n = scriptred.ActRobot(robo)
                    except:
                        n=0
                        print("Redbot error")
                    moves[robo] = n
                for robo in self.__bluebots:
                    try:
                        n = scriptblue.ActRobot(robo)
                    except:
                        n=0
                        print("Blubot error")
                    moves[robo] = n
            else:
                try:
                    scriptred.ActBase(self.__redbase)
                except:
                    print("Redbase error")
                try:
                    scriptblue.ActBase(self.__bluebase)
                except:
                    print("Bluebase error")

                for robo in self.__bluebots:
                    try:
                        n = scriptblue.ActRobot(robo)
                    except:
                        n=0
                        print("Blue bot error")
                    moves[robo] = n

                for robo in self.__redbots:
                    try:
                        n = scriptred.ActRobot(robo)
                    except:
                        n=0
                        print("Redbot error")
                    moves[robo] = n
            
            
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
            #pygame.display.iconify()
            result = self.game_over()
            if result != None:
                return result
        return self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            #print( "Blue Wins")
            return 0
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Red Team Wins", True, (255,100,100), (230,230,230))
            #print( "Red Wins")
            return 1
        self.screen.blit(game_over, ((self.__dim[0])*10,(self.__dim[1])*10))
        pygame.display.flip()
        #time.sleep(5)
        sys.exit(0)

    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = ((self.__dim[0])*20+60, self.__dim[1]*18 + 5)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, ((self.__dim[0])*20+30, self.__dim[1]*18))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = ((self.__dim[0])*20+258, self.__dim[1]*18 +5)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, ((self.__dim[0])*20+230, self.__dim[1]*18))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self, img_path):
        """Take info about __collectibles and create the map"""
        im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, self.__dim)
        im = np.array(im)
        im = im - np.full((self.__dim[1],self.__dim[0]), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = self.__dim[0]*20+100
        titlerect.y = 40
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, ((self.__dim[0])*20+ 30, self.__dim[1]*2.5))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, ((self.__dim[0])*20+50, self.__dim[1]*5))
        self.screen.blit(blue_self, ((self.__dim[0])*20+50, self.__dim[1]*5 + 30))
        self.screen.blit(blue_robots, ((self.__dim[0])*20+50, self.__dim[1]*5 + 60))
        self.screen.blit(blue_virus, ((self.__dim[0])*20+50, self.__dim[1]*5 + 90))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, ((self.__dim[0])*20+30, self.__dim[1]*10))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, ((self.__dim[0])*20+50, self.__dim[1]*12))
        self.screen.blit(red_self, ((self.__dim[0])*20+50, self.__dim[1]*12 + 30))
        self.screen.blit(red_robots, ((self.__dim[0])*20+50, self.__dim[1]*12 + 60))
        self.screen.blit(red_virus, ((self.__dim[0])*20+50, self.__dim[1]*12 + 90))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 1e-2:
            return 0
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, ((self.__dim[0])*10,(self.__dim[0])*10))
            pygame.display.flip()
            #time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 1e-2:
            return 1
            print("Red Wins")
            game_over = game_over_font.render("Red Team Wins", True, (255,100,100), (230,230,230))
            self.screen.blit(game_over, ((self.__dim[0])*10,(self.__dim[0])*10))
            pygame.display.flip()
            #time.sleep(5)
            sys.exit(0)
            
    

game = Game((40,40), (19,9), (19,29), "test_img2.jpg")
print(game.run_game())