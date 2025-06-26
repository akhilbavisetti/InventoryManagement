import os
import sys
import pymysql
from datetime import datetime, timedelta
import random

# Add the parent directory to sys.path to import from app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import our compatible password hashing function
from app.utils.auth_helpers import safe_generate_password_hash

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Akhilraj@2005',
    'db': 'fertiliser_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def create_sample_data():
    conn = None
    try:
        # Connect to the database
        print("Connecting to MySQL database...")
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Disable foreign key checks before truncating
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Clear existing data
        tables = [
            'stock_adjustments',
            'sale_items',
            'sales',
            'purchase_items',
            'purchases',
            'products',
            'customers',
            'suppliers',
            'categories',
            'users'
        ]
        
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table}")
        
        # Re-enable foreign key checks after truncating
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        # Insert users
        print("Creating users...")
        admin_password = safe_generate_password_hash('admin123')
        staff_password = safe_generate_password_hash('staff123')
        
        cursor.execute('''
            INSERT INTO users (username, password, full_name, email, role)
            VALUES
                ('admin', %s, 'Admin User', 'admin@example.com', 'admin'),
                ('staff', %s, 'Staff User', 'staff@example.com', 'staff')
        ''', (admin_password, staff_password))
        
        # Insert categories
        print("Creating categories...")
        categories = [
            ('Urea', 'Nitrogen-rich fertilisers'),
            ('DAP', 'Diammonium phosphate fertilisers'),
            ('NPK', 'Compound fertilisers with Nitrogen, Phosphorus, and Potassium'),
            ('Potash', 'Potassium-rich fertilisers'),
            ('Organic', 'Natural and organic fertilisers')
        ]
        
        cursor.executemany('''
            INSERT INTO categories (name, description) VALUES (%s, %s)
        ''', categories)
        
        # Get category IDs
        cursor.execute('SELECT id, name FROM categories')
        category_data = cursor.fetchall()
        category_ids = {cat['name']: cat['id'] for cat in category_data}
        
        # Insert products
        print("Creating products...")
        products = [
            ('Urea 46-0-0', category_ids['Urea'], 350.00, 380.00, 'bag', 100, 20),
            ('DAP 18-46-0', category_ids['DAP'], 1200.00, 1280.00, 'bag', 80, 15),
            ('NPK 20-20-20', category_ids['NPK'], 850.00, 920.00, 'bag', 60, 15),
            ('MOP (Potash)', category_ids['Potash'], 750.00, 800.00, 'bag', 50, 10),
            ('Organic Compost', category_ids['Organic'], 280.00, 320.00, 'kg', 200, 50),
            ('Neem Cake', category_ids['Organic'], 45.00, 55.00, 'kg', 150, 30),
            ('Calcium Nitrate', category_ids['NPK'], 85.00, 95.00, 'kg', 120, 25),
            ('Single Super Phosphate', category_ids['DAP'], 420.00, 450.00, 'bag', 70, 15),
            ('Boron Fertiliser', category_ids['NPK'], 180.00, 210.00, 'kg', 40, 10),
            ('Zinc Sulphate', category_ids['NPK'], 95.00, 110.00, 'kg', 60, 15)
        ]
        
        for product in products:
            cursor.execute('''
                INSERT INTO products 
                (name, category_id, purchase_price, selling_price, unit, current_stock, min_stock_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', product)
        
        # Get product IDs
        cursor.execute('SELECT id, name FROM products')
        product_data = cursor.fetchall()
        product_ids = {prod['name']: prod['id'] for prod in product_data}
        
        # Insert customers
        print("Creating customers...")
        customers = [
            ('Rahul Sharma', '9876543210', 'rahul@example.com', '123 Farmer Colony, Delhi'),
            ('Priya Singh', '8765432109', 'priya@example.com', '456 Green Fields, Mumbai'),
            ('Amit Patel', '7654321098', 'amit@example.com', '789 Harvest Road, Ahmedabad'),
            ('Sunita Verma', '6543210987', 'sunita@example.com', '234 Crop Avenue, Jaipur'),
            ('Rajesh Kumar', '5432109876', 'rajesh@example.com', '567 Soil Street, Chennai')
        ]
        
        cursor.executemany('''
            INSERT INTO customers (name, phone, email, address)
            VALUES (%s, %s, %s, %s)
        ''', customers)
        
        # Get customer IDs
        cursor.execute('SELECT id, name FROM customers')
        customer_data = cursor.fetchall()
        customer_ids = [cust['id'] for cust in customer_data]
        
        # Insert suppliers
        print("Creating suppliers...")
        suppliers = [
            ('National Fertilisers Ltd.', 'Rajiv Mehta', '9876123450', 'nfl@example.com', 'Plot 123, Industrial Area, Delhi'),
            ('Indian Farmers Fertiliser Co-op', 'Sarita Devi', '8765123450', 'iffco@example.com', 'IFFCO Tower, Mumbai'),
            ('Krishak Bharati Co-op', 'Mohan Lal', '7654123450', 'kribhco@example.com', 'KRIBHCO Bhawan, Noida'),
            ('Coromandel International', 'Anand Kumar', '6543123450', 'coromandel@example.com', 'Coromandel House, Secunderabad'),
            ('Zuari Agro Chemicals', 'Deepak Gupta', '5432123450', 'zuari@example.com', 'Zuari Road, Goa')
        ]
        
        cursor.executemany('''
            INSERT INTO suppliers (name, contact_person, phone, email, address)
            VALUES (%s, %s, %s, %s, %s)
        ''', suppliers)
        
        # Get supplier IDs
        cursor.execute('SELECT id, name FROM suppliers')
        supplier_data = cursor.fetchall()
        supplier_ids = [sup['id'] for sup in supplier_data]
        
        # Insert purchases
        print("Creating purchases...")
        start_date = datetime.now() - timedelta(days=60)
        
        for i in range(1, 21):
            purchase_date = start_date + timedelta(days=i*3)
            supplier_id = random.choice(supplier_ids)
            ref_number = f"PO-{purchase_date.strftime('%Y%m%d')}-{i:03d}"
            
            # Create purchase header
            cursor.execute('''
                INSERT INTO purchases 
                (supplier_id, reference_number, purchase_date, total_amount, notes, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (supplier_id, ref_number, purchase_date.date(), 0, f"Stock purchase {i}", 1))
            
            purchase_id = cursor.lastrowid
            total_amount = 0
            
            # Add 1-3 products to each purchase
            num_products = random.randint(1, 3)
            selected_products = random.sample(list(product_ids.items()), num_products)
            
            for product_name, product_id in selected_products:
                quantity = random.randint(5, 20)
                product_cursor = conn.cursor()
                product_cursor.execute('SELECT purchase_price FROM products WHERE id = %s', (product_id,))
                product_data = product_cursor.fetchone()
                unit_price = product_data['purchase_price']
                total_price = quantity * unit_price
                total_amount += total_price
                
                cursor.execute('''
                    INSERT INTO purchase_items
                    (purchase_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (purchase_id, product_id, quantity, unit_price, total_price))
                
                product_cursor.close()
            
            # Update purchase total
            cursor.execute('''
                UPDATE purchases
                SET total_amount = %s
                WHERE id = %s
            ''', (total_amount, purchase_id))
        
        # Insert sales
        print("Creating sales...")
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(1, 31):
            sale_date = start_date + timedelta(days=i)
            customer_id = random.choice(customer_ids) if random.random() > 0.3 else None
            invoice_number = f"INV-{sale_date.strftime('%Y%m%d')}-{i:03d}"
            
            # Create sale header
            cursor.execute('''
                INSERT INTO sales 
                (customer_id, invoice_number, sale_date, total_amount, notes, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (customer_id, invoice_number, sale_date.date(), 0, f"Sale {i}", 1))
            
            sale_id = cursor.lastrowid
            total_amount = 0
            
            # Add 1-4 products to each sale
            num_products = random.randint(1, 4)
            selected_products = random.sample(list(product_ids.items()), num_products)
            
            for product_name, product_id in selected_products:
                quantity = random.randint(1, 5)
                product_cursor = conn.cursor()
                product_cursor.execute('SELECT selling_price FROM products WHERE id = %s', (product_id,))
                product_data = product_cursor.fetchone()
                unit_price = product_data['selling_price']
                total_price = quantity * unit_price
                total_amount += total_price
                
                cursor.execute('''
                    INSERT INTO sale_items
                    (sale_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (sale_id, product_id, quantity, unit_price, total_price))
                
                product_cursor.close()
            
            # Update sale total
            cursor.execute('''
                UPDATE sales
                SET total_amount = %s
                WHERE id = %s
            ''', (total_amount, sale_id))
        
        conn.commit()
        print("Sample data created successfully.")
    
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_sample_data() 