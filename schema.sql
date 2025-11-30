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
