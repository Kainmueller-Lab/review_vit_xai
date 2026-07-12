import pandas as pd
import json


TABLE_FILE = "tables/method_table_clean.csv"
TAXONOMY_FILE = "taxonomy.json"

# table is divided into Post-hoc and Ante-hoc methods
STAGE = "Post-hoc"


data = pd.read_csv(TABLE_FILE)
print("Data columns ", data.columns)

# add citation key
data["Method"] = data["Method"] + r" \cite{" + data["Citation Key"] + "}"
data.drop(["Citation Key"], axis=1, inplace=True)

# filter by stage
data = data[data[STAGE] == 1]
data.drop(["Post-hoc", "Ante-hoc"], axis=1, inplace=True)


# load taxonomy
taxonomy = json.load(open(TAXONOMY_FILE))


#################################################################################
# Remove taxonomy categories that are no longer in the dataframe
#################################################################################

filtered_taxonomy = {}

for meta, subgroups in taxonomy.items():
    remaining = [s for s in subgroups if s in data.columns]
    if remaining:
        filtered_taxonomy[meta] = remaining

taxonomy = filtered_taxonomy


#################################################################################
# Define Column Format
#################################################################################

column_format = "ll|"  # Method + Year

for i, (meta, subgroups) in enumerate(taxonomy.items()):
    column_format += "c" * len(subgroups)

    # add spacing between meta-groups, but not after the last one
    if i < len(taxonomy) - 1:
        column_format += "|"

print("Column format:", column_format)


#################################################################################
# Define Meta Header
#################################################################################

meta_header = []

for meta, subgroups in taxonomy.items():
    meta_header.append(
        rf"\multicolumn{{{len(subgroups)}}}{{c|}}{{{meta}}}"
    )

# two empty columns for Method and Year
meta_header = "&&" + " & ".join(meta_header)


#################################################################################
# Define rotated taxonomy headers
#################################################################################

taxonomy_columns = [
    col
    for subgroups in taxonomy.values()
    for col in subgroups
]

headers = (
    data.columns[0]  # Method
    + " & "
    + data.columns[1]  # Year
    + " & "
    + " & ".join(
        rf"\rotatebox{{90}}{{{col}}}"
        for col in taxonomy_columns
    )
)


#################################################################################
# Convert table to LaTeX
#################################################################################

latex = data.replace({0: "", 1: "x"}).to_latex(
    index=False,
    header=False,
    column_format=column_format
)


#################################################################################
# Place empty line between different years
#################################################################################

years = data["Year"].values

lines = latex.split("\n")
new_lines = []

for i, line in enumerate(lines):
    new_lines.append(line)

    i_year = i - 3

    if i_year < len(years) - 1 and years[i_year + 1] != years[i_year]:
        new_lines.append(r"\addlinespace")

latex = "\n".join(new_lines)


#################################################################################
# Insert custom headers
#################################################################################

latex = latex.replace(
    r"\toprule",
    "\n"
    + headers
    + r"\\"
    + "\n"
    + meta_header
    + r" \\"
)


#################################################################################
# Write output
#################################################################################

with open(f"latex/table_{STAGE.lower()}.tex", "w") as text_file:
    text_file.write(latex)