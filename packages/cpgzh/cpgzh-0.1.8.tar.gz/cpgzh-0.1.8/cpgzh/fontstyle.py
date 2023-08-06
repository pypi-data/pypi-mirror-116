
import os
import pygame
import pygame.draw
from pgzero import loaders


class FontStyle:
    '字体样式类'

    def __init__(self) -> None:
        '初始化字体样式'
        self.styles = {}
        path = os.path.join(loaders.root, 'fonts')
        if os.path.isdir(path):
            self.fonts = os.listdir(path)
            self.fontname = self.fonts[-1]  # 字体名字
        else:
            self.fonts = []
            self.fontname = None
        self.bold = None  # 加粗
        self.italic = None  # 斜体
        self.underline = None  # 下划线
        self.color = 'black'  # 字体颜色
        self.gcolor = None  # 渐变色
        self.ocolor = None  # 边框颜色
        self.scolor = None  # 阴影颜色
        self.align = 'left'  # 左对齐
        self.alpha = 1.0  # 不透明度
        self.angle = 0  # 旋转角度
        self.owidth = None  # 边框宽度
        self.shadow = (0.0, 0.0)  # 阴影，x方向和y方向
        self.fontsize = 30  # 字体大小
        self.sysfonts = pygame.font.get_fonts()  # 所有系统字体
        self.sysfontname = self.sysfonts[-1]  # 设置系统字体

    def __setattr__(self, name, value) -> None:
        '重写设置属性的方法'
        self.__dict__[name] = value
        if not name in ['sysfonts', 'styles', 'fonts']:
            self.styles[name] = value
