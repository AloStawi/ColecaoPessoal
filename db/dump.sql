CREATE DATABASE colecao_livros;

USE colecao_livros;

CREATE TABLE livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano INT,
    genero VARCHAR(100),
    status_leitura ENUM('não lido', 'lendo', 'concluído') DEFAULT 'não lido',
    nota INT,
    data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);