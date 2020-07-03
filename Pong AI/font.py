import pygame
def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class Font():
    def __init__(self, path):
        self.spacing = 2
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = pygame.image.load(path).convert()
        font_img.set_colorkey((0,0,0))
        current_char_width = 0
        self.charaters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x,0))
            if c[0] == 127:
                char_img = clip(font_img, x-current_char_width, 0 ,current_char_width,font_img.get_height())
                self.charaters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.charaters["A"].get_width()*2
    def render(self, surf, text, loc, maxlinewidth):
        x_offset = 0
        y_offset = 0
        for char in text:
            if char != " ":
                surf.blit(pygame.transform.scale(self.charaters[char],(self.charaters[char].get_width()*2,self.charaters[char].get_height()*2)), (loc[0]+x_offset,loc[1]+y_offset))
                x_offset += self.charaters[char].get_width()*2 + self.spacing
            else:
                x_offset += self.space_width + self.spacing
            if x_offset > maxlinewidth:
                if char != " ":
                    x_offset = 0
                    y_offset += self.charaters[char].get_height() + self.spacing