import mysql.connector
import random
import datetime




def db_connection():
    return mysql.connector.connect(
        host ="localhost",
        user ="root",
        password ="",
        database ="sql_project"
    )

def create_db():
    conn =db_connection()
    mycommand =conn.cursor()
    query ="create database sql_project"
    mycommand.execute(query)
    conn.close()
    return "database created successfully"

def create_parent_table():
    conn =db_connection()
    mycommand =conn.cursor()
    query ="create table products (p_id int primary key auto_increment ,p_name varchar(255) not null ,p_description varchar(255) ,p_category varchar(255) not null ,p_price decimal(10) not null ,p_img varchar(255))"
    mycommand.execute(query)
    conn.close()
    return " the parent table created succesfully "

def create_parent_table_2():
    conn =db_connection()
    mycommand =conn.cursor()
    query ="create table customers (c_id int primary key auto_increment ,c_name varchar(255) not null ,c_email varchar(255) not null ,c_address varchar(255) not null ,c_phone varchar(255) not null)"
    mycommand.execute(query)
    conn.close()
    return " the second parent table created successfully"

def create_child_table():
    conn =db_connection()
    mycommand =conn.cursor()
    query ="create table orders ( o_id int primary key auto_increment , c_id int, o_date Date DEFAULT NOW() ,o_status varchar(255) default 'order placed',o_total decimal(10)  ,FOREIGN KEY (c_id) REFERENCES customers(c_id) )"
    mycommand.execute(query)
    conn.close()
    return " the child table is created successfully"

# def insert_data_in_create_parent_table2():
#     conn =db_connection()
#     mycommand =conn.cursor()
#     query ="INSERT INTO `customers` (`c_name`, `c_email`, `c_address`, `c_phone`) VALUES ('John Doe', 'johndoe@example.com', '123 Main Street', '1234567890')"
#     mycommand.execute(query)
#     conn.commit()
#     conn.close()
#     return " the data inserted in  parent table_2 is succesfull "
    

# def insert_data_in_create_parent_table():
#     conn =db_connection()
#     mycommand =conn.cursor()
#     query ="INSERT INTO `products`( `p_name`, `p_description`, `p_category`, `p_price`, `p_img`) VALUES ( 'Laptop', 'A powerful laptop for work and play', 'Electronics', '999.99', 'laptop.jpg')"
#     mycommand.execute(query)
#     conn.commit()
#     conn.close()
#     return " the data inserted in  parent table  is succesfull"   



# def insert_data_in_child_table():
#     conn =db_connection()
#     mycommand =conn.cursor()
#     query ="INSERT INTO `orders`(  `o_date`, `o_status`, `o_total`) VALUES (  '2024-08-25', 'pending', '99.99')"
#     mycommand.execute(query)
#     conn.commit()
#     conn.close()
#     return "the data is inserted in child table "




def insert_data_into_table(table_name, columns, data):
    """Inserts data into a specified table using parameterized queries."""
    conn = db_connection()  # Replace with your database connection function
    mycommand = conn.cursor()

    placeholders = ', '.join(['%s'] * len(columns))
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    for row in data:
        mycommand.execute(query, row)

    conn.commit()
    mycommand.close()
    conn.close()
    return " the insertion of data is completed"

# Generate sample data
customer_data = [
    ('Customer %d' % i, f"customer{i}@example.com", f"Address {i}", f"1234567890{i}")
    for i in range(1, 21)
]

product_data = [
    (f"Product {i}", f"Description {i}", f"Category {i}", random.randint(10, 1000), f"product{i}.jpg")
    for i in range(1, 21)
]

order_data = [
    (random.randint(1, 20), datetime.date.today() + datetime.timedelta(days=i), 'pending', random.randint(50, 500))
    for i in range(1, 21)
]

# Insert data
print(insert_data_into_table('customers', ['c_name', 'c_email', 'c_address', 'c_phone'], customer_data))
print(insert_data_into_table('products', ['p_name', 'p_description', 'p_category', 'p_price', 'p_img'], product_data))

print(insert_data_into_table('orders', ['c_id', 'o_date', 'o_status', 'o_total'], order_data))

    
    
# print(insert_data_in_child_table())
# print(insert_data_in_create_parent_table())
# print(insert_data_in_create_parent_table2())

# print(create_child_table())
# print(create_parent_table_2())
# print(create_db())
# print(create_parent_table())
