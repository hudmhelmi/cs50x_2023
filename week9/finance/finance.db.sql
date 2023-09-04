CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  username TEXT NOT NULL,
  hash TEXT NOT NULL,
  cash NUMERIC NOT NULL DEFAULT 10000.00
);

CREATE TABLE sqlite_sequence(name, seq);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER,
    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Buy', 'Sell')),
    symbol TEXT NOT NULL,
    price INTEGER NOT NULL,
    shares INTEGER NOT NULL,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);