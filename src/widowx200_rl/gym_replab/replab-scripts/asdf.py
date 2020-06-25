import matplotlib.pyplot as plt
import numpy as np
import time

time.sleep(1.0)

plt.ion()
fig, ax = plt.subplots()
x, y = [],[]
time.sleep(2)
#sc = ax.scatter(x,y)
#plt.xlim(0,10)
#plt.ylim(0,10)

plt.draw()
plt.pause(0.1)
time.sleep(2)
'''
for i in range(1000):
    x.append(np.random.rand(1)*10)
    y.append(np.random.rand(1)*10)
    sc.set_offsets(np.c_[x,y])
    fig.canvas.draw_idle()
    plt.pause(0.1)
'''
#plt.waitforbuttonpress()

