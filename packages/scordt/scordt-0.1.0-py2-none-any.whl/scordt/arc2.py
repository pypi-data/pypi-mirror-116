import numpy as np

# Function to calculate arc length
def dist(f, x0, x1):
    ret = np.sqrt((f(x1) - f(x0))**2 + (x1 - x0)**2)
    return ret

def arc_len(f, interval, n):
    l = 0
    if interval[0] == interval[1]:
        return 0
    else:
        step = ((interval[1] - interval[0]) / n)
        for i in np.arange(interval[0] + step, interval[1], step):
            l += dist(f, i, i - step)
            # print(dist(f, i, i - step))
        return l
