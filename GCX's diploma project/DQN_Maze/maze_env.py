import scipy.io as scio
import numpy
import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 1    # 单位格子边长(占1个像素)
class Maze(tk.Tk, object):
    def __init__(self, maze_h, maze_w, index,):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.n_features = 2
        self.title('maze')
        self.MAZE_H = maze_h  # 纵向格子数量
        self.MAZE_W = maze_w  # 横向格子数量
        self.index = index
        self.geometry('{0}x{1}'.format(self.MAZE_H * UNIT, self.MAZE_H * UNIT))
        self._build_maze()


    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=self.MAZE_H * UNIT,
                           width=self.MAZE_W * UNIT)

        # create grids 由于处理的是图片，绘制网点将会非常密集，遂移除
        # for c in range(0, MAZE_W * UNIT, UNIT):
        #     x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
        #     self.canvas.create_line(x0, y0, x1, y1)
        # for r in range(0, MAZE_H * UNIT, UNIT):
        #     x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
        #     self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # hell
        hell1_center = origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - UNIT, hell1_center[1] - UNIT,
            hell1_center[0] + UNIT, hell1_center[1] + UNIT,
            fill='black')
        # hell
        # hell2_center = origin + np.array([UNIT, UNIT * 2])
        # self.hell2 = self.canvas.create_rectangle(
        #     hell2_center[0] - 15, hell2_center[1] - 15,
        #     hell2_center[0] + 15, hell2_center[1] + 15,
        #     fill='black')

        # create oval
        # oval_center = origin + UNIT * 2
        # self.oval = self.canvas.create_oval(
        #     oval_center[0] - UNIT, oval_center[1] - UNIT,
        #     oval_center[0] + UNIT, oval_center[1] + UNIT,
        #     fill='yellow')

        # 图片路径
        FilePath = 'D:\\pythonProject\\edgeDetection\\dataset\\data\\'
        KeyName = 'loc{}'.format(self.index)
        locPath = FilePath + KeyName

        # 读入奖励点坐标数据
        loc = scio.loadmat(locPath).get('loc{}'.format(self.index)).tolist()

        # 尝试改写create oval
        # oval_center = origin + UNIT * 2
        Row = numpy.size(loc, 0)
        for row in range(Row):
            self.oval = self.canvas.create_oval(
                loc[row][1] - UNIT, loc[row][0] - UNIT,
                loc[row][1] + UNIT, loc[row][0] + UNIT,
                fill='yellow')


        # create red rect
        rect_center = np.array([loc[100][0], loc[100][1]])
        self.rect = self.canvas.create_rectangle(
            rect_center[0] - UNIT, rect_center[1] - UNIT,
            rect_center[0] + UNIT, rect_center[1] + UNIT,
            fill='red')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 5, origin[1] - 5,
            origin[0] + 5, origin[1] + 5,
            fill='red')
        # return observation
        return (np.array(self.canvas.coords(self.rect)[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(self.MAZE_H*UNIT)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (self.MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (self.MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        next_coords = self.canvas.coords(self.rect)  # next state
        # print(next_coords)

        # reward function
        if next_coords == self.canvas.coords(self.oval):
            self.rect = self.canvas.create_rectangle(
                next_coords[0]+50, next_coords[1]+50,
                next_coords[2]+50, next_coords[3]+50,
                fill='red')
            reward = 1
            done = True
        elif next_coords in [self.canvas.coords(self.hell1)]:
            self.rect = self.canvas.create_rectangle(
                next_coords[0]+50, next_coords[1]+50,
                next_coords[2]+50, next_coords[3]+50,
                fill='red')
            reward = -1
            done = True
        else:
            reward = 0
            done = False
        s_ = (np.array(next_coords[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(self.MAZE_H*UNIT)
        return s_, reward, done

    def render(self):
        # time.sleep(0.01)
        self.update()