"""
Last modified: 25.06.2020

The table class is defined here. You can change the layout of the table.
"""

from graphics import *
from textures import *


class Table:
    def __init__(
        self,
        _gameboardwidth,
        _gameboardheight,
        _border,
        _holesize_middle,
        _holesize_edges,
        _texture,
        _textureBalken,
        _textureGameover,
    ):
        self.gameboardwidth = _gameboardwidth
        self.gameboardheight = _gameboardheight
        self.border = _border
        self.holesize_middle = _holesize_middle
        self.holesize_edges = _holesize_edges
        self.texture = _texture
        self.textureBalken = _textureBalken
        self.textureGameover = _textureGameover

        # if no table texture detected, use the following values
        self.border_r = 0.5
        self.border_g = 0.0
        self.border_b = 0.0
        self.gameboard_r = 0.0
        self.gameboard_g = 0.5
        self.gameboard_b = 0.0
        self.hole_r = 0.0
        self.hole_g = 0.0
        self.hole_b = 0.0

    def draw(self):
        if self.texture == 0:
            glBegin(GL_QUADS)
            glColor3f(self.border_r, self.border_g, self.border_b)
            glVertex2f(0, 0)
            glVertex2f(self.gameboardwidth, 0)
            glVertex2f(self.gameboardwidth, self.gameboardheight)
            glVertex2f(0, self.gameboardheight)
            glEnd()

            glBegin(GL_QUADS)
            glColor3f(self.gameboard_r, self.gameboard_g, self.gameboard_b)
            glVertex2f(self.border, self.border)
            glVertex2f(self.gameboardwidth - self.border, self.border)
            glVertex2f(
                self.gameboardwidth - self.border, self.gameboardheight - self.border
            )
            glVertex2f(self.border, self.gameboardheight - self.border)
            glEnd()

        else:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glColor3f(1.0, 1.0, 1.0)

            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(0.0, 0.0)
            glTexCoord2f(1.0, 0.0)
            glVertex2f(self.gameboardwidth, 0.0)
            glTexCoord2f(1.0, 1.0)
            glVertex2f(self.gameboardwidth, self.gameboardheight)
            glTexCoord2f(0.0, 1.0)
            glVertex2f(0.0, self.gameboardheight)
            glEnd()
            glDisable(GL_TEXTURE_2D)

        glColor3f(self.hole_r, self.hole_g, self.hole_b)
        # holes on edges:
        graphicsBall(
            self.gameboardwidth - self.border,
            self.gameboardheight - self.border,
            self.holesize_edges,
        )
        graphicsBall(
            self.gameboardwidth - self.border, 0 + self.border, self.holesize_edges
        )
        graphicsBall(0 + self.border, 0 + self.border, self.holesize_edges)
        graphicsBall(
            0 + self.border, self.gameboardheight - self.border, self.holesize_edges
        )
        # holes in middle:
        graphicsBall(self.gameboardwidth / 2, self.border, self.holesize_middle)
        graphicsBall(
            self.gameboardwidth / 2,
            self.gameboardheight - self.border,
            self.holesize_middle,
        )

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textureBalken)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0.0, self.gameboardheight + 150)
        glTexCoord2f(0.0, 0.3)
        glVertex2f(self.gameboardwidth, self.gameboardheight + 150)
        glTexCoord2f(1.0, 0.3)
        glVertex2f(self.gameboardwidth, self.gameboardheight)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(0.0, self.gameboardheight)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def drawGameover(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textureGameover)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.gameboardwidth, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.gameboardwidth, self.gameboardheight)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0.0, self.gameboardheight)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glDisable(GL_BLEND)
