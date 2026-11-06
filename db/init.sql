CREATE TABLE counter (
    id INT PRIMARY KEY,
    hits INT
);

INSERT INTO counter (id, hits) VALUES (1, 0);

CREATE TABLE access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    access_time DATETIME,
    client_ip VARCHAR(45),
    internal_ip VARCHAR(45)
);