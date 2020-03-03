import pygame as pg


pg.init()
##screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.SysFont(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text='',isPassword=False, isDoB=False):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.isPassword = isPassword
        self.isDoB = isDoB
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    #print(self.text)
                    #self.text = ''
                    pass
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                #previously just else
                #added code to only accept certain chars


                elif (event.unicode).isalnum() or (event.unicode) in ['!',',','@','#','$','%','.','?']:
                    self.text += event.unicode
                # Re-render the text
                # for test case 1, exception handling:
                #self.txt_surface = FONT.render(self.text, True, self.color,(255,255,255))
                #for test case 2, actual run:
                if self.isPassword == True and len(self.text) != 0:
                    self.txt_surface = FONT.render('*'*(len(self.text)-1)+self.text[len(self.text)-1],True, self.color,(255,255,255))
                elif self.isDoB == True:
                    if (len(self.text)>1 and self.text[-1] not in  ['0','1','2','3','4','5','6','7','8','9']) or (len(self.text)>8 and self.text[-1] in ['0','1','2','3','4','5','6','7','8','9']):
                        self.text = self.text[0:len(self.text)-1]
                    elif (len(self.text) == 1 and self.text[0] not in  ['0','1','2','3','4','5','6','7','8','9']):
                        self.text = ''
                    else:
                        pass
                    self.txt_surface = FONT.render(self.text+"DDMMYYYY"[len(self.text):], True, self.color,(255,255,255))
                else: self.txt_surface = FONT.render(self.text, True, self.color,(255,255,255))

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


#test InputBox class and its functions
def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_UP:
                   print(input_box1.text)
                   print(input_box2.text)


        for box in input_boxes:
            box.update()

        #screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)



#main()
#pg.quit()
