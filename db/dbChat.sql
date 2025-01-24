USE dbchat;conexiones

CREATE TABLE conexiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    ip VARCHAR(45) NOT NULL,
    puerto INT NOT NULL
);

CREATE TABLE desconexiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    ip VARCHAR(45) NOT NULL,
    puerto INT NOT NULL
);
