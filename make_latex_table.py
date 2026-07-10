import pandas as pd
#from itertools import groupby
import json 



TABLE_FILE = "tables/method_table_clean.csv"
TAXONOMY_FILE = "taxonomy.json"
# table is divided into Post-hoc and Ante-hoc methdos 
STAGE = "Ante-hoc"


data = pd.read_csv(TABLE_FILE)
print("Data columns ", data.columns)

# add citation key
data["Method"] = data["Method"] + r" \cite{" + data["Citation Key"] + "}"
data.drop(["Citation Key"], axis=1, inplace=True)

# filter by stage 
data = data[data[STAGE] ==1]
data.drop(["Post-hoc", "Ante-hoc"], axis=1, inplace=True)

# load taxonomy
taxonomy = json.load(open("taxonomy.json"))



#################################################################################
# Define Column Format 
#################################################################################

column_format = "ll|"  # first column (e.g. row labels)

for i, (meta, subgroups) in enumerate(taxonomy.items()):
    column_format += "c" * len(subgroups)

    # add spacing between meta-groups, but not after the last one
    if i < len(taxonomy) - 1:
        #column_format += r"@{\hspace{20pt}}"
        column_format += r"|"
        #column_format +=r"!{\vrule width 0.3pt}"

print(column_format)


#################################################################################
# Define Meta Header
#################################################################################

meta_header = []

for meta, subgroups in taxonomy.items():
    meta_header.append(
        rf"\multicolumn{{{len(subgroups)}}}{{c|}}{{{meta}}}"
    )

meta_header = "&&" +" & ".join(meta_header) 


#################################################################################
# Define Meta Header
#################################################################################

# roatate taxonomy categories
headers = "&"+" & ".join([r"\rotatebox{90}{" + col + "}" for col in data.columns[1:]])

# convert table to latex
latex = data.replace({0:"", 1:"x"}).to_latex(index=False, header=False, column_format=column_format)

# place empty line between different years 
years = data["Year"].values
lines = latex.split("\n")
new_lines = []
for i, line in enumerate(lines):
    #print(line)
    new_lines.append(line)
    i_year = i-3
    if i_year < len(years)-1 and years[i_year+1] != years[i_year]:
        #print("hi")
        new_lines.append(r"\addlinespace")
latex = "\n".join(new_lines)


# put header and meta-header on table 
latex = latex.replace(
    r"\toprule",
   "\n" + headers + r"\\" + "\n" + meta_header + r" \\" 
)


with open(f"latex/table_{STAGE.lower()}.tex", "w") as text_file:
    text_file.write(latex)