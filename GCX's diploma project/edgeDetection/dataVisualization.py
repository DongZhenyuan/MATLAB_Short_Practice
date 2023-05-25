import seaborn as sns
# sns.set()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_data():
    """
    获取数据
    """
    basecond = np.array([[18, 20, 19, 18, 13, 4, 1], [20, 17, 12, 9, 3, 0, 0], [20, 20, 20, 12, 5, 3, 0]])
    cond1 = np.array([[18, 19, 18, 19, 20, 15, 14], [19, 20, 18, 16, 20, 15, 9], [19, 20, 20, 20, 17, 10, 0]])
    cond2 = np.array([[20, 20, 20, 20, 19, 17, 4], [20, 20, 20, 20, 20, 19, 7], [19, 20, 20, 19, 19, 15, 2]])
    cond3 = np.array([[20, 20, 20, 20, 19, 17, 12], [18, 20, 19, 18, 13, 4, 1], [20, 19, 18, 17, 13, 2, 0]])
    return basecond, cond1, cond2, cond3


data = get_data()
label = ['SOB', 'CAN', 'LAP', 'DQN']
df = []
for i in range(len(data)):
    df.append(pd.DataFrame(data[i]).melt(var_name='Recall', value_name='Precision'))
    df[i]['algorithm'] = label[i]

df = pd.concat(df)     # 合并
sns.lineplot(x="Recall", y="Precision", hue="algorithm", style="algorithm", data=df)
plt.title("Award")
plt.show()
