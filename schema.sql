DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usermail TEXT UNIQUE NOT NULL,
    userpassword PASSWORD NOT NULL
);