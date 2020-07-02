CREATE TABLE games(gid int(2) AUTO_INCREMENT PRIMARY KEY NOT NULL, name varchar(15) NOT NULL, x_value int(3) NOT NULL, o_value int(3) NOT NULL, empty_value int(3) NOT NULL, qType1 bool NOT NULL, qType2 bool NOT NULL, qType3 bool NOT NULL, qType4 bool NOT NULL, qType5 bool NOT NULL, qType6 bool NOT NULL, qType7 bool NOT NULL, qType8 bool NOT NULL, qType9 bool NOT NULL, type int(1) NOT NULL, win int(3) );


INSERT INTO games(name, x_value, o_value, empty_value, qType1, qType2, qType3, qType4, qType5, qType6, qType7, qType8, qType9, type) VALUES("Game1", 12, 23, 45, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0);


CREATE TABLE students(sid int(2) NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(20) NOT NULL, pass varchar(15) NOT NULL, win int(3) NOT NULL);


INSERT INTO students(name, pass, win) VALUES("iresh", "iresharma", 100);


create table gamesPlayed(gid int(2) NOT NULL, sid int(2) NOT NULL, result bool);