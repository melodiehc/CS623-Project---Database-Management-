import psycopg2

# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Summertime678",  
    "host": "localhost",
    "port": 5432,
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# -------------------------------------------------
# TRANSACTION WRAPPER (ACID)
# -------------------------------------------------
def run_transaction(fn, *args):
    conn = None
    try:
        conn = get_connection()
        conn.autocommit = False
        cur = conn.cursor()

        fn(cur, *args)

        conn.commit()
        print("Transaction committed.\n")
    except Exception as e:
        if conn:
            conn.rollback()
        print("Transaction rolled back due to error:", e)
    finally:
        if conn:
            conn.close()


# -------------------------------------------------
# 1. Delete product p1 from Product (cascade delete from Stock)
# -------------------------------------------------
def tx_delete_product(cur, prod):
    print(f"Deleting product {prod} ...")
    cur.execute("DELETE FROM Product WHERE prod = %s;", (prod,))


# -------------------------------------------------
# 2. Delete depot d1 from Depot (cascade delete from Stock)
# -------------------------------------------------
def tx_delete_depot(cur, dep):
    print(f"Deleting depot {dep} ...")
    cur.execute("DELETE FROM Depot WHERE dep = %s;", (dep,))


# -------------------------------------------------
# 3. Rename product p1 → pp1
# -------------------------------------------------
def tx_rename_product(cur, old_prod, new_prod):
    print(f"Renaming product {old_prod} to {new_prod} ...")
    cur.execute(
        "UPDATE Product SET prod = %s WHERE prod = %s;",
        (new_prod, old_prod),
    )


# -------------------------------------------------
# 4. Rename depot d1 → dd1
# -------------------------------------------------
def tx_rename_depot(cur, old_dep, new_dep):
    print(f"Renaming depot {old_dep} to {new_dep} ...")
    cur.execute(
        "UPDATE Depot SET dep = %s WHERE dep = %s;",
        (new_dep, old_dep),
    )


# -------------------------------------------------
# 5. Add product (p100, cd, 5) and stock (p100, d2, 50)
# -------------------------------------------------
def tx_add_product_and_stock(cur):
    print("Adding product p100 and stock record ...")
    cur.execute(
        "INSERT INTO Product (prod, pname, price) VALUES (%s, %s, %s);",
        ("p100", "cd", 5),
    )
    cur.execute(
        "INSERT INTO Stock (prod, dep, quantity) VALUES (%s, %s, %s);",
        ("p100", "d2", 50),
    )


# -------------------------------------------------
# 6. Add depot (d100, Chicago, 100) and stock (p1, d100, 100)
# -------------------------------------------------
def tx_add_depot_and_stock(cur):
    print("Adding depot d100 and stock record ...")
    cur.execute(
        "INSERT INTO Depot (dep, addr, volume) VALUES (%s, %s, %s);",
        ("d100", "Chicago", 100),
    )
    cur.execute(
        "INSERT INTO Stock (prod, dep, quantity) VALUES (%s, %s, %s);",
        ("p1", "d100", 100),
    )


# -------------------------------------------------
# PRINT TABLES (for demo)
# -------------------------------------------------
def print_tables():
    conn = get_connection()
    cur = conn.cursor()
    for table in ["Product", "Depot", "Stock"]:
        print(f"\n--- {table} ---")
        cur.execute(f"SELECT * FROM {table} ORDER BY 1;")
        for row in cur.fetchall():
            print(row)
    conn.close()
    print("\n")


# -------------------------------------------------
# MENU (DEMO INTERFACE)
# -------------------------------------------------
def main():
    while True:
        print("\n=== CS623 Project Menu ===")
        print("1. Delete product p1")
        print("2. Delete depot d1")
        print("3. Rename product p1 → pp1")
        print("4. Rename depot d1 → dd1")
        print("5. Add product (p100, cd, 5) + stock (p100, d2, 50)")
        print("6. Add depot (d100, Chicago, 100) + stock (p1, d100, 100)")
        print("7. Show tables")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            run_transaction(tx_delete_product, "p1")
        elif choice == "2":
            run_transaction(tx_delete_depot, "d1")
        elif choice == "3":
            run_transaction(tx_rename_product, "p1", "pp1")
        elif choice == "4":
            run_transaction(tx_rename_depot, "d1", "dd1")
        elif choice == "5":
            run_transaction(tx_add_product_and_stock)
        elif choice == "6":
            run_transaction(tx_add_depot_and_stock)
        elif choice == "7":
            print_tables()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
