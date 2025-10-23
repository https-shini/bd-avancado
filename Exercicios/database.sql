DROP DATABASE IF EXISTS comparador_produtos;
CREATE DATABASE IF NOT EXISTS comparador_produtos;
USE comparador_produtos;

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    preco DECIMAL(10,2),
    link TEXT,
    loja VARCHAR(100)
);


DELIMITER $$

CREATE PROCEDURE ranking_produtos(IN ordem VARCHAR(4))
BEGIN
    IF UPPER(ordem) = 'ASC' THEN
        SELECT nome, loja, preco, link
        FROM produtos
        ORDER BY preco ASC;
    ELSEIF UPPER(ordem) = 'DESC' THEN
        SELECT nome, loja, preco, link
        FROM produtos
        ORDER BY preco DESC;
    ELSE
        SELECT 'Parâmetro inválido. Use "ASC" ou "DESC".' AS mensagem;
    END IF;
END$$

DELIMITER ;

CALL ranking_produtos('ASC');
CALL ranking_produtos('DESC');
