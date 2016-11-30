DROP TABLE if EXISTS Blubs;
DROP table if EXISTS Accounts;

CREATE TABLE Blubs(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Author Varchar(255),
  Content Varchar(255)
);

CREATE TABLE Accounts(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  UserName Varchar(255),
  Password Varchar(255)
);
