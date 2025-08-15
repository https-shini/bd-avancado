
~~~~sql
-- =====================================================================
-- PARTE 1: CRIAÇÃO DAS TABELAS
-- Definição da estrutura do banco de dados com boas práticas.
-- =====================================================================

-- Tabela para armazenar os possíveis status de uma notícia (Ex: Publicada, Rascunho).
CREATE TABLE tb_status_noticia (
    id_status_noticia NUMBER,
    status            VARCHAR2(40),
    CONSTRAINT pk_status_noticia PRIMARY KEY (id_status_noticia)
);

-- Tabela para armazenar as categorias das notícias (Ex: Tecnologia, Política).
CREATE TABLE tb_categoria (
    id_categoria NUMBER,
    categoria    VARCHAR2(40),
    CONSTRAINT pk_categoria PRIMARY KEY (id_categoria)
);

-- Tabela para armazenar os dados dos jornalistas.
CREATE TABLE tb_jornalista (
    id_jornalista     NUMBER,
    nome              VARCHAR2(40),
    email             VARCHAR2(40),
    telefone          VARCHAR2(40),
    data_contratacao  DATE,
    CONSTRAINT pk_jornalista PRIMARY KEY (id_jornalista)
);

-- Tabela principal que armazena as informações de cada notícia.
-- Contém chaves estrangeiras que a relacionam com status e categoria.
CREATE TABLE tb_noticia (
    id_noticia        NUMBER,
    titulo            VARCHAR2(40),
    conteudo          VARCHAR2(40),
    data_criacao      DATE,
    id_status_noticia NUMBER,
    id_categoria      NUMBER,
    CONSTRAINT pk_noticia PRIMARY KEY (id_noticia),
    CONSTRAINT fk_noticia_status FOREIGN KEY (id_status_noticia) REFERENCES tb_status_noticia(id_status_noticia),
    CONSTRAINT fk_noticia_categoria FOREIGN KEY (id_categoria) REFERENCES tb_categoria(id_categoria)
);

-- Tabela associativa que resolve o relacionamento N:N (muitos-para-muitos)
-- entre notícias and jornalistas.
CREATE TABLE tb_noticia_jornalista (
    id_noticia_jornalista NUMBER,
    id_noticia            NUMBER,
    id_jornalista         NUMBER,
    CONSTRAINT pk_noticia_jornalista PRIMARY KEY (id_noticia_jornalista),
    CONSTRAINT fk_nj_noticia FOREIGN KEY (id_noticia) REFERENCES tb_noticia(id_noticia),
    CONSTRAINT fk_nj_jornalista FOREIGN KEY (id_jornalista) REFERENCES tb_jornalista(id_jornalista)
);


-- =====================================================================
-- PARTE 2: INSERÇÃO DE DADOS
-- Populado as tabelas com dados de exemplo para que as consultas
-- possam ser executadas e testadas.
-- =====================================================================

-- Inserindo 5 registros na tabela de status.
INSERT INTO tb_status_noticia (id_status_noticia, status) VALUES (1, 'Publicada');
INSERT INTO tb_status_noticia (id_status_noticia, status) VALUES (2, 'Arquivada');
INSERT INTO tb_status_noticia (id_status_noticia, status) VALUES (3, 'Rascunho');
INSERT INTO tb_status_noticia (id_status_noticia, status) VALUES (4, 'Pendente de Revisão');
INSERT INTO tb_status_noticia (id_status_noticia, status) VALUES (5, 'Excluída');

-- Inserindo 5 registros na tabela de categorias.
INSERT INTO tb_categoria (id_categoria, categoria) VALUES (1, 'Tecnologia');
INSERT INTO tb_categoria (id_categoria, categoria) VALUES (2, 'Política');
INSERT INTO tb_categoria (id_categoria, categoria) VALUES (3, 'Economia');
INSERT INTO tb_categoria (id_categoria, categoria) VALUES (4, 'eSports');
INSERT INTO tb_categoria (id_categoria, categoria) VALUES (5, 'Cultura');

-- Inserindo 5 registros na tabela de jornalistas.
-- A função TO_DATE é usada para converter um texto ('string') em um formato de data.
INSERT INTO tb_jornalista (id_jornalista, nome, email, telefone, data_contratacao) 
    VALUES (42499607, 'André Felipe Jorge Rachid', 'andre.rachid@gmail.com', '11991234567', TO_DATE('2025-01-10', 'yyyy-mm-dd'));
INSERT INTO tb_jornalista (id_jornalista, nome, email, telefone, data_contratacao) 
    VALUES (34637109, 'Flávio Caramit Gomes', 'flavio.gomes@gmail.com', '11992345678', TO_DATE('2025-05-03', 'yyyy-mm-dd'));
INSERT INTO tb_jornalista (id_jornalista, nome, email, telefone, data_contratacao) 
    VALUES (34032207, 'Guilherme de Souza Cruz', 'guilherme.cruz@gmail.com', '11993456789', TO_DATE('2025-02-02', 'yyyy-mm-dd'));
INSERT INTO tb_jornalista (id_jornalista, nome, email, telefone, data_contratacao) 
    VALUES (35566515, 'Vinicius Ansbach Costa', 'vinicius.costa@gmail.com', '11994567890', TO_DATE('2025-03-15', 'yyyy-mm-dd'));
INSERT INTO tb_jornalista (id_jornalista, nome, email, telefone, data_contratacao) 
    VALUES (35700033, 'Vitor Stratikopoulos França', 'vitor.franca@gmail.com', '11995678901', TO_DATE('2025-04-20', 'yyyy-mm-dd'));

-- Inserindo 5 registros na tabela de notícias.
INSERT INTO tb_noticia (id_noticia, titulo, conteudo, data_criacao, id_status_noticia, id_categoria) 
    VALUES (1, 'Novo Processador Anunciado', 'Lançamento da CPU.', TO_DATE('2025-08-14', 'yyyy-mm-dd'), 1, 1);
INSERT INTO tb_noticia (id_noticia, titulo, conteudo, data_criacao, id_status_noticia, id_categoria) 
    VALUES (2, 'Acordo Comercial é Firmado', 'Acordo foi assinado.', TO_DATE('2025-07-20', 'yyyy-mm-dd'), 1, 2);
INSERT INTO tb_noticia (id_noticia, titulo, conteudo, data_criacao, id_status_noticia, id_categoria) 
    VALUES (3, 'Banco Central Sobe Juros', 'Taxa Selic sobe 0.25%.', TO_DATE('2025-06-11', 'yyyy-mm-dd'), 2, 3);
INSERT INTO tb_noticia (id_noticia, titulo, conteudo, data_criacao, id_status_noticia, id_categoria) 
    VALUES (4, 'FURIA Vence e Avança no Major', 'Equipe brasileira de CS2 avança.', TO_DATE('2025-05-30', 'yyyy-mm-dd'), 4, 4);
INSERT INTO tb_noticia (id_noticia, titulo, conteudo, data_criacao, id_status_noticia, id_categoria) 
    VALUES (5, 'Exposição de Arte Moderna', 'Museu inaugura expo.', TO_DATE('2025-08-10', 'yyyy-mm-dd'), 3, 5);

-- Inserindo as ligações entre notícias e jornalistas, definindo a autoria.
INSERT INTO tb_noticia_jornalista (id_noticia_jornalista, id_noticia, id_jornalista) 
    VALUES (1, 1, 42499607); -- Notícia de Tecnologia escrita por André
INSERT INTO tb_noticia_jornalista (id_noticia_jornalista, id_noticia, id_jornalista) 
    VALUES (2, 2, 34637109); -- Notícia de Política escrita por Flávio
INSERT INTO tb_noticia_jornalista (id_noticia_jornalista, id_noticia, id_jornalista) 
    VALUES (3, 3, 35566515); -- Notícia de Economia escrita por Vinicius
INSERT INTO tb_noticia_jornalista (id_noticia_jornalista, id_noticia, id_jornalista) 
    VALUES (4, 4, 34032207); -- Notícia de eSports escrita por Guilherme
INSERT INTO tb_noticia_jornalista (id_noticia_jornalista, id_noticia, id_jornalista) 
    VALUES (5, 5, 35700033); -- Notícia de Cultura escrita por Vitor


-- =====================================================================
-- PARTE 3: CONSULTAS (LEITURA DOS DADOS)
-- Respostas para os 15 exercícios
-- =====================================================================

-- Exercício 1: Listar todas as notícias.
SELECT * FROM tb_noticia;

-- Exercício 2: Listar todas as notícias exibindo a data no formato dd/mm/yyyy.
SELECT id_noticia, titulo, TO_CHAR(data_criacao, 'dd/mm/yyyy') AS data_formatada FROM tb_noticia;

-- Exercício 3: Listar todas as notícias cujo mês seja agosto. Exibir da mais atual para a mais antiga.
SELECT * FROM tb_noticia WHERE TO_CHAR(data_criacao, 'MM') = '08' ORDER BY data_criacao DESC;

-- Exercício 4: Listar a quantidade de notícias existentes.
SELECT COUNT(*) AS quantidade_total FROM tb_noticia;

-- Exercício 5: Listar as categorias existentes.
SELECT * FROM tb_categoria;

-- Exercício 6: Listar todas as notícias da mais atual para a mais antiga.
SELECT * FROM tb_noticia ORDER BY data_criacao DESC;

-- Exercício 7: Listar apenas as duas últimas notícias criadas.
SELECT * FROM tb_noticia ORDER BY data_criacao DESC FETCH FIRST 2 ROWS ONLY;

-- Exercício 8: Listar apenas a primeira notícia criada.
SELECT * FROM tb_noticia ORDER BY data_criacao ASC FETCH FIRST 1 ROW ONLY;

-- Exercício 9: Liste a quantidade de notícias existentes por categoria.
SELECT id_categoria, COUNT(id_noticia) AS quantidade FROM tb_noticia GROUP BY id_categoria;

-- Exercício 10: Liste a quantidade de notícias existentes por categoria (versão simples).
SELECT id_categoria, COUNT(id_noticia) AS quantidade FROM tb_noticia GROUP BY id_categoria;

-- Exercício 11: Listar o título, ID da categoria e data de criação das notícias.
SELECT titulo, id_categoria, data_criacao FROM tb_noticia;

-- Exercício 12: Exibir todas as categorias cadastradas.
SELECT * FROM tb_categoria;

-- Exercício 13: Listar as notícias onde o título inicia com a letra 'A'.
SELECT * FROM tb_noticia WHERE titulo LIKE 'A%';

-- Exercício 14: Listar as notícias onde o título não inicia com a letra 'A'.
SELECT * FROM tb_noticia WHERE titulo NOT LIKE 'A%';

-- Exercício 15: Listar notícias das categorias com ID 2 (Política) ou 4 (eSports).
SELECT * FROM tb_notcia WHERE id_categoria IN (2, 4);


-- =====================================================================
-- QUERY BONUS
-- Comando para Listar Todos os Dados do Banco
-- =====================================================================
SELECT * FROM tb_categoria; 		 -- Mostrando todos os dados da tabela de CATEGORIAS
SELECT * FROM tb_status_noticia; 	 -- Mostrando todos os dados da tabela de STATUS
SELECT * FROM tb_jornalista;		 -- Mostrando todos os dados da tabela de JORNALISTAS
SELECT * FROM tb_noticia;			 -- Mostrando todos os dados da tabela de NOTÍCIAS
SELECT * FROM tb_noticia_jornalista; -- Mostrando as ligações entre NOTÍCIAS e JORNALISTAS


-- =====================================================================
-- PARTE 4: EXCLUSÃO DAS TABELAS
-- Comandos para remover as tabelas e limpar o ambiente do banco de dados
-- após a conclusão dos exercícios.
-- =====================================================================

-- É necessário remover as tabelas na ordem inversa de sua dependência
-- para evitar erros de chave estrangeira.
DROP TABLE tb_noticia_jornalista;
DROP TABLE tb_noticia;
DROP TABLE tb_jornalista;
DROP TABLE tb_status_noticia;
DROP TABLE tb_categoria;
~~~~







