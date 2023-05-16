import streamlit as st
import sqlite3

st.title("Shopping Website CMS")

# Create a connection to the database
conn = sqlite3.connect('shopping.db')
c = conn.cursor()

# Create a table to store products if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT)''')
conn.commit()

# Sidebar menu
st.sidebar.title("Shopping Website CMS")
menu_options = ["Add Product", "View Products"]
selected_option = st.sidebar.selectbox("Menu", menu_options)

# Add Product
if selected_option == "Add Product":
    st.header("Add Product")
    name = st.text_input("Product Name")
    price = st.number_input("Product Price")
    description = st.text_area("Product Description")

    if st.button("Add"):
        c.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", (name, price, description))
        conn.commit()
        st.success("Product added successfully!")

# View Products
if selected_option == "View Products":
    st.header("View Products")

    c.execute("SELECT * FROM products")
    product_rows = c.fetchall()

    if len(product_rows) == 0:
        st.info("No products available.")
    else:
        for i, product in enumerate(product_rows, start=1):
            st.subheader(f"Product {i}")
            st.write(f"Name: {product[1]}")
            st.write(f"Price: {product[2]}")
            st.write(f"Description: {product[3]}")
            st.write("---")

# Close the database connection
conn.close()

# Run the app
if __name__ == '__main__':
    st.write()
