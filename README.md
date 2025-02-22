project main: MonieShop Transaction Analysis

Project Goal : To process all these transaction files (2024 in total, across multiple subfolders) and produce five key analytics:
	1.	Highest sales volume in a day
	2.	Highest sales value in a day
	3.	Most sold product ID by volume
	4.	Highest sales staff ID for each month
	5.	Highest hour of the day by average transaction volume


Problem solving approach:
1. Reading Through the Multiple Transaction Files
	•	within The main() function:
	1.	Defines a base folder ( mp-hackathon-sample-data).
	2.	Locates all subfolders in that base directory (e.g., test-case-1, test-case-2, etc.).
	3.	For each subfolder, i keep and counts the .txt files and then calls analyze_transaction_data(subfolder).
	4.	After all subfolders are processed, i checks whether the total number of .txt files is 2024 (as expected).

Why this matters:
	•	The problem states there are 2024 daily transaction files. This considered solution ensures the python script can traverse multiple folders (each containing one or more daily .txt files), summing up the overall file count while generating analytics per subfolder.

2. Parsing Each Transaction
	•	The format_transaction_record(line) function:
	1.	Splits a line by commas into four parts:
	•	salesStaffId, transactionTime, products, saleAmount
	2.	Converts strings to their proper datatypes (int, float, datetime)
	3.	Calls extra_products_details(products_str) to extract the product details:
	•	Splits the bracketed string [productId:qty|...]
	•	Returns a dictionary of {productId: quantity} and a total quantity.
	4.	Returns a structured transaction dictionary.

Why this matters:
	•	Each .txt file can have many lines, each representing a single transaction. Parsing ensures each transaction is turned into a consistent Python object with salesStaffId, transactionTime, products, totalItems, and saleAmount.

 3. compile the transaction data and Analyze it
	•	The analyze_transaction_data(folder_path) function:
	1.	Iterates through each .txt file in the given folder.
	2.	For every valid transaction line (parsed via format_transaction_record), the code accumulates the data in several dictionaries:
	•	daily_volume: Tracks how many items sold per day.
	•	daily_value: Tracks total sales value (money) per day.
	•	product_volume: Tracks cumulative quantity per product ID across all transactions.
	•	staff_sales_month: Tracks total sales amount by (year, month, staffId).
	•	hour_items_sold and hour_transaction_count: Track items sold and transaction count for each hour (0–23).
	3.	These accumulations happen line-by-line so that, by the time all files have been read, you have a complete view of daily, monthly, hourly, and product-based totals.

Why this matters:
	•	The problem requires multiple metrics at different levels (day, month, product, hour).

4. Computing the Five Required Metrics

After reading all files and populating the dictionaries, i computed the required metrics:
	1.	Highest Sales Volume in a Day:
	•	Finds the day in daily_volume with the maximum total items sold (max(daily_volume, key=daily_volume.get)).
	2.	Highest Sales Value in a Day:
	•	Finds the day in daily_value with the maximum sum of sale amounts.
	3.	Most Sold Product by Volume:
	•	Locates the product ID in product_volume with the highest cumulative quantity.
	4.	Highest Sales Staff ID per Month:
	•	Re-maps (year, month, staffId) into a dictionary, then for each (year, month) picks the staff ID with the highest total.
	5.	Highest Hour by Average Transaction Volume:
	•	Uses hour_items_sold[hour] / hour_transaction_count[hour] to find which hour has the largest average number of items per transaction.


How to Test Script ?
## please run : python monieshop-analytics.py on the terminal.

Thank you!