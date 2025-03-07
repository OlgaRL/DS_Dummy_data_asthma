# %% load packages
import pandas as pd
import numpy as np
import json
import ast
from datetime import datetime
from collections import defaultdict
from datetime import datetime
# %%

## load data

with open("C:\\Users\\Olga_\\OneDrive\\Documents\\Olga Documents\\my projects and summary\\sample tasks\\drug-label-0001-of-0013.json\drug-label-0001-of-0013.json", "r") as file:
    data = json.load(file)
   


# %% Extract and structure relevant information from JSON records

resultsListDict = data.get("results") # relevant records are stored in results

# %% filter dataset to the required fields 
filtered_data = [
      {
          "effective_time": entry.get("effective_time"),
          #"spl_product_data_elements": entry.get("spl_product_data_elements"),
          "manufacturer": entry.get("openfda", {}).get("manufacturer_name"),
          "route": entry.get("openfda", {}).get("route"),
          "substance_name": entry.get("openfda",{}).get("substance_name"),
          "brand_name": entry.get("openfda",{}).get("brand_name"),
      } for entry in data.get("results", [])
  ]

df = pd.DataFrame(filtered_data) # convert to dataframe
df["date"] = pd.to_datetime(df["effective_time"], format="%Y%m%d")
df["num_substances"] = df["substance_name"].apply(lambda x: len(x) if isinstance(x, list) else 0)
df["route"] = df["route"].apply(lambda x: ",".join(x) if isinstance(x, list) else str(x))
df["year"] = df["date"].dt.year
df["drug_name"] = df["brand_name"].apply(lambda x: ",".join(x) if isinstance(x, list) else str(x))
# %% Calculate the average number of substances per drug name
df_avg = df.groupby(["drug_name","year","route"], as_index=False)["num_substances"].mean()

# Rename the column for clarity
df_avg.rename(columns={"num_substances": "avg_num_substances"}, inplace=True)

# Print the result
print(df_avg)
# %%