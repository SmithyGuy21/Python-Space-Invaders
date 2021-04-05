# https://www.youtube.com/watch?v=4_9twnEduFA&ab_channel=TechWithTim

import pygame

pygame.init()

win = pygame.display.set_mode((600, 600))
win.fill((255, 255, 255))


class Button:
    def __init__(self, color, x, y, width, height, text='', font=pygame.font.SysFont('comicsans', 80)):
        self.color = color
        self.x = int(x)
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = self.font.render(self.text, 1, (0, 0, 0))  # labels text in font passed in
            win.blit(text, (
                self.x + (self.width / 2 - int(text.get_width()) / 2),
                self.y + (self.height / 2 - int(text.get_height()) / 2)))  # centers text

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


def redrawWindow():
    win.fill((255, 255, 255))
    greenButton.draw(win, (0, 0, 0))
    resetButton.draw(win, (0, 0, 0))


run = True
greenButton = Button((0, 0, 255), 150, 200, 300, 150, "Default")
resetButton = Button((100, 100, 100), 0, 0, 100, 75, "Reset", pygame.font.SysFont('comicsans', 40))
tempText = "Default"
tempColor = (0, 0, 255)

# while run:
#     pygame.time.Clock().tick(60)    # locks game to 60fps so the program isn't intensive
#     redrawWindow()
#     pygame.display.update()
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#             pygame.quit()
#             quit()
#         pos = pygame.mouse.get_pos()
#         if greenButton.isOver(pos) and greenButton.text != "Nice Job" and greenButton.text != "Almost":
#             tempText = greenButton.text
#             tempColor = greenButton.color
#             greenButton.text = "Almost"
#             greenButton.color = (0, 150, 0)
#         elif not (greenButton.isOver(pos)) and greenButton.text == "Almost":
#             greenButton.text = tempText
#             greenButton.color = tempColor
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if greenButton.isOver(pos):
#                 greenButton.text = "Nice Job"
#                 greenButton.color = (0, 255, 0)
#             elif resetButton.isOver(pos):
#                 greenButton.text = "Default"
#                 greenButton.color = (0, 0, 255)
#             else:
#                 greenButton.text = "Try Again"
#                 greenButton.color = (255, 0, 0)
