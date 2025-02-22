import os
from datetime import datetime
from collections import defaultdict

def extra_products_details(products_str):
    inner = products_str.strip('[]')
    if not inner:
        return {}, 0
    product_pairs = inner.split('|') 
    product_dict = {}
    total_qty = 0
    for pair in product_pairs:
        product_id_str, qty_str = pair.split(':')
        product_id = product_id_str.strip()
        quantity = int(qty_str.strip())
        product_dict[product_id] = quantity
        total_qty += quantity
    return product_dict, total_qty
 

def format_transaction_record(line):
    parts = line.split(',')
    if len(parts) != 4:
        raise ValueError(f"invalid line (expected 4 columns): {line}")

    sales_staff_id_str, transaction_time_str, products_str, sale_amount_str = [p.strip() for p in parts]

    sales_staff_id = int(sales_staff_id_str)
    sale_amount = float(sale_amount_str)
    transaction_time = datetime.fromisoformat(transaction_time_str) 

    prod_dict, total_qty = extra_products_details(products_str)

    return {
        'salesStaffId': sales_staff_id,
        'transactionTime': transaction_time,
        'products': prod_dict,
        'totalItems': total_qty,
        'saleAmount': sale_amount
    }
 

def analyze_transaction_data(folder_path):
    daily_volume = defaultdict(int)     
    daily_value = defaultdict(float)          
    product_volume = defaultdict(int)   
    staff_sales_month = defaultdict(float)
    hour_items_sold = defaultdict(int)  
    hour_transaction_count = defaultdict(int)
    
    # Process every .txt file within the folder
    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    text_file = format_transaction_record(line)
                except ValueError:
                    print(f"Skipping invalid line in {filename}: {line}")
                    continue

                day_key = text_file['transactionTime'].date()
                year = text_file['transactionTime'].year
                month = text_file['transactionTime'].month
                staff_id = text_file['salesStaffId']
                hour = text_file['transactionTime'].hour

                daily_volume[day_key] += text_file['totalItems']
                daily_value[day_key] += text_file['saleAmount']

                for product_id, qty in text_file['products'].items():
                    product_volume[product_id] += qty

                staff_sales_month[(year, month, staff_id)] += text_file['saleAmount']

                hour_items_sold[hour] += text_file['totalItems']
                hour_transaction_count[hour] += 1


    # 1) Highest sales volume in a day
    if daily_volume:
        max_volume_day = max(daily_volume, key=daily_volume.get)
        max_volume_value = daily_volume[max_volume_day]
    else:
        max_volume_day, max_volume_value = None, 0

    # 2) Highest sales value in a day
    if daily_value:
        max_value_day = max(daily_value, key=daily_value.get)
        max_value_amount = daily_value[max_value_day]
    else:
        max_value_day, max_value_amount = None, 0

    # 3) Most sold product by volume
    if product_volume:
        max_product_id = max(product_volume, key=product_volume.get)
        max_product_qty = product_volume[max_product_id]
    else:
        max_product_id, max_product_qty = None, 0

    # 4) Highest sales staff ID for each month
    monthly_staff_map = defaultdict(lambda: defaultdict(float))
    for (year, month, staff_id), amount in staff_sales_month.items():
        monthly_staff_map[(year, month)][staff_id] += amount

    # 5) Highest hour of the day by average transaction volume
    max_hour = None
    max_avg_volume = 0.0
    for hour in range(24):
        if hour_transaction_count[hour] > 0:
            avg_volume = hour_items_sold[hour] / hour_transaction_count[hour]
            if avg_volume > max_avg_volume:
                max_avg_volume = avg_volume
                max_hour = hour

    # --- display results for each subfolder ---
    print(f"\n=== Results for folder: {folder_path} ===")

    if max_volume_day is not None:
        print(f"1) Highest sales volume day: {max_volume_day} with volume={max_volume_value}")
    else:
        print("1) No data for daily volume.")
        
    if max_value_day is not None:
        print(f"2) Highest sales value day: {max_value_day} with total value={max_value_amount:.2f}")
    else:
        print("2) No data for daily value.")

    if max_product_id is not None:
        print(f"3) Most sold product: {max_product_id} with total quantity={max_product_qty}")
    else:
        print("3) No product data.")

    print("4) Highest sales staff for each (year, month):")
    if monthly_staff_map:
        for (year, month) in sorted(monthly_staff_map.keys()):
            staff_dict = monthly_staff_map[(year, month)]
            best_staff = max(staff_dict, key=staff_dict.get)
            best_amount = staff_dict[best_staff]
            print(f"   {year}-{month:02d}: Staff ID={best_staff}, Sales={best_amount:.2f}")
    else:
        print("   No staff sales data found.")

    if max_hour is not None:
        print(f"5) Highest hour by avg transaction volume: Hour={max_hour}, Avg={max_avg_volume:.2f}")
    else:
        print("5) No hourly transaction data.")

def main():
    base_folder = "./mp-hackathon-sample-data"
    if not os.path.exists(base_folder):
        print(f"ERROR: Base folder not found: {base_folder}")
        return

    subfolders = []
    for entry in os.listdir(base_folder):
        sub_path = os.path.join(base_folder, entry)
        if os.path.isdir(sub_path):
            subfolders.append(sub_path)

    if not subfolders:
        print(f"No subfolders found in {base_folder}")
        return

    total_txt_files = 0
    for folder in subfolders:
        txt_files_count = sum(1 for fn in os.listdir(folder) if fn.endswith(".txt"))
        total_txt_files += txt_files_count

        analyze_transaction_data(folder)

    if total_txt_files == 2024:
        print(f"\nAll 2024 transaction files were processed successfully!")
    else:
        print(f"\nWARNING: Expected 2024 .txt files, but found {total_txt_files}")

if __name__ == "__main__":
    main()