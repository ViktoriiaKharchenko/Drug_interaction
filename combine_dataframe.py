import os
import pandas as pd

def combine_files():
    folder_path = 'C:\Disk E\drug interaction'

    combined_df = pd.DataFrame()

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            print(filename)
            file_path = os.path.join(folder_path, filename)

            df = pd.read_csv(file_path)

            combined_df = combined_df._append(df, ignore_index=True)

    combined_df.to_csv("drug_interaction.csv", index=False)

# File paths for the two CSV files
file_path1 = 'drug_class.csv'
file_path2 = 'drug_interaction.csv'

# Read the first CSV file into a DataFrame
df_class = pd.read_csv(file_path1)
df_class['Drug'] = df_class['Drug'].str.lower()
df_class['Drug'] = df_class['Drug'].str.replace('(', '').str.replace(')', '')

print(len(df_class['Drug'].unique()))
print(len(df_class['Class'].unique()))
# # Read the second CSV file into another DataFrame

df_interaction = pd.read_csv(file_path2)
df_interaction['Drug1_lower'] = df_interaction['Drug1'].str.lower()
df_interaction['Drug2_lower'] = df_interaction['Drug2'].str.lower()

df_interaction['Drug1_lower'] = df_interaction['Drug1_lower'].str.replace('(', '').str.replace(')', '')
df_interaction['Drug2_lower'] = df_interaction['Drug2_lower'].str.replace('(', '').str.replace(')', '')

print(len(df_interaction['Drug1_lower'].unique()))
print(len(df_interaction['Drug2_lower'].unique()))

drug_list = df_interaction['Drug1_lower']
drug_list = drug_list._append(df_interaction['Drug2_lower'])
print(len(drug_list.unique()))

drug_list2 = drug_list.to_frame(name='Drug')
merged_df = pd.merge(df_class, drug_list2, on='Drug', how='inner')
unique_values = merged_df.drop_duplicates(subset=['Drug', 'Class'])
print(len(unique_values['Drug'].unique()))
print(len(unique_values['Class'].unique()))

#df2 = df_interaction.rename(columns={'Drug1': 'Drug'})
#
#
# merged_df = pd.merge(df_class, df2, on='Drug', how='inner')
#
unique_values.to_csv("merged.csv", index=False)