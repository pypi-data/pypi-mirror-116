import math
import os
import pickle
import sys
import time

import guizero
from guizero import App
import pygame
import pygame.draw
from pgzero import game, loaders
from pgzero.actor import ANCHOR_CENTER, POS_TOPLEFT, Actor, transform_anchor
from pgzero.rect import Rect

def round_xy(pos):
    '四舍五入坐标'
    if isinstance(pos, tuple):
        x, y = pos
        return(round(x), round(y))
    else:
        return(round(pos))


class Data:
    '数据存储类'

    def __init__(self) -> None:
        self.status = 0
        self.start = time.time()
        self.time = 0
        self.score = 0


class FontStyle:
    '字体样式类'
    

    def __init__(self) -> None:
        '初始化字体样式'
        self.styles = {}
        path = os.path.join(loaders.root, 'fonts')
        if os.path.isdir(path):
            self.fonts = os.listdir(path)
            self.fontname = self.fonts[-1]# 字体名字
        else:
            self.fonts = []
            self.fontname = None
        self.bold = None#加粗
        self.italic = None# 斜体
        self.underline=None# 下划线
        self.color = 'black'# 字体颜色
        self.gcolor = None# 渐变色
        self.ocolor = None# 边框颜色        
        self.scolor = None# 阴影颜色
        self.align = 'left'# 左对齐
        self.alpha = 1.0# 不透明度
        self.angle = 0# 旋转角度
        self.owidth = None# 边框宽度
        self.shadow = (0.0,0.0)# 阴影，x方向和y方向
        self.fontsize = 30# 字体大小
        self.sysfonts=pygame.font.get_fonts()# 所有系统字体
        self.sysfontname=self.sysfonts[-1]# 设置系统字体
        

    def __setattr__(self, name, value) -> None:
        '重写设置属性的方法'
        self.__dict__[name] = value
        if not name in ['sysfonts','styles','fonts']:
            self.styles[name] = value


class Master:
    def __init__(self, data_path='data.dat') -> None:
        '管家类，负责一些管理类的功能'
        self._fullscreen = False
        self.data_path = data_path
        self.load_data()
        self.data.temp = ''
        self.app = App(visible=False)
        self.mod = sys.modules['__main__']

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

    def load_data(self):
        '加载数据'
        if os.path.isfile(self.data_path):
            with open(self.data_path, 'rb') as f:
                self.data = pickle.load(f)
                # print(f'{self.data_path}加载成功！')
                return 1
        else:
            # print(f'{self.data_path}加载失败！')
            self.data = Data()
            return 0

    def sava_data(self):
        '保存数据'
        try:
            with open(self.data_path, 'wb') as f:
                pickle.dump(self.data, f)
                print(f'{self.data_path}保存成功！')
                return 1
        except:
            print(f'{self.data_path}保存失败！')
            return 0

    def del_data(self):
        '删除数据'
        try:
            os.remove(self.data_path)
            print(f'{self.data_path}删除成功')
            return 1
        except:
            print(f'{self.data_path}不存在')
            return 0

    def msg(self, msg='这是提示信息'):
        '提示信息'
        guizero.info('提示', msg, master=self.app)

    def warning(self, msg='这是警告信息'):
        '警告信息'
        guizero.warn('警告', msg, master=self.app)

    def error(self, msg='这是错误信息'):
        '错误信息'
        guizero.error('错误', msg, master=self.app)


class Actor(Actor):

    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        '新的角色类'
        self._flip_x = False
        self._flip_y = False
        self._scale = 1
        self._mask = None
        self._taskid = 0
        self._animate_counter = 0  # 切换造型动画的计数
        self._images = [image]
        self.animate_fps = 10  # 切换造型的频率，默认是10，表示1s切换10次
        self.is_animate = 1
        self.maxfps = 120  # 角色响应任务事件的最大帧率，创建任务的时候每s可以有120个间隔来执行任务
        self.direction = 0
        self.tasks = {}
        super().__init__(image, pos, anchor, **kwargs)

    def distance_to(self, actor):
        '计算到另一个角色的距离'
        dx = actor.x - self.x
        dy = actor.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def direction_to(self, actor):
        '计算面向另一个角色的方向'
        dx = actor.x - self.x
        dy = self.y - actor.y

        angle = math.degrees(math.atan2(dy, dx))
        if angle > 0:
            return angle

        return 360 + angle

    def move_towards(self, actor, dist):
        '朝另一个角色移动dist步'
        angle = math.radians(self.direction_to(actor))
        dx = dist * math.cos(angle)
        dy = dist * math.sin(angle)
        self.x += dx
        self.y -= dy

    def point_towards(self, actor):
        '面向另一个角色'
        print(self.direction_to(actor))
        self.angle = self.direction_to(actor)

    def move_in_direction(self, dist):
        '朝着当前方向移动dist步，不是角色角度'
        angle = math.radians(self.direction)
        dx = dist * math.cos(angle)
        dy = dist * math.sin(angle)
        self.x += dx
        self.y -= dy

    def move_forward(self, dist):
        '演着角色角度移动dist步'
        angle = math.radians(self.angle)
        dx = dist * math.cos(angle)
        dy = dist * math.sin(angle)
        self.x += dx
        self.y -= dy

    def move_left(self, dist):
        '朝当前角度的左边移动dist步'
        angle = math.radians(self.angle + 90)
        dx = dist * math.cos(angle)
        dy = dist * math.sin(angle)
        self.x += dx
        self.y -= dy

    def move_right(self, dist):
        '朝当前角度的右边移动dist步'
        angle = math.radians(self.angle - 90)
        dx = dist * math.cos(angle)
        dy = dist * math.sin(angle)
        self.x += dx
        self.y -= dy

    def move_back(self, dist):
        '倒退dist步'
        angle = math.radians(self.angle)
        dx = -dist * math.cos(angle)
        dy = -dist * math.sin(angle)
        self.x += dx
        self.y -= dy

    @property
    def images(self):
        '设置造型列表'
        return self._images

    @images.setter
    def images(self, images):
        '设置造型列表'
        self._images = images
        if len(self._images) != 0:
            self.image = self._images[0]

    def next_image(self):
        '下一个造型'
        if self.image in self._images:
            current = self._images.index(self.image)
            if current == len(self._images) - 1:
                self.image = self._images[0]
            else:
                self.image = self._images[current + 1]
        else:
            self.image = self._images[0]

    def toggle_animate(self):
        '切换角色是否自动切换造型'
        if self.is_animate:
            self.is_animate = 0
        else:
            self.is_animate = 1

    def animate(self):
        '''
        切换造型动画
        self.animate_fps为切换的频率，默认是10，表示1s切换10次
        '''
        if self.is_animate:
            if self.animate_fps < 0:
                self.animate_fps = 0
            now = int(time.time() * self.animate_fps)
            if now != self._animate_counter:
                self._animate_counter = now
                self.next_image()

    def run_tasks(self):
        '''
        根据计划任务执行要做的事
        需要放在update函数中执行
        '''
        self.animate()
        now = int(time.time() * self.maxfps)  # 获取当前绝对帧数
        # 如果任务过期就执行并删除
        for taskCounter in list(self.tasks):
            if taskCounter <= now:
                for taskid in self.tasks[taskCounter]:
                    self.tasks[taskCounter][taskid]()
                    # print(f'任务{taskid}执行完毕')
                del self.tasks[taskCounter]
            else:
                break

    def create_delay_tasks(self, task, seconds=1, times=1):
        '''
        创建任务队列并添加到角色的任务列表中。  
        延迟seconds秒执行task任务，times代表这个任务执行多少次
        不写第二个和第三个参数就是等待1秒执行1次task
        '''
        now = time.time()
        tasks = []
        for i in range(times):
            taskTime = now+(i+1)*seconds  # 计算执行任务的时间
            taskCounter = int(taskTime*self.maxfps)  # 计算计数器走到哪一帧
            self._taskid += 1
            # 将任务加到任务队列
            if taskCounter in self.tasks:
                self.tasks[taskCounter][self._taskid] = task
            else:
                self.tasks[taskCounter] = {self._taskid: task}
            tasks.append(self._taskid)  # 将任务加到任务列表用于返回
        return tasks

    def remove_taskById(self, id):
        '根据id删掉任务'
        index = None
        for i in self.tasks:
            if id in self.tasks[i]:
                del self.tasks[i][id]
                # print(f'任务{id}被取消')
                break

    @property
    def angle(self):
        '设置角度'
        return self._angle

    @angle.setter
    def angle(self, angle):
        '设置角度'
        self._angle = angle
        self._transform_surf()

    @property
    def scale(self):
        '设置缩放'
        return self._scale

    @scale.setter
    def scale(self, scale):
        '设置缩放'
        self._scale = scale
        self._transform_surf()

    @property
    def flip_x(self):
        '设置x方向翻转'
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flip_x):
        '设置x方向翻转'
        self._flip_x = flip_x
        self._transform_surf()

    @property
    def flip_y(self):
        '设置x方向翻转'
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flip_y):
        '设置y方向翻转'
        self._flip_y = flip_y
        self._transform_surf()

    @property
    def image(self):
        '设置造型'
        return self._image_name

    @image.setter
    def image(self, image):
        '设置当前造型'
        self._image_name = image
        self._orig_surf = self._surf = loaders.images.load(image)
        self._update_pos()
        self._transform_surf()

    def _transform_surf(self):
        '变换角色的缩放、翻转等'
        self._surf = self._orig_surf
        p = self.pos

        if self._scale != 1:
            size = self._orig_surf.get_size()
            self._surf = pygame.transform.scale(
                self._surf, (int(size[0] * self.scale), int(size[1] * self.scale)))
        if self._flip_x:
            self._surf = pygame.transform.flip(self._surf, True, False)
        if self._flip_y:
            self._surf = pygame.transform.flip(self._surf, False, True)

        self._surf = pygame.transform.rotate(self._surf, self._angle)

        self.width, self.height = self._surf.get_size()
        w, h = self._orig_surf.get_size()
        ax, ay = self._untransformed_anchor
        anchor = transform_anchor(ax, ay, w, h, self._angle)
        self._anchor = (anchor[0] * self.scale, anchor[1] * self.scale)

        self.pos = p
        self._mask = None

    def collidepoint_pixel(self, x, y=0):
        '检测碰撞到某个像素，像素级精确检测'
        if isinstance(x, tuple):
            y = x[1]
            x = x[0]
        if self._mask == None:
            self._mask = pygame.mask.from_surface(self._surf)

        xoffset = int(x - self.left)
        yoffset = int(y - self.top)
        if xoffset < 0 or yoffset < 0:
            return 0

        width, height = self._mask.get_size()
        if xoffset > width or yoffset > height:
            return 0

        return self._mask.get_at((xoffset, yoffset))

    def collide_pixel(self, actor):
        '检测碰撞其他某个角色，返回重叠的坐标，如果没重叠就直接返回None，像素级精确检测'
        for a in [self, actor]:
            if a._mask == None:
                a._mask = pygame.mask.from_surface(a._surf)

        xoffset = int(actor.left - self.left)
        yoffset = int(actor.top - self.top)

        return self._mask.overlap(actor._mask, (xoffset, yoffset))

    def collidelist_pixel(self, actors):
        '检测碰撞角色列表，返回碰撞到的角色的索引，没碰到返回None，像素级精确检测'
        for i in range(len(actors)):
            if self.collide_pixel(actors[i]):
                return i
        return None

    def collidelistall_pixel(self, actors):
        '检测碰撞角色列表，返回值是碰撞到的角色，返回一个列表，如果列表为空说明没碰到，像素级精确检测'
        collided = []
        for i in range(len(actors)):
            if self.collide_pixel(actors[i]):
                collided.append(i)
        return collided

    def obb_collidepoints(self, actors):
        '检测多个角色碰撞，旋转了rect，使得rect贴合角色'
        angle = math.radians(self._angle)
        costheta = math.cos(angle)
        sintheta = math.sin(angle)
        width, height = self._orig_surf.get_size()
        half_width = width / 2
        half_height = height / 2

        i = 0
        for actor in actors:
            tx = actor.x - self.x
            ty = actor.y - self.y
            rx = tx * costheta - ty * sintheta
            ry = ty * costheta + tx * sintheta

            if rx > -half_width and rx < half_width and ry > -half_height and ry < half_height:
                return i
            i += 1

        return -1

    def obb_collidepoint(self, x, y=0):
        '检测碰撞一个点，旋转了rect，使得rect贴合角色'
        if isinstance(x, tuple):
            y = x[1]
            x = x[0]
        angle = math.radians(self._angle)
        costheta = math.cos(angle)
        sintheta = math.sin(angle)
        width, height = self._orig_surf.get_size()
        half_width = width / 2
        half_height = height / 2

        tx = x - self.x
        ty = y - self.y
        rx = tx * costheta - ty * sintheta
        ry = ty * costheta + tx * sintheta

        if rx > -half_width and rx < half_width and ry > -half_height and ry < half_height:
            return True

        return False

    def circle_collidepoints(self, radius, actors):
        '检测碰撞一堆点，将角色变成圆形区域，适合于圆形角色的碰撞检测'
        rSquare = radius ** 2

        i = 0
        for actor in actors:
            dSquare = (actor.x - self.x)**2 + (actor.y - self.y)**2

            if dSquare < rSquare:
                return i
            i += 1

        return -1

    def circle_collidepoint(self, radius, x, y=0):
        '检测碰撞一个点，将角色变成圆形区域，适合于圆形角色的碰撞检测'
        if isinstance(x, tuple):
            y = x[1]
            x = x[0]
        rSquare = radius ** 2
        dSquare = (x - self.x)**2 + (y - self.y)**2

        if dSquare < rSquare:
            return True

        return False

    def draw(self):
        '绘图'
        game.screen.blit(self._surf, self.topleft)

    def get_rect(self):
        '获取角色的rect'
        return self._rect


if __name__ == '__main__':
    font = FontStyle()
    font.color = 'red'
    print(font.sysfonts)
