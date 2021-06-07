import pandas as pd
s = pd.Series([0.0,3.6,2.0,5.8,4.2,8.0])
s.index = pd.Index([0,1,2,3,4,5])
s.index.name = 'MY_IDX'
s.name = 'MY_SERIES'
print(s)
print(s.index[-1])
print(s.values[-1])
print(s.iloc[-1])
print(s.describe())

import matplotlib.pyplot as plt
plt.title("ELLIOTT_WAVE")
plt.plot(s, 'bs--')
plt.xticks(s.index)
plt.yticks(s.values)
plt.grid(True)
plt.show()
