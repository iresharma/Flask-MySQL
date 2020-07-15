create table gameplayed(
    id int(2) PRIMARY KEY AUTO_INCREMENT,
    gid varchar(255),
    sid varchar(255),
    points int(2) NOT NULL
);

create table games(
    gid varchar(255) PRIMARY KEY,
    name varchar(255) NOT NULL,
    x_value int(2) NOT NULL,
    o_value int(2) NOT NULL,
    empty_value int(2) NOT NULL,
    col1 tinyint(1)  NOT NULL,
    col2 tinyint(1)  NOT NULL,
    col3 tinyint(1)  NOT NULL,
    row1 tinyint(1)  NOT NULL,
    row2 tinyint(1)  NOT NULL,
    row3 tinyint(1)  NOT NULL,
    dia1 tinyint(1)  NOT NULL,
    dia2 tinyint(1)  NOT NULL,
    type int(2) NOT NULL,
    played int(2) NOT NULL,
    win float(2,2) NOT NULL
);

create table students(
    sid varchar(255) PRIMARY KEY,
    name  varchar(255) NOT NULL,
    pas  varchar(255) NOT NULL,
    email  varchar(255) NOT NULL UNIQUE
);

create table logged(
    id int(2) PRIMARY KEY AUTO_INCREMENT,
    sid varchar(255) NOT NULL
);