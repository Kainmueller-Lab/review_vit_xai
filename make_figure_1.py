import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from pywaffle import Waffle
from matplotlib.colors import ListedColormap

import seaborn as sns
from pywaffle import Waffle

METHODS_TABLE = 'tables/(Vision) Transformer XAI Paper Overview - Taxonomy Table v4.csv'

####################################################################################
# prepare data 
####################################################################################

# read table
data = pd.read_csv(METHODS_TABLE, header=1)

# make table numeric
data = data.replace({'NaN': 0, " " : 0, "?" : 0, 'x': 1}).fillna(0)

for col in data.columns:
    try:
        numeric_col = pd.to_numeric(data[col], errors='raise') # attempts to convert the column to numeric, raises an error if it fails
        if (numeric_col % 1 == 0).all(): # checks if all values are integers
            data[col] = numeric_col.astype(int)
        else:
            data[col] = numeric_col
    except (ValueError, TypeError) as e:
        # If conversion fails, print the error message and the column name
        print(f"Could not convert column '{col}' to numeric. Error: {e}")
        print(col)
        pass

data = data[data["Year"]>2000]



reviews = ['Fantozzi', 'Kashefi', 'Stassin']
papers_per_review = {"ours":len(data)}

for rev in reviews: 
    papers_per_review[rev] = data[rev].sum()


papers_per_year = data.groupby(["Year"]).count()["Short Name Identifier"]



####################################################################################
# plot papers per year 
####################################################################################
ppy = list(papers_per_year.values.astype(int))
newcmp  = ListedColormap(['teal', 'white'])
N = 30

plots = []
for i, dat in enumerate(ppy): 
    plots.append({'values': [dat, N-dat],  # Convert actual number to a reasonable block number
            'title': {'label':str(dat), 'loc': 'left', 'fontsize': 12}
            })

fig = plt.figure(
    FigureClass=Waffle,
    plots={
        151: plots[0],
        152: plots[1],  
        153: plots[2],
        154: plots[3],
        155: plots[4],
    },
    rows=8,  # Outside parameter applied to all subplots, same as below
    #cols=4,
    cmap_name=newcmp, #"Accent",  # Change color with cmap
    rounding_rule='ceil',  # Change rounding rule, so value less than 1000 will still have at least 1 block
    vertical=True,  # Change orientation to vertical
    icons = ["file-lines", "truck"], 
    icon_size=12,    
    figsize=(5,3), 
)

plt.tight_layout()
plt.savefig("figures/methdos_per_year.pdf", bbox_inches='tight')
plt.show()


####################################################################################
# plot papers per review 
####################################################################################

reviews = ['Stassin',  'Fantozzi', 'Kashefi','ours']

N = 75


plots = []

for i, rv in enumerate(reviews): 
    dat = papers_per_review[rv]
    if i == 3:  # Last bar (rightmost)
        plots.append({'values': [dat, N-dat],
                'title': {'label':str(dat), 'loc': 'left', 'fontsize': 12}, 
                'rows': 15,  # 6 columns for the last bar (90 blocks / 6 cols = 15 rows)
                'cmap_name': ListedColormap(['darkslateblue', 'white'])  # Different color
                })
    else:
        plots.append({'values': [dat, N-dat],
                'title': {'label':str(dat), 'loc': 'left', 'fontsize': 12}, 
                'rows': 15,
                })

newcmp = ListedColormap(['mediumslateblue', 'white'])

fig = plt.figure(
    FigureClass=Waffle,
    plots={
        141: plots[0],
        142: plots[1],  
        143: plots[2],
        144: plots[3],
    },
    cmap_name=newcmp,
    rounding_rule='ceil',
    icons = ["file-lines", "truck"], 
    icon_size=12,
    vertical=True,
    figsize=(6,4), 
)

plt.tight_layout()
plt.savefig("figures/methdos_per_review.pdf", bbox_inches='tight')

plt.show()