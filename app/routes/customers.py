from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

bp = Blueprint('customers', __name__, url_prefix='/customers')

@bp.route('/')
@login_required
def index():
    conn = mysql.connection
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # Get sorting parameters
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    
    # Validate sort_by to prevent SQL injection
    valid_columns = ['id', 'name', 'phone', 'email', 'address', 'created_at']
    if sort_by not in valid_columns:
        sort_by = 'id'
    
    # Validate sort_order
    if sort_order.lower() not in ['asc', 'desc']:
        sort_order = 'asc'
    
    # Build the query with ORDER BY
    query = f"SELECT * FROM customers WHERE business_id = %s ORDER BY {sort_by} {sort_order}"
    cursor.execute(query, (current_user.business_id,))
    customers = cursor.fetchall()
    cursor.close()
    
    return render_template('customers/index.html', 
                          customers=customers, 
                          sort_by=sort_by, 
                          sort_order=sort_order)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        
        conn = mysql.connection
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO customers (name, phone, email, address, business_id)
                VALUES (%s, %s, %s, %s, %s)
            ''', (name, phone, email, address, current_user.business_id))
            
            conn.commit()
            flash('Customer added successfully', 'success')
            
            # If the request came from the sales form, return the new customer ID
            if 'from_sales' in request.form:
                customer_id = cursor.lastrowid
                return redirect(url_for('sales.create', customer_id=customer_id))
            
            return redirect(url_for('customers.index'))
        except Exception as e:
            conn.rollback()
            flash(f'Error adding customer: {str(e)}', 'danger')
        finally:
            cursor.close()
    
    # Check if request is from sales form
    from_sales = request.args.get('from_sales', False)
    
    return render_template('customers/create.html', from_sales=from_sales)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    conn = mysql.connection
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # Get customer
    cursor.execute('SELECT * FROM customers WHERE id = %s AND business_id = %s', (id, current_user.business_id))
    customer = cursor.fetchone()
    
    if not customer:
        flash('Customer not found', 'danger')
        return redirect(url_for('customers.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        
        try:
            cursor.execute('''
                UPDATE customers
                SET name = %s, phone = %s, email = %s, address = %s
                WHERE id = %s AND business_id = %s
            ''', (name, phone, email, address, id, current_user.business_id))
            
            conn.commit()
            flash('Customer updated successfully', 'success')
            return redirect(url_for('customers.index'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating customer: {str(e)}', 'danger')
    
    cursor.close()
    return render_template('customers/edit.html', customer=customer)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    conn = mysql.connection
    cursor = conn.cursor()
    
    try:
        # Check if customer has sales
        cursor.execute('SELECT COUNT(*) as count FROM sales WHERE customer_id = %s AND business_id = %s', (id, current_user.business_id))
        result = cursor.fetchone()
        
        if result[0] > 0:
            flash('Cannot delete customer with existing sales records', 'danger')
            return redirect(url_for('customers.index'))
        
        # Delete customer
        cursor.execute('DELETE FROM customers WHERE id = %s AND business_id = %s', (id, current_user.business_id))
        
        conn.commit()
        flash('Customer deleted successfully', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting customer: {str(e)}', 'danger')
    finally:
        cursor.close()
    
    return redirect(url_for('customers.index'))

@bp.route('/history/<int:id>')
@login_required
def history(id):
    conn = mysql.connection
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # Get customer
    cursor.execute('SELECT * FROM customers WHERE id = %s AND business_id = %s', (id, current_user.business_id))
    customer = cursor.fetchone()
    
    if not customer:
        flash('Customer not found', 'danger')
        return redirect(url_for('customers.index'))
    
    # Get customer sales history
    cursor.execute('''
        SELECT s.*, COUNT(si.id) as item_count
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        WHERE s.customer_id = %s AND s.business_id = %s
        GROUP BY s.id
        ORDER BY s.sale_date DESC
    ''', (id, current_user.business_id))
    
    sales = cursor.fetchall()
    cursor.close()
    
    return render_template('customers/history.html', customer=customer, sales=sales) 