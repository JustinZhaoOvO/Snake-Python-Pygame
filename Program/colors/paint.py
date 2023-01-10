# coding=UTF-8
# File: paint.py
# SOftware: PyCharm
# time: 2021-08-27 3:00 p.m.
import pygame
import random
import sys
class paint():
    def __init__(self,tran,veti,each_tran,each_veti):
        self.size = self.width, self.height = tran,veti
        self.each_tran = each_tran
        self.each_veti = each_veti
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("colors")
        self.colorlst = []
        self.green = self.init_picture("green.png",(each_tran,each_veti))
        self.colorlst.append(self.green)
        self.blue = self.init_picture("blue.png", (each_tran,each_veti))
        self.colorlst.append(self.blue)
        self.cyan = self.init_picture("cyan.png", (each_tran,each_veti))
        self.colorlst.append(self.cyan)
        self.lime = self.init_picture("lime.png", (each_tran,each_veti))
        self.colorlst.append(self.lime)
        self.pink = self.init_picture("pink.png", (each_tran,each_veti))
        self.colorlst.append(self.pink)
        self.purple = self.init_picture("purple.png", (each_tran,each_veti))
        self.colorlst.append(self.purple)
        self.red = self.init_picture("red.png", (each_tran,each_veti))
        self.colorlst.append(self.red)
        self.white = self.init_picture("white.png", (each_tran,each_veti))
        self.colorlst.append(self.white)
        self.yellow = self.init_picture("yellow.png", (each_tran,each_veti))
        self.colorlst.append(self.yellow)


    def make_map(self):
        lst = []
        for i in range(self.height):
            lst.append([])
            for _ in range(self.width):
                lst[i].append(0)
        return lst

    def make_indexlist(self):
        lst = []
        for i in range(self.width//self.each_tran):
            for j in range(self.height//self.each_veti):
                lst.append((i,j))
        random.shuffle(lst)
        return lst

    def init_picture(self,picture_link,picture_size):
        picture = pygame.image.load(picture_link)
        picture = pygame.transform.scale(picture,picture_size)
        return picture

    def painting(self,index):
        self.screen.blit(random.choice(self.colorlst),index)

def main(tran,veti,each_tran,each_veti):
    Paint = paint(tran,veti,each_tran,each_veti)
    index_lst = Paint.make_indexlist()
    for i in index_lst:
        Paint.painting((i[0] * each_tran,i[1] * each_veti))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:          #.type获取操作的数字代码,pygame.QUIT为256
                sys.exit(10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:          #.type获取操作的数字代码,pygame.QUIT为256
                sys.exit(10)
if __name__ == "__main__":
    main(400,400,4,4)