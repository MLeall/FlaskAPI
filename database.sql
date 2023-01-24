CREATE TABLE users(
  id    INTEGER PRIMARY KEY AUTOINCREMENT, 
  name  TEXT,
  email  TEXT,
  key TEXT
);

CREATE TABLE stores(
  id     INTEGER PRIMARY KEY AUTOINCREMENT, 
  name   TEXT, 
  userId INTEGER,
  FOREIGN KEY(userId) REFERENCES users(id)
);

CREATE TABLE products(
  id     INTEGER PRIMARY KEY AUTOINCREMENT, 
  name   TEXT,
  price  NUMERIC,
  storeId INTEGER,
  FOREIGN KEY(storeId) REFERENCES stores(id)
);
