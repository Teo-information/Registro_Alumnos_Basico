CREATE DATABASE gestor_notas;
USE gestor_notas;

CREATE TABLE notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante VARCHAR(100),
    nota INT
);
