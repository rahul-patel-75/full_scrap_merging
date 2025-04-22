import pandas as pd


# Load the Excel file
file_path = r"C:\Users\Desk0012\Downloads\output_with_flags.xlsx"
df = pd.read_excel(file_path,sheet_name='Sheet2')




priority_order = [
    # Tier 1 – Highly Reliable
    "practo.com",
    "lybrate.com",
    "apollo247",
    "bajajfinservhealth",
    "myupchar.com",
    "medibuddy.in",
    "credihealth.com",

    # Tier 2 – Moderately Reliable
    "skedoc.com",
    "doctoriduniya.com",
    "sehat.com",
  
    "deldure.com",
    "ask4healthcare",
    "hexahealth.com",
    "meddco.com",

    # Tier 3 – Limited Reliability
    "lazoi.com",
    "quickerala.com",
    "patakare.com",
    "docindia.org",
    "mymedisage.com",
    "drlogy.com",
    "doctor360",
    "ihindustan.com",
    "healthfrog",
    "www.drdata",

    # Tier 4 – Low Trust / Unclear
    "prescripson.com",
    "curofy.com",
    "justdialdds.com",
    "converse.rgcross.com",
    "healthworldhospitals.com",
    "healthgrades.com"
]
# Create a priority map
priority_map = {domain: i for i, domain in enumerate(priority_order)}
default_priority = len(priority_order) + 1

# Function to find domain priority from URL
def get_priority_from_url(url):
    for domain, priority in priority_map.items():
        if domain in url:
            return priority
    return default_priority

# Apply the function to the DataFrame
df["priority"] = df["url"].apply(get_priority_from_url)

# Sort by priority and URL
df = df.sort_values(by=["priority", "url"]).reset_index(drop=True)





# Ensure column names are clean
df.columns = df.columns.str.strip()

# Identify main columns (excluding the first 'url' column)
base_columns = df.columns.tolist()
url_col = 'url'
record_id_col = 'record_id'
url_base_index = df.columns.get_loc(url_col)

# Group by record_id
merged_rows = []

for record_id, group in df.groupby(record_id_col):
    merged_row = group.iloc[0].copy()

    # Fill missing values in the merged_row using all rows in the group
    for _, row in group.iterrows():
        for col in df.columns:
            if pd.isna(merged_row[col]) or merged_row[col] == '':
                if not pd.isna(row[col]) and row[col] != '':
                    merged_row[col] = row[col]

    # Collect all URLs (from all rows of this group)
    urls = group[url_col].dropna().unique().tolist()
    if urls:
        merged_row[url_col] = urls[0]  # first URL in 'url' column
        for i, extra_url in enumerate(urls[1:], start=2):
            merged_row[f"url_{i}"] = extra_url

    merged_rows.append(merged_row)

# Create final DataFrame
final_df = pd.DataFrame(merged_rows)

# Save to Excel
output_path = r"C:\Users\Desk0012\Downloads\final_GSK_gp_rem_250_merging_after_merging.csv"
final_df.to_csv(output_path, index=False)
