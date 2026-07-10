
import pandas as pd
import json

METHODS_TABLE = 'tables/(Vision) Transformer XAI Paper Overview - Taxonomy Table v4.csv'
EVAL_TABLE = 'tables/(Vision) Transformer XAI Paper Overview - Evaluation Table Edited.csv'

######################################################################################
# METHODS Table
######################################################################################

# read original data 
data = pd.read_csv(METHODS_TABLE, header = 1)

# load taxonomy
taxonomy = json.load(open("taxonomy.json"))

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

# remove not-needed columns 
print("Columns: ", data.columns)
data.drop(['Fantozzi', 'Kashefi', 'Stassin', 'Unnamed: 33'], axis=1, inplace=True)

# rename columns to match with eval-table 
data.rename({"Short Name Identifier":"Method"}, axis=1, inplace=True)

# remove un-needed rows 
data = data[data["Year"]>2000]

#remove trailing whitespace
data["Method"] = data["Method"].str.rstrip()



# print summary 
for key, value in taxonomy.items():
    print(f"{key}: {len(value)} methods")

print("Years covered:", data["Year"].unique())
print(f"{len(data)} unique methods in methods table: {list(data['Method'])}")


# save to csv
data.to_csv("tables/method_table_clean.csv", index=False)


######################################################################################
# EVAL Table
######################################################################################

evals = pd.read_csv(EVAL_TABLE)
evals = evals.replace({'NaN': 0, " " : 0, "?" : 0, 'x': 1}).fillna(0)

for col in ['localization', 'only localization', 'Perturbation', 'only qualitative', 'User Study']:
    try:
        numeric_col = pd.to_numeric(evals[col], errors='raise') # attempts to convert the column to numeric, raises an error if it fails
        if (numeric_col % 1 == 0).all(): # checks if all values are integers
            evals[col] = numeric_col.astype(int)
        else:
            evals[col] = numeric_col
    except (ValueError, TypeError) as e:
        # If conversion fails, print the error message and the column name
        print(f"Could not convert column '{col}' to numeric. Error: {e}")
        print(col)
        pass

evals = evals[evals["Method"].str.len()>1]

evals.columns = ['Method', 'eval_models', 'eval_dataset', 'eval_baselines', 'eval_metrics', 'localization',
       'only localization', 'perturbation', 'only qualitative', 'user study']
#remove trailing whitespace
evals["Method"] = evals["Method"].str.rstrip()

print(f"{len(evals)} unique methods in eval table: {list(evals['Method'])}")

# save to csv
evals.to_csv("tables/eval_table_clean.csv", index=False)


######################################################################################
# MERGED Table
######################################################################################

print("Methods in method table but not in eval table ", set(data["Method"]).difference(set(evals["Method"])))



merged = pd.merge(data, evals, how="outer")
print(f"{len(merged)} unique methods in merged table: {list(merged['Method'])}")
merged.to_csv("tables/merged_table_clean.csv", index=False)