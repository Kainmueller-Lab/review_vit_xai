import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from pywaffle import Waffle
from matplotlib.colors import ListedColormap

import seaborn as sns
from pywaffle import Waffle

METHODS_TABLE = 'tables/method_table_clean.csv'

# read table
data = pd.read_csv(METHODS_TABLE)

print(data.head())

my_data = data[["Post-hoc", "Ante-hoc"]].sum()
print(my_data)


stage = dict(my_data)#{"post-hoc": 50, "ante-hoc": 28}
newcmp  = ListedColormap(['teal', 'coral'])


# Basic waffle
plt.figure(
  FigureClass=Waffle,
  rows=5,
  #columns=5,
  cmap_name = newcmp,
  values=stage,
  legend={'loc': 'upper left', 'bbox_to_anchor': (1.05, 1)},
)


plt.savefig("figures\methods_per_stage.pdf", bbox_inches='tight')

plt.show()