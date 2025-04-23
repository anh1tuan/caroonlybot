import pygame
from numpy import array

pygame.init()
pygame.display.set_caption("Caro vs Bot")

img_bg = pygame.image.load("image/background.png")
img_cell = pygame.image.load("image/cell.png")
img_cellx = pygame.image.load("image/cellx.png")
img_cello = pygame.image.load("image/cello.png")
img_celle = pygame.image.load("image/celle.png")
img_bgright = pygame.image.load("image/bgright.png")
font = pygame.font.SysFont('Times New Roman', 100)
fontnho = pygame.font.SysFont('Times New Roman', 60)
img_luot = {
    True:font.render("X",True,(255,0,0)),
    False:font.render("O",True,(0,202,0))
}
vt_img_luot = {
    True:None,
    False:None
}

for i in vt_img_luot:
    vt_img_luot[i] = img_luot[i].get_rect()
    vt_img_luot[i].center = (300//2,200//2)
    vt_img_luot[i][0] += 700
    vt_img_luot[i][1] += 200

img_luot_man = {
    True:fontnho.render("Lượt bạn",True,(0,0,0)),
    False:fontnho.render("Máy nghĩ",True,(0,0,0))
}

vt_img_luot_man = {
    True:None,
    False:None
}

for i in vt_img_luot_man:
    vt_img_luot_man[i] = img_luot_man[i].get_rect()
    vt_img_luot_man[i].center = (300//2,200//2)
    vt_img_luot_man[i][0] += 700
    vt_img_luot_man[i][1] += 200

img_win = {
    1:fontnho.render("X thắng",True,(255,0,0)),
    2:fontnho.render("O thắng",True,(0,202,0)),
    3:fontnho.render("Hòa",True,(255,255,0))
}

vt_img_win = {
    1:None,
    2:None
}

for i in img_win:
    vt_img_win[i] = img_win[i].get_rect()
    vt_img_win[i].center = (300//2,200//2)
    vt_img_win[i][0] += 700
    vt_img_win[i][1] += 200

pygame.display.set_icon(img_cellx)

class caro:
    L_4_huong = ((-1,-1),(-1,0),(-1,1),(0,-1))
    def __init__(self,r,c,show = True):
        self.r = r
        self.c = c
        self.kc_cell = min(int(700/r),int(700/c))
        self.show = show
        if show:
            self.D_img = {
                0:pygame.transform.scale(img_cell,(self.kc_cell,self.kc_cell)),
                1:pygame.transform.scale(img_cellx,(self.kc_cell,self.kc_cell)),
                2:pygame.transform.scale(img_cello,(self.kc_cell,self.kc_cell))
            }
            self.img_previos_move = pygame.transform.scale(img_bgright,(self.kc_cell,self.kc_cell))
            self.img_celle = pygame.transform.scale(img_celle,(self.kc_cell,self.kc_cell))
            self.sc = pygame.display.set_mode((1000,700))
        self.run = True
        self.vsbot = False
        self.show_affect = False
        self.time_load = pygame.time.get_ticks()
        self.reset()
    def reset(self):
        self.diagram = []
        for i in range(self.c):
            self.diagram.append([0]*self.r)
        self.xo = True
        self.time = pygame.time.get_ticks()
        self.time_show = pygame.time.get_ticks() - 1000
        self.result = 0
        self.time_end = None
        self.L_undo = []
        self.L_undo_affect = []
        self.L_undo_gh = []
        self.L_affect = []
        self.trai = None
        self.phai = None
        self.tren = None
        self.duoi = None
    def nap_diagram(self,diagram,xo):
        self.reset()
        self.diagram = []
        for i in range(len(diagram)):
            self.diagram.append(diagram[i].copy())
        self.r = len(diagram[0])
        self.c = len(diagram)
        self.kc_cell = min(int(700/self.r),int(700/self.c))
        if self.show:
            self.D_img = {
                0:pygame.transform.scale(img_cell,(self.kc_cell,self.kc_cell)),
                1:pygame.transform.scale(img_cellx,(self.kc_cell,self.kc_cell)),
                2:pygame.transform.scale(img_cello,(self.kc_cell,self.kc_cell))
            }
            self.img_previos_move = pygame.transform.scale(img_bgright,(self.kc_cell,self.kc_cell))
            self.img_celle = pygame.transform.scale(img_celle,(self.kc_cell,self.kc_cell))
        if xo == 1: self.xo = True
        else: self.xo = False
        self.nap_L_affect()
    def nap_L_affect(self):
        self.L_affect = []
        kq = {1:0,2:0}
        for y in range(self.c):
            for x in range(self.r):
                for xm,ym in self.L_4_huong:
                    if self.diagram[y][x] != 0:
                        for i in range(-2,3):
                            if i != 0:
                                if 0 <= x+i*xm < self.r and 0 <= y+i*ym < self.c:
                                    if (x+i*xm,y+i*ym) not in self.L_affect and self.diagram[y+i*ym][x+i*xm] == 0:
                                        self.L_affect.append((x+i*xm,y+i*ym))
                        if self.trai == None:
                            self.trai = x
                            self.phai = x
                            self.tren = y
                            self.duoi = y
                        else:
                            if x < self.trai:
                                self.trai = x
                            elif x > self.phai:
                                self.phai = x
                            if y < self.tren:
                                self.tren = y
                            elif y > self.duoi:
                                self.duoi = y
    def lay_diagram(self):
        kq = []
        for i in range(len(self.diagram)):
            kq.append(self.diagram[i].copy())
        return kq  
    def draw_khung_luot_di(self):
        pygame.draw.rect(self.sc,(0, 51, 102),(700 - int(0.06*self.kc_cell),0,300 + int(0.06*self.kc_cell),200),width = int(0.06*self.kc_cell),border_radius = 5)
        if self.result == 0:
            if self.vsbot:
                self.sc.blit(img_luot_man[self.xo],vt_img_luot_man[self.xo])
            else:
                self.sc.blit(img_luot[self.xo],vt_img_luot[self.xo])
        else:
            self.sc.blit(img_win[self.result],vt_img_win[self.result])
    def draw_khung_tg(self):
        pygame.draw.rect(self.sc,(0, 51, 102),(700 - int(0.06*self.kc_cell),200,300 + int(0.06*self.kc_cell),200),width = int(0.06*self.kc_cell),border_radius = 5)
        if self.result == 0:
            if pygame.time.get_ticks() - self.time_show > 1000:
                self.time_show = pygame.time.get_ticks()
                time = (pygame.time.get_ticks() - self.time)//1000
                phut = time//60
                giay = time%60
                chuoi = ""
                if phut < 10:
                    chuoi += "0"
                chuoi += str(phut) + ":"
                if giay < 10:
                    chuoi += "0"
                chuoi += str(giay)
                self.img_time = font.render(chuoi,True, (0, 51, 102))
                self.vt_img_time = self.img_time.get_rect()
                self.vt_img_time.center = (300//2,200//2)
                self.vt_img_time[0] += 700
        else:
            if self.time_end == None: self.time_end = (pygame.time.get_ticks() - self.time)//1000
        self.sc.blit(self.img_time,self.vt_img_time)
    def draw_khung_logo(self):
        pygame.draw.rect(self.sc,(0, 51, 102),(700 - int(0.06*self.kc_cell),400,300 + int(0.06*self.kc_cell),300),width = int(0.06*self.kc_cell),border_radius = 5)
    def vsmay(self):
        self.vsbot = True
    def vsnguoi(self):
        self.vsbot = False
    def draw(self):
        self.sc.blit(img_bg,(0,0))
        if len(self.L_undo) != 0:
            x, y = self.L_undo[-1]
            self.sc.blit(self.img_previos_move,(x*self.kc_cell,y*self.kc_cell))
        if self.show_affect:
            for x,y in self.L_affect:
                self.sc.blit(self.img_celle,(x*self.kc_cell,y*self.kc_cell))
        for i in range(self.r):
            for j in range(self.c):
                self.sc.blit(self.D_img[self.diagram[j][i]],(i*self.kc_cell,j*self.kc_cell))
        pygame.draw.rect(self.sc,(0, 51, 102),(0,0,self.kc_cell*self.r,self.kc_cell*self.c),width = int(0.06*self.kc_cell),border_radius = 5)
        #pygame.draw.rect(self.sc,(0, 51, 102),(700,0,300,700),border_radius = 5)
        self.sc.blit(img_bgright,(700,0))
        self.draw_khung_tg()
        self.draw_khung_luot_di()
        self.draw_khung_logo()
        pygame.display.update()
    def botmove(self,x,y):
        if self.result == 0 and 0 <= x < self.r and 0 <= y < self.c and self.diagram[y][x] == 0:
            if self.xo:
                self.diagram[y][x] = 1
            else:
                self.diagram[y][x] = 2
            self.xo = not self.xo
            self.L_undo.append([x,y])
            self.L_undo_affect.append(self.L_affect.copy())
            self.L_undo_gh.append((self.trai,self.phai,self.tren,self.duoi))
            self.update_gh(x,y)
            self.result = self.checkresult()
        elif self.diagram[y][x] != 0:
            print("Trùng điểm")
    def update_gh(self,x,y):
        if self.trai == None:
            self.trai = x
            self.phai = x
            self.tren = y
            self.duoi = y
        else:
            if x < self.trai:
                self.trai = x
            elif x > self.phai:
                self.phai = x
            if y < self.tren:
                self.tren = y
            elif y > self.duoi:
                self.duoi = y
        if (x,y) in self.L_affect:
            self.L_affect.remove((x,y))
        for xm,ym in self.L_4_huong:
            if self.diagram[y][x] != 0:
                for i in range(-2,3):
                    if i != 0:
                        if 0 <= x+i*xm < self.r and 0 <= y+i*ym < self.c:
                            if (x+i*xm,y+i*ym) not in self.L_affect and self.diagram[y+i*ym][x+i*xm] == 0:
                                self.L_affect.append((x+i*xm,y+i*ym))
    def lay_L_nuoc_di(self):
        return self.L_affect.copy()
    def lay_gh(self):
        return self.trai,self.phai,self.tren,self.duoi
    def undo(self,sl = 1):
        for i in range(sl):
            if len(self.L_undo) != 0:
                self.L_affect = self.L_undo_affect[-1]
                self.trai,self.phai,self.tren,self.duoi = self.L_undo_gh[-1]
                x,y = self.L_undo[-1]
                self.diagram[y][x] = 0
                self.L_undo.pop(-1)
                self.L_undo_affect.pop(-1)
                self.L_undo_gh.pop(-1)
                self.xo = not self.xo
                self.result = 0
            # print("Undo")
    def event(self):
        for e in pygame.event.get(): 
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.result == 0 and not self.vsbot or self.xo:
                    x,y = pygame.mouse.get_pos()
                    x,y = x//self.kc_cell,y//self.kc_cell
                    if 0 <= x < self.r and 0 <= y < self.c and self.diagram[y][x] == 0:
                        if self.xo:
                            self.diagram[y][x] = 1
                        else:
                            self.diagram[y][x] = 2
                        self.xo = not self.xo
                        self.L_undo.append([x,y])
                        self.L_undo_affect.append(self.L_affect.copy())
                        self.L_undo_gh.append((self.trai,self.phai,self.tren,self.duoi))
                        self.update_gh(x,y)
                        self.result = self.checkresult()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.reset()
                    print("SPACE")
                if e.key == pygame.K_BACKSPACE:
                    self.undo()
                if e.key == pygame.K_u:
                    self.undo(2)
                if e.key == pygame.K_TAB:
                    self.show_affect = not self.show_affect
                if e.key == pygame.K_q:  # Thêm đoạn này để thoát game khi nhấn Q
                    self.run = False
                    pygame.quit()  # Dừng pygame
                    return    
    def checkresult_huong(self,x,y,xm,ym):
        x0, y0 = x,y
        x -= xm
        y -= ym
        dem = 0
        diem = self.diagram[y0][x0]
        while True:
            if (not (0 <= x < self.r and 0 <= y < self.c)) or diem != self.diagram[y][x]:
                break
            dem += 1
            x -= xm
            y -= ym
        x, y = x0,y0
        x += xm
        y += ym
        while True:
            if (not (0 <= x < self.r and 0 <= y < self.c)) or diem != self.diagram[y][x]:
                break
            dem += 1
            x += xm
            y += ym
        if dem < 4: return 0
        return diem
    def checkresult(self):
        if not self.L_undo:  # kiểm tra nếu chưa có nước đi nào
            return 0  # chưa kết thúc

        x, y = self.L_undo[-1]
        kq = self.checkresult_huong(x, y, 1, 0)
        if kq != 0: return kq
        kq = self.checkresult_huong(x, y, 0, 1)
        if kq != 0: return kq
        kq = self.checkresult_huong(x, y, 1, 1)
        if kq != 0: return kq
        kq = self.checkresult_huong(x, y, 1, -1)
        if kq != 0: return kq
        if len(self.L_affect) == 0: return 3
        return 0

    def cho(self):
        if pygame.time.get_ticks() - self.time_load > 1000:
            self.time_load = pygame.time.get_ticks()
            self.draw()
        pygame.event.get()
    def runned(self):
        self.event()
        if self.run:
            self.draw()
        return self.run