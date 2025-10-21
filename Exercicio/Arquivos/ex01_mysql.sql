DROP DATABASE IF EXISTS comparador_precos;
CREATE DATABASE comparador_precos;
USE comparador_precos;
CREATE TABLE produtos (
id_produto INT PRIMARY KEY AUTO_INCREMENT,
nome_produto VARCHAR(255) NOT NULL,
valor_produto DECIMAL(10, 2) NOT NULL,
link_origem VARCHAR(500) NOT NULL,
site_origem VARCHAR(100) NOT NULL,
data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
INDEX idx_valor (valor_produto)
);
DELIMITER //
CREATE PROCEDURE sp_ranking_produtos(
IN p_ordenacao VARCHAR(10)
)
BEGIN
DECLARE v_total INT;
IF p_ordenacao NOT IN ('ASC', 'DESC') THEN
SELECT 'ERRO: Use ASC ou DESC como parâmetro' AS mensagem;
ELSE
SELECT COUNT(*) INTO v_total FROM produtos;
IF v_total = 0 THEN
SELECT 'Nenhum produto cadastrado' AS mensagem;
ELSE
IF p_ordenacao = 'ASC' THEN
SELECT
ROW_NUMBER() OVER (ORDER BY valor_produto ASC) AS ranking,
id_produto,
nome_produto,
valor_produto,
site_origem,
link_origem
FROM produtos
ORDER BY valor_produto ASC;
ELSE
SELECT
ROW_NUMBER() OVER (ORDER BY valor_produto DESC) AS ranking,
id_produto,
nome_produto,
valor_produto,
site_origem,
link_origem
FROM produtos
ORDER BY valor_produto DESC;
END IF;
END IF;
END IF;
END //
DELIMITER ;
INSERT INTO produtos (nome_produto, valor_produto, link_origem, site_origem) VALUES
('Notebook Gamer Acer Nitro 5', 4299.90, 'https://www.kabum.com.br/produto/123', 'Kabum'),
('Mouse Gamer Logitech G502', 299.99, 'https://www.amazon.com.br/produto/456', 'Amazon'),
('Teclado Mecânico HyperX', 549.00, 'https://www.mercadolivre.com.br/produto/789', 'Mercado Livre'),
('Monitor LG 24" Full HD', 899.90, 'https://www.kabum.com.br/produto/321', 'Kabum'),
('Headset Gamer HyperX Cloud', 399.99, 'https://www.amazon.com.br/produto/654', 'Amazon'),
('Webcam Logitech C920', 449.00, 'https://www.mercadolivre.com.br/produto/987', 'Mercado Livre');
CALL sp_ranking_produtos('ASC');
CALL sp_ranking_produtos('DESC');
SELECT * FROM produtos ORDER BY valor_produto;
SELECT
site_origem,
MIN(valor_produto) AS menor_preco,
MAX(valor_produto) AS maior_preco
FROM produtos
GROUP BY site_origem;