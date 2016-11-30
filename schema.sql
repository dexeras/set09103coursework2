DROP TABLE if EXISTS Blubs;
DROP table if exists Blubbers;

CREATE TABLE Blubs(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Author Varchar(255),
  Content Varchar(255),
  Time Varchar(255)
);

CREATE TABLE Blubbers(
  UserName Varchar(255) PRIMARY KEY,
  Password Varchar(255)
);
