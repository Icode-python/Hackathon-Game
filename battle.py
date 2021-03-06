from settings import *
import pygame
from guis import *
import random

class BattleSystem(pygame.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.gui
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.playerimg = pygame.Surface((TILESIZE * 20, TILESIZE * 20))
        self.playerimg.fill(YELLOW)

        self.mobimg = pygame.Surface((TILESIZE * 20, TILESIZE * 20))
        self.mobimg.fill(RED)
        
        self.playerHealthBar = pygame.Surface((TILESIZE * PLAYER_HEALTH, TILESIZE))
        self.playerHealthBar.fill(RED)
        self.mobHealthBar = pygame.Surface((TILESIZE, TILESIZE * 2))
        self.mobHealthBar.fill(RED)

        self.attacks = []
        self.keyboard = Keyboard(WIDTH - KEYBOARDWIDTH, HEIGHT - KEYBOARDHEIGHT, KEYBOARDWIDTH, KEYBOARDHEIGHT, self.game, None)
        self.questionBoard = Button(self.keyboard.x, self.keyboard.y - KEYBOARDHEIGHT - TILESIZE, KEYBOARDWIDTH, KEYBOARDHEIGHT, '', LIGHTGREY, self.game, self.keyboard.font_size)
        
        self.Battling = False
        self.width = 64
        self.height = 64

    def battle(self, mob):
        self.Battling = True
        self.generateProblem()
        self.keyboard.cursorx = self.keyboard.x - self.keyboard.width/2 + CURSORWIDTH
        while self.Battling:
            self.playerHealthBar = pygame.Surface((TILESIZE * self.game.player.health * 1.5, TILESIZE))
            self.playerHealthBar.fill(RED)
            self.mobHealthBar = pygame.Surface((TILESIZE * mob.health * 1.5, TILESIZE))
            self.mobHealthBar.fill(RED)
            self.game.update()
            for gui in self.game.gui:
                gui.update()
            self.game.events()
            self.game.draw()
            self.questionBoard.text = self.equation
            self.keyboard.cursorinput(mob)
            #self.check(mob)
    
    def check(self, mob):
        if len(self.keyboard.text) > 0:
            self.text = float(self.keyboard.text)
            if self.text == self.answer:
                self.keyboard.text = ''
                self.keyboard.screenText = ''
                self.text = 0
                mob.health -= 1
                if mob.health == 0:
                    self.Battling = False
                    mob.kill()
                self.generateProblem()
            else:
                self.game.player.health -= 1
                self.generateProblem()

    def generateProblem(self):
        self.operatorList = ['+', '-', '*', '/']
        self.operatorGen = random.randint(0, 3)
        self.operator = self.operatorList[self.operatorGen]
        self.num1 = random.randint(0, 100)
        self.num2 = random.randint(1, 10)
        self.equation = f' {self.num1} {self.operator} {self.num2}'
        print(self.equation)
        self.answer = 0
        if self.operator == '+': 
            self.answer = self.num1 + self.num2

        if self.operator == '-': 
            self.answer = self.num1 - self.num2
        
        if self.operator == '*': 
            self.answer = self.num1 * self.num2

        if self.operator == '/': 
            self.answer = self.num1 / self.num2
            self.answer = round(self.answer, 2)
