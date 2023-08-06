
import os
import pickle
import sys

import guizero
import pygame
import pygame.draw
from guizero import App
from pgzero.rect import Rect

from .data import Data


def round_xy(pos):
    '四舍五入坐标'
    if isinstance(pos, tuple):
        x, y = pos
        return(round(x), round(y))
    else:
        return(round(pos))


class Master:
    def __init__(self, data_path='data.dat') -> None:
        '管家类，负责一些管理类的功能'
        self._fullscreen = False
        self.data = Data(data_path)
        self.load_data()
        self.data.temp = ''
        self.app = App(visible=False)
        self.mod = sys.modules['__main__']

    @property
    def data_path(self):
        '获取data_path'
        return self.data.data_path

    @data_path.setter
    def data_path(self, path):
        '设置data_path'
        print(f'数据地址{path}')
        self.data.data_path = path

    def load_data(self):
        '加载数据'
        self.data.load_data()

    def save_data(self):
        '保存数据'
        self.data.save_data()

    def del_data(self):
        '删除数据'
        self.data.del_data()

    def set_fullscreen(self) -> None:
        '设置全屏'
        self.mod.screen.surface = pygame.display.set_mode(
            (self.mod.WIDTH, self.mod.HEIGHT), pygame.FULLSCREEN)
        self._fullscreen = True

    def set_windowed(self) -> None:
        '设置窗口化'
        self.mod.screen.surface = pygame.display.set_mode(
            (self.mod.WIDTH, self.mod.HEIGHT))
        self._fullscreen = False

    def toggle_fullscreen(self) -> None:
        '切换全屏和窗口化'
        if self._fullscreen:
            self.set_windowed()
        else:
            self.set_fullscreen()

    def hide_mouse(self) -> None:
        '隐藏鼠标'
        pygame.mouse.set_visible(False)

    def show_mouse(self) -> None:
        '显示鼠标'
        pygame.mouse.set_visible(True)

    def draw_dot(self, pos, radius, color):
        '绘制一个点，参数依次为：中心坐标，直径，颜色'
        pos = round_xy(pos)
        self.draw_circle(pos, radius, color, 0)

    def draw_line(self, start, end, color, border=1):
        '绘制一条线，参数依次为：起点、终点、颜色、宽度'
        start = round_xy(start)
        end = round_xy(end)
        pygame.draw.line(self._surf, color, start, end, border)

    def draw_circle(self, pos, radius, color, border=1):
        '''
        绘制圆圈或者圆环，参数依次为：圆心坐标、直径、颜色、圆环宽度
        border参数默认为1，会绘制宽度为1的圆圈
        border参数设置成0，绘制实心圆
        '''
        pos = round_xy(pos)
        self._surf = self.mod.screen.surface
        pygame.draw.circle(self._surf, color, pos, radius, border)

    def draw_ellipse(self, pos, width, height, color, border=1):
        '''
        绘制椭圆，参数依次为：中心坐标，宽度、高度、颜色、边框宽度
        border参数默认为1，会绘制宽度为1的椭圆
        border参数设置成0，绘制实心椭圆
        '''
        pos = round_xy(pos)
        self._surf = self.mod.screen.surface
        x = pos[0]-width/2
        y = pos[1]-height/2
        rect = Rect(x, y, width, height)
        pygame.draw.ellipse(self._surf, color, rect, border)

    def draw_rect(self, pos, width, height, color, border=1, radius=0):
        '''
        绘制长方形或者正方形，参数以此为：中心坐标、宽度、高度、颜色、边框宽度、圆角半径
        边框宽度、圆角半径默认为1和0,会绘制一个边框为1没有圆角的方形
        '''
        pos = round_xy(pos)
        self._surf = self.mod.screen.surface
        x = pos[0]-width/2
        y = pos[1]-height/2
        rect = Rect(x, y, width, height)
        pygame.draw.rect(self._surf, color, rect, border, radius)

    def input(self, msg='请输入数据：') -> str:
        '简单输入框'
        text = guizero.askstring('输入', msg)
        self.data.temp = text
        return text

    def select_file(self, msg='请选择文件', filetypes=[["All files", "*.*"]]) -> str:
        '''
        选择文件，filetypes是文件类型，比如：   

        filetypes=[["All files", "*.*"]]    

        不想限定的话，就不传递这个参数。  
        '''
        file = guizero.select_file(
            '请选择一个文件', filetypes=filetypes, master=self.app)
        self.data.temp = file
        return file

    def select_file_save(self, msg='请选择文件', filetypes=[["All files", "*.*"]]) -> str:
        '''
        保存文件的选择提示框，filetypes是文件类型，比如：   

        filetypes=[["All files", "*.*"]]    

        不想限定的话，就不传递这个参数。  
        '''
        path = guizero.select_file(
            '请选择一个文件', filetypes=filetypes, save=True, master=self.app)
        self.data.temp = path
        return path

    def select_dir(self, msg='请选择文件夹') -> str:
        '选择一个文件夹'
        dir = guizero.select_folder('请选择一个文件夹', master=self.app)
        self.data.temp = dir
        return dir

    def yes_no(self, msg='是否？'):
        '是否做某件事的选择框'
        yes_or_no = guizero.yesno('请选择', msg, master=self.app)
        self.data.temp = yes_or_no
        return yes_or_no

    def msg(self, msg='这是提示信息'):
        '提示信息'
        guizero.info('提示', msg, master=self.app)

    def warning(self, msg='这是警告信息'):
        '警告信息'
        guizero.warn('警告', msg, master=self.app)

    def error(self, msg='这是错误信息'):
        '错误信息'
        guizero.error('错误', msg, master=self.app)
