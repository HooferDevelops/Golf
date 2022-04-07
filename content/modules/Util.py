import pygame, math, os, sys

def createLine(surface, color, startPos, endPos, width=1, maxLength=99999):
    x0, y0 = startPos
    x1, y1 = endPos
    length = min(math.hypot(x1-x0, y1-y0), maxLength)
    angle = math.atan2(y0-y1, x0-x1)

    # I do not know how I managed to do this with 0 calculus skills
    midX = length/2 * -math.cos(abs(math.radians(360)-angle)) + x0
    midY = length/2 * math.sin(abs(math.radians(360)-angle)) + y0 
  
    width2, length2 = width, length/2
    sin_ang, cos_ang = math.sin(angle), math.cos(angle)

    width2_sin_ang  = width2*sin_ang
    width2_cos_ang  = width2*cos_ang
    length2_sin_ang = length2*sin_ang
    length2_cos_ang = length2*cos_ang

    ul = (midX + length2_cos_ang - width2_sin_ang,
          midY + width2_cos_ang  + length2_sin_ang)
          
    ur = (midX - length2_cos_ang - width2_sin_ang,
          midY + width2_cos_ang  - length2_sin_ang)
    bl = (midX + length2_cos_ang + width2_sin_ang,
          midY - width2_cos_ang  + length2_sin_ang)
    br = (midX - length2_cos_ang + width2_sin_ang,
          midY - width2_cos_ang  - length2_sin_ang)

    # Allows for opacity
    transparentSurface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    transparentSurface.fill((0,0,0,0))
    pygame.draw.polygon(transparentSurface, color, (ul, ur, br, bl))
    
    surface.blit(transparentSurface, (0,0))

def lerp3Color(colorA, colorB, colorC, value):
  # https://stackoverflow.com/questions/13488957/interpolate-from-one-color-to-another
  if (value <= 0.5):
    value = value * 2
    r = (colorB[0] - colorA[0]) * value + colorA[0]
    g = (colorB[1] - colorA[1]) * value + colorA[1]
    b = (colorB[2] - colorA[2]) * value + colorA[2]
    a = (colorB[3] - colorA[3]) * value + colorA[3]
    
    return (r, g, b, a)
  else:
    r = (colorC[0] - colorB[0]) * value + colorB[0]
    g = (colorC[1] - colorB[1]) * value + colorB[1]
    b = (colorC[2] - colorB[2]) * value + colorB[2]
    a = (colorC[3] - colorB[3]) * value + colorB[3]
    
    return (r, g, b, a)

windowSize = 800
rootDirectory = os.path.dirname(sys.modules['__main__'].__file__)