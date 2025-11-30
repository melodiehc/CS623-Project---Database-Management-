# CS623-Project---Database-Management-

# CS623 Transactional Database Project  
**Author:** Melodie Cornelly  
**Course:** CS623 – Database Management  
**Semester:** Fall 2025  
**Professor:** Pratik Chaudhari 

---

## 📌 Project Overview
This project implements a **transactional database application** using **PostgreSQL** and **Python (psycopg2)**.  
It demonstrates how ACID properties (Atomicity, Consistency, Isolation, Durability) are enforced through a series of update transactions involving three database tables:

- **Product(prod, pname, price)**
- **Depot(dep, addr, volume)**
- **Stock(prod, dep, quantity)**

Foreign key constraints with **ON DELETE CASCADE** and **ON UPDATE CASCADE** ensure reactive behavior when primary keys are modified or removed.

The Python program provides a **menu-driven interface** where each option executes one of the required transactions inside a controlled SQL transaction block.

---

## 📊 Database Schema

```sql
CREATE TABLE Product (
    prod   VARCHAR(10) PRIMARY KEY,
    pname  VARCHAR(50),
    price  NUMERIC(10,2)
);

CREATE TABLE Depot (
    dep     VARCHAR(10) PRIMARY KEY,
    addr    VARCHAR(50),
    volume  INTEGER
);

CREATE TABLE Stock (
    prod     VARCHAR(10),
    dep      VARCHAR(10),
    quantity INTEGER,
    PRIMARY KEY (prod, dep),
    FOREIGN KEY (prod) REFERENCES Product(prod)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (dep) REFERENCES Depot(dep)
        ON DELETE CASCADE ON UPDATE CASCADE
);
