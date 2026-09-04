# Converting `.xlsx` to `.csv`
import pandas as pd

input_file = "../data/zepto_v1.xlsx";
output_file = "../data/zepto_v1.csv";

cnvrt = pd.read_excel(input_file);

cnvrt.to_csv(output_file, index=False)

print(f"Converted {len(cnvrt)} rows to {output_file}")