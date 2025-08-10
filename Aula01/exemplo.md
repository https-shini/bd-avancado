<h1 align="center">🚀 Guia de Execução de Script SQL (Oracle)</h1>

<p align="center">
  <a href="https://github.com/https-shini/bd-avancado" >Home</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/https-shini/bd-avancado/edit/main/Aula01/Aula01.md">Aula01</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-como-executar">Como Executar</a>
    &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-detalhes-do-script">Detalhes do Script</a>
    &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-referências">Referências</a>
</p>

<br>

Este repositório disponibiliza um script SQL completo para **criar** e **popular** um banco de dados simples com tabelas de **usuários** e **pedidos**.  

O script foi desenvolvido como um exercício prático para a minha primeira aula de **Banco de Dados Avançado**, com o objetivo de testar de forma independente como criar e popular uma tabela simples, além de trabalhar os conceitos básicos de relacionamento entre tabelas.

Ele é ideal para execução em ambiente Oracle SQL, como o **Oracle Live SQL**, facilitando a criação do banco a partir do zero.

---

## ⚙️ Como Executar
Para configurar o banco de dados, copie o código abaixo, acompanhe o passo a passo para entendê-lo, cole-o em uma única aba ('SQL Worksheet') do seu ambiente Oracle e execute-o.

1. Abra seu ambiente Oracle SQL (ex: Oracle Live SQL).  
2. Crie uma nova aba de SQL ("SQL Worksheet").  
3. Copie e cole o script.  
4. Execute-o para criar as tabelas, inserir dados e preparar o banco.

---

## 📜 Detalhes do Script
### Passo 1: 🏗️ Criação das Tabelas
Primeiro, as tabelas são criadas na ordem de dependência.  
A tabela `usuario` é criada primeiro, pois a tabela `pedido` possui uma chave estrangeira (`FOREIGN KEY`) que faz referência a ela.

```sql
-- Cria a tabela para armazenar os usuários
CREATE TABLE usuario (
    idusuario   NUMBER PRIMARY KEY,
    nome        VARCHAR2(100) NOT NULL,
    email       VARCHAR2(100) UNIQUE
);

-- Cria a tabela para armazenar os pedidos (sem a data ainda)
CREATE TABLE pedido (
    idpedido      NUMBER PRIMARY KEY,
    idusuario     NUMBER,
    CONSTRAINT fk_pedido_usuario FOREIGN KEY (idusuario) REFERENCES usuario(idusuario)
);

-- Adiciona a coluna de data à tabela de pedidos já criada
ALTER TABLE pedido ADD data_pedido DATE;
```

### Passo 2: 👤 Inserção de Usuários
Com as tabelas criadas, inserimos os registros dos usuários.

```sql
INSERT INTO usuario (idusuario, nome, email) VALUES (42499607, 'André Felipe Jorge Rachid', 'andre@gmail.com');
INSERT INTO usuario (idusuario, nome, email) VALUES (34637109, 'Flávio Caramit Gomes', 'flavio@gmail.com');
INSERT INTO usuario (idusuario, nome, email) VALUES (34032207, 'Guilherme de Souza Cruz', 'guilherme@gmail.com');
INSERT INTO usuario (idusuario, nome, email) VALUES (35566515, 'Vinicius Ansbach Costa', 'vinicius@gmail.com');
INSERT INTO usuario (idusuario, nome, email) VALUES (35700033, 'Vitor Stratikopoulos França', 'vitor@gmail.com');
```

### Passo 3: 🛒 Inserção de Pedidos
Agora, inserimos os pedidos, associando cada um a um usuário existente através do idusuario.

```sql
INSERT INTO pedido (idpedido, idusuario, data_pedido) VALUES (201, 42499607, TO_DATE('2025-08-10', 'YYYY-MM-DD'));
INSERT INTO pedido (idpedido, idusuario, data_pedido) VALUES (202, 34637109, TO_DATE('2025-08-10', 'YYYY-MM-DD'));
INSERT INTO pedido (idpedido, idusuario, data_pedido) VALUES (203, 34032207, TO_DATE('2025-08-09', 'YYYY-MM-DD'));
INSERT INTO pedido (idpedido, idusuario, data_pedido) VALUES (204, 35566515, TO_DATE('2025-08-10', 'YYYY-MM-DD'));
INSERT INTO pedido (idpedido, idusuario, data_pedido) VALUES (205, 35700033, TO_DATE('2025-08-08', 'YYYY-MM-DD'));
INSERT INTO pedido (idpedido, idusuario, data_pedido) VALUES (206, 42499607, TO_DATE('2025-08-10', 'YYYY-MM-DD'));
```

### Passo 4: 💾 Confirmação das Transações (Commit)
O comando COMMIT salva permanentemente todas as alterações (criações e inserções) feitas no banco de dados.

```sql
COMMIT;
```

### Passo 5: 📊 Consulta dos Dados Combinados
Finalmente, executamos uma consulta JOIN para visualizar os dados de forma consolidada, mostrando os detalhes de cada pedido junto com as informações do usuário que o realizou.

```sql
SELECT
    p.idpedido,
    p.data_pedido,
    u.nome,
    u.email,
    u.idusuario
FROM
    pedido p
JOIN
    usuario u ON p.idusuario = u.idusuario
ORDER BY
    p.idpedido;
```

---

## 📚 Referências
* [Oracle Live SQL](https://livesql.oracle.com)
* [Documentação Oracle SQL](https://docs.oracle.com/en/database/oracle/oracle-database/index.html)


