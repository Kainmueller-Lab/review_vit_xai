import pandas as pd
import matplotlib.pyplot as plt 
from pywaffle import Waffle
from matplotlib.colors import ListedColormap
from pywaffle import Waffle
import json 
import numpy as np 
import seaborn as sns

taxonomy = json.load(open("taxonomy.json"))
METHODS_TABLE = 'tables/method_table_clean.csv'
data = pd.read_csv(METHODS_TABLE)

#tax = "Class-specificity"
#tax_idx = 1

colors = ["seagreen", "lavender", "cyan", "lightblue", "teal", "orange", "green", "brown"]


plt.figure(figsize=(16, 8))
for tax_idx, tax in enumerate(taxonomy): 

    plt.subplot(2,4,tax_idx+1)
    my_data = data[taxonomy[tax]].sum()
    print(my_data)

    ax = sns.barplot(data=my_data, orient="h", edgecolor="black", 
                    palette=sns.light_palette(colors[tax_idx], n_colors=len(my_data)), 
                    width=0.5)

    for idx, label in enumerate(taxonomy[tax]):  
        plt.text(x=0, y=idx, s= label, size=12)

    plt.setp(ax.patches, linewidth=3) 
    ax.spines[['left', 'bottom']].set_linewidth(3)
    ax.spines[['right', 'top']].set_visible(False)
    ax.set_yticks([])
    plt.xticks(size=14)
    plt.title(tax, size=14)


plt.savefig("figures/methods_per_category.pdf")
plt.show()