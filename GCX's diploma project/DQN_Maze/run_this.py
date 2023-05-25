import scipy.io as scio
import numpy
import numpy as np
from maze_env import Maze
from RL_brain import DeepQNetwork

def run_maze():
	step = 0
	# 原本的episode有300遍，这里先降为2遍
	for episode in range(2):
		print("episode: {}".format(episode))
		observation = env.reset()
		while True:
			print("step: {}".format(step))
			env.render()
			action = RL.choose_action(observation)
			observation_, reward, done = env.step(action)
			RL.store_transition(observation, action, reward, observation_)
			if (step>200) and (step%5==0):
				RL.learn()
			observation = observation_
			# 为了加速调试，这里用step的值作为判断条件
			if step > 20000:
			# if done:
				break
			step += 1
	print('game over')
	env.destroy()

if __name__ == '__main__':
	# 这个循环将依次处理 dataset 中的 .mat 文件
	# 文件的命名上以递增的数字结尾, 方便在循环中直接通过索引访问
	for index in range(5):
		# 文件路径
		FilePath = 'D:\\pythonProject\\edgeDetection\\dataset\\data\\'
		dataFile = FilePath + 'data{}.mat'.format(index)
		location = FilePath + 'loc{}.mat'.format(index)

		# data包含二值图像的完整信息, 获取图像的长宽,作为整个迷宫的尺寸
		data = scio.loadmat(dataFile).get('data{}'.format(index)).tolist()
		maze_h = numpy.size(data, 0)
		maze_w = numpy.size(data, 1)

		# 因为每一张图片的大小各不相同,迷宫尺寸也应随之更新,所以将长宽作为参数传入Maze类
		env = Maze(maze_h, maze_w, index,)
		RL = DeepQNetwork(env.n_actions, env.n_features,
						learning_rate=0.01,
						reward_decay=0.9,
						e_greedy=0.9,
						replace_target_iter=200,
						memory_size=2000
						)
		env.after(1000, run_maze)
		env.mainloop()
		# 该绘图功能尚有报错
		# RL.plot_cost()