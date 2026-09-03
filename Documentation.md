## Step1 - Data Audits 
import pandas as pd

df = pd.read_excel("../data/zepto_v1.xlsx")

print("\n--- SHAPE ---")
print(df.shape)

print("\n--- COLUMNS ---")
print(df.columns.tolist())

print("\n--- FRIST 5 ROWS ---")
print(df.head())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATES ---")
print("Duplicate rows:", df.duplicated().sum())

print("\n--- SUMMARY ---")
print(df.describe(include="all"))

## Step2 - SQL Insertion 
CREATE DATABASE quickcommerce; 

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category TEXT,
    name TEXT,
    mrp NUMERIC,
    discount_percent NUMERIC,
    available_quantity INTEGER,
    discounted_selling_price NUMERIC,
    weight_in_gms INTEGER,
    out_of_stock BOOLEAN,
    quantity INTEGER
);

\l             → databases
\c database    → connect/select database
\dt            → tables
\d products    → table structure
SELECT ...     → actual data

### Query
SELECT category, name, mrp, discount_percent, available_quantity, discounted_selling_price, weight_in_gms, out_of_stock, quantity, COUNT(*) AS duplicate_count FROM products GROUP BY category, name, mrp, discount_percent, available_quantity, discounted_selling_price, weight_in_gms, out_of_stock, quantity HAVING COUNT(*) > 1;

### Output
"Paan Corner"	"Listerine Cool Mint Mouthwash - Mild Taste"	15000	10	6	13500	250	false	250	2
"Personal Care"	"Listerine Cool Mint Mouthwash - Mild Taste"	15000	10	6	13500	250	false	250	2

### Query
SELECT COUNT(*) as invalid_price_records FROM products WHERE mrp <= 0 OR discounted_selling_price <= 0;

### Output
1

### Query
SELECT COUNT(*) AS invalid_inventory_records FROM products WHERE available_quantity < 0;

### Output
0

### Query
SELECT COUNT(*) AS invalid_WEIGHT_records FROM products WHERE weight_in_gms < 0;

### Output
0

### Query
SELECT
    name,
    mrp,
    discount_percent,
    discounted_selling_price,
    ROUND(
        mrp * (1 - discount_percent / 100),
        2
    ) AS calculated_price
FROM products
LIMIT 20;

### Output
"Onion"	2500	16	2100	2100.00
"Tomato Hybrid"	4200	16	3500	3528.00
"Tender Coconut"	5100	15	4300	4335.00
"Coriander Leaves"	2000	15	1700	1700.00
"Ladies Finger "	1400	14	1200	1204.00
"Potato"	3500	17	2900	2905.00
"Lemon"	7500	16	6300	6300.00
"Watermelon "	5800	15	4900	4930.00
"Capsicum Green "	2300	17	1900	1909.00
"Chilli Green "	1900	15	1600	1615.00
"Banana Robusta"	2900	17	2400	2407.00
"Garlic Indian "	1100	18	900	902.00
"Cauliflower"	2600	15	2200	2210.00
"Ginger"	1400	14	1200	1204.00
"Spinach"	1900	15	1600	1615.00
"Muskmelon"	4200	16	3500	3528.00
"Cabbage "	1500	13	1300	1305.00
"Methi"	3000	16	2500	2520.00
"Broccoli"	3600	16	3000	3024.00
"Sapota"	3000	16	2500	2520.00

### Query
SELECT
    out_of_stock,
    MIN(available_quantity) AS minimum_quantity,
    MAX(available_quantity) AS maximum_quantity,
    COUNT(*) AS products
FROM products
GROUP BY out_of_stock
ORDER BY out_of_stock;

### Output
false	1	6	3279
true	0	0	453

### Query
SELECT COUNT(*) AS inconsistent_records
FROM products
WHERE
    (out_of_stock = TRUE AND available_quantity > 0)
 OR (out_of_stock = FALSE AND available_quantity = 0);

 ### Output
 0



## Data Quality Assessment

Total records:             3,732
Missing values:            0
Exact duplicate records:   ?
Invalid prices:            ?
Invalid discounts:        ?
Invalid inventory:         ?
Pricing inconsistencies:   ?
Stock-status conflicts:    ?


## Final OutCome
### A. Overall inventory health
### Query
SELECT
    COUNT(*) AS total_products,
    COUNT(*) FILTER (WHERE out_of_stock = TRUE) AS out_of_stock_products,
    COUNT(*) FILTER (WHERE out_of_stock = FALSE) AS available_products,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE out_of_stock = TRUE)
        / COUNT(*), 2
    ) AS stockout_rate
FROM products;

### Output
3732	453	3279	12.14

### B. Stock-out by category
### Query
SELECT
    category,
    COUNT(*) AS total_products,
    COUNT(*) FILTER (WHERE out_of_stock = TRUE) AS out_of_stock_products,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE out_of_stock = TRUE)
        / COUNT(*), 2
    ) AS stockout_rate
FROM products
GROUP BY category
ORDER BY stockout_rate DESC;

### Output
"category"	"total_products"	"out_of_stock_products"	"stockout_rate"
"Biscuits"	147	42	28.57
"Beverages"	129	28	21.71
"Dairy, Bread & Batter"	129	28	21.71
"Meats, Fish & Eggs"	63	12	19.05
"Health & Hygiene"	97	13	13.40
"Munchies"	514	64	12.45
"Cooking Essentials"	514	64	12.45
"Ice Cream & Desserts"	388	45	11.60
"Chocolates & Candies"	388	45	11.60
"Packaged Food"	388	45	11.60
"Home & Cleaning"	194	19	9.79
"Fruits & Vegetables"	93	6	6.45
"Personal Care"	344	21	6.10
"Paan Corner"	344	21	6.10

### C. High-value unavailable products
### Query
SELECT
    product_id,
    name,
    category,
    mrp,
    discount_percent,
    discounted_selling_price
FROM products
WHERE out_of_stock = TRUE
ORDER BY mrp DESC
LIMIT 10;

### Output
"product_id"	"name"	"category"	"mrp"	"discount_percent"	"discounted_selling_price"
1095	"Patanjali Cow's Ghee"	"Munchies"	56500	0	56500
581	"Patanjali Cow's Ghee"	"Cooking Essentials"	56500	0	56500
3441	"MamyPoko Pants Standard Diapers, Extra Large (12 - 17 kg)"	"Paan Corner"	39900	7	36900
3097	"MamyPoko Pants Standard Diapers, Extra Large (12 - 17 kg)"	"Personal Care"	39900	7	36900
1068	"Aashirvaad Atta With Mutigrains"	"Munchies"	31500	8	28700
554	"Aashirvaad Atta With Mutigrains"	"Cooking Essentials"	31500	8	28700
1088	"Everest Kashmiri Lal Chilli Powder"	"Munchies"	31000	10	27900
574	"Everest Kashmiri Lal Chilli Powder"	"Cooking Essentials"	31000	10	27900
1060	"Madhur Pure And Hygienic Sugar"	"Munchies"	29500	9	26600
1250	"RRO Mozzarella Block Cheese"	"Dairy, Bread & Batter"	29500	50	14700

### D. Discount analysis
### Query
SELECT
    category,
    ROUND(AVG(discount_percent), 2) AS avg_discount,
    ROUND(MIN(discount_percent), 2) AS min_discount,
    ROUND(MAX(discount_percent), 2) AS max_discount
FROM products
GROUP BY category
ORDER BY avg_discount DESC;

### Output
"category"	"avg_discount"	"min_discount"	"max_discount"
"Fruits & Vegetables"	15.46	4.00	23.00
"Meats, Fish & Eggs"	11.03	0.00	50.00
"Packaged Food"	8.32	0.00	50.00
"Ice Cream & Desserts"	8.32	0.00	50.00
"Chocolates & Candies"	8.32	0.00	50.00
"Biscuits"	8.24	0.00	51.00
"Health & Hygiene"	8.05	0.00	50.00
"Beverages"	7.16	0.00	50.00
"Cooking Essentials"	7.16	0.00	50.00
"Munchies"	7.16	0.00	50.00
"Dairy, Bread & Batter"	7.16	0.00	50.00
"Personal Care"	6.25	0.00	45.00
"Paan Corner"	6.25	0.00	45.00
"Home & Cleaning"	5.68	0.00	18.00

### E. Inventory distribution
### Query
SELECT
    category,
    SUM(available_quantity) AS total_available_inventory,
    ROUND(AVG(available_quantity), 2) AS avg_inventory_per_product
FROM products
WHERE out_of_stock = FALSE
GROUP BY category
ORDER BY total_available_inventory DESC;

### Output
"category"	"total_available_inventory"	"avg_inventory_per_product"
"Munchies"	2186	4.86
"Cooking Essentials"	2186	4.86
"Packaged Food"	1521	4.43
"Ice Cream & Desserts"	1521	4.43
"Chocolates & Candies"	1521	4.43
"Personal Care"	1458	4.51
"Paan Corner"	1458	4.51
"Home & Cleaning"	839	4.79
"Beverages"	485	4.80
"Dairy, Bread & Batter"	485	4.80
"Biscuits"	448	4.27
"Health & Hygiene"	425	5.06
"Fruits & Vegetables"	275	3.16
"Meats, Fish & Eggs"	152	2.98

## 2. Now analysis has a purpose

| Business question                    | SQL output                   |
| ------------------------------------ | ---------------------------- |
| How serious is the problem?          | Overall stock-out rate       |
| Where is the problem?                | Stock-out rate by category   |
| Which products should we prioritize? | High-value stock-outs        |
| Is pricing worth reviewing?          | Average discount by category |
| Where is inventory concentrated?     | Inventory by category        |





