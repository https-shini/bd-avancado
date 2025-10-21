# 📚 Laboratório de Banco de Dados Avançado

## 📋 Informações da Atividade

**Disciplina:** Laboratório de Banco de Dados Avançado  
**Professor:** Me. Allan Vidal  
**Curso:** Ciência da Computação – Universidade Cruzeiro do Sul  
**Pontuação Total:** Até 2.0 pontos  
**Formato:** Atividade em grupo (máximo 3 integrantes)

---

## 📝 Exercícios Propostos

### 🔹 [Exercício 1: Comparador de Preços - Web Scraping](./EXERCICIO_01.md)

**Pontuação:** 1.0 ponto

#### 📌 Enunciado

Você foi contratado para desenvolver uma aplicação em Python que auxilie os usuários na comparação de preços de produtos em diferentes aplicações web.

#### 🎯 Requisitos Obrigatórios

| # | Requisito | Peso |
|---|-----------|------|
| a | Coletar dados de **pelo menos 3 sites diferentes** utilizando web scraping (com BeautifulSoup) | 30% |
| b | Armazenar em banco de dados **MySQL** com: id do produto, nome, valor e link de origem | 30% |
| c | Criar e executar uma **procedure** que exiba ranking ordenado (ASC/DESC por parâmetro) | 40% |

#### ✅ Critérios de Avaliação

- **Web Scraping funcional** com BeautifulSoup em 3+ sites
- **Persistência correta** dos dados no MySQL
- **Stored Procedure parametrizada** para ranking
- **Código limpo e documentado**
- **Execução sem erros**

#### 🛠️ Tecnologias

- Python 3.x
- MySQL 8.0+
- Bibliotecas: `beautifulsoup4`, `requests`, `mysql-connector-python`

#### 📊 Resumo da Solução

A solução implementa:
1. ✅ **3 funções de scraping** (Amazon, Mercado Livre, Shopee) usando BeautifulSoup
2. ✅ **Classe `GerenciadorBanco`** para operações MySQL
3. ✅ **Stored Procedure `sp_ranking_produtos`** com parâmetro ASC/DESC
4. ✅ **Estrutura de tabelas** com índices otimizados

**[📖 Ver documentação completa →](./EXERCICIO_01.md)**

<details>
<summary><b>Ver código completo.</b></summary>

## 🔗 Código Completo

### 📄 `database.sql`

```sql
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
        SELECT 'ERRO: Use ASC ou DESC' AS mensagem;
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
```

### 📄 `main.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercício 1: Comparador de Preços com Web Scraping
Requisitos: BeautifulSoup, 3+ sites, MySQL, Procedure
"""

import requests
from bs4 import BeautifulSoup
import mysql.connector
import time

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sua_senha_aqui',
    'database': 'comparador_precos'
}

class GerenciadorBanco:
    def __init__(self, config):
        self.conexao = None
        self.cursor = None
        try:
            self.conexao = mysql.connector.connect(**config)
            self.cursor = self.conexao.cursor()
            print("✓ Conectado ao MySQL")
        except mysql.connector.Error as err:
            print(f"✗ Erro: {err}")
            exit(1)
    
    def inserir_produto(self, nome, valor, link, site):
        try:
            sql = """
            INSERT INTO produtos (nome_produto, valor_produto, link_origem, site_origem)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(sql, (nome, valor, link, site))
            self.conexao.commit()
            return True
        except mysql.connector.Error as err:
            print(f"✗ Erro: {err}")
            return False
    
    def limpar_tabela(self):
        try:
            self.cursor.execute("TRUNCATE TABLE produtos")
            self.conexao.commit()
            print("✓ Tabela limpa")
        except mysql.connector.Error as err:
            print(f"✗ Erro: {err}")
    
    def exibir_ranking(self, ordenacao='ASC'):
        try:
            self.cursor.callproc('sp_ranking_produtos', [ordenacao])
            for result in self.cursor.stored_results():
                return result.fetchall()
        except mysql.connector.Error as err:
            print(f"✗ Erro: {err}")
```



</details>

---

### 🔹 [Exercício 2: Jogo Jokenpô em PL/SQL](./EXERCICIO_02.md)

**Pontuação:** 0.5 ponto

#### 📌 Enunciado

Utilizando PL/SQL, crie um script que simule o jogo Jokenpô (Pedra, Papel e Tesoura).

#### 🎯 Requisitos Obrigatórios

| # | Requisito | Peso |
|---|-----------|------|
| a | Usuário informa jogada; **Oracle gera jogada do PC aleatoriamente** | 30% |
| b | Comparar jogadas e **definir resultado** (empate, vitória usuário ou PC) | 30% |
| c | **Salvar cada jogada** em tabela e criar consulta com estatísticas completas | 40% |

#### ✅ Critérios de Avaliação

- **Geração aleatória** correta usando `DBMS_RANDOM`
- **Lógica de comparação** implementada corretamente
- **Persistência** de todas as jogadas
- **Views/Consultas** para estatísticas (vitórias usuário, PC, empates)
- **PL/SQL bem estruturado** com tratamento adequado

#### 🛠️ Tecnologias

- Oracle Database (Oracle SQL Live)
- PL/SQL
- Package `DBMS_RANDOM` e `DBMS_OUTPUT`

#### 📊 Resumo da Solução

A solução implementa:
1. ✅ **Tabela `tbJokenpo`** com histórico completo de jogadas
2. ✅ **Procedure `jogarJokenpo`** com geração aleatória e lógica de comparação
3. ✅ **View `vwEstatisticasJokenpo`** para totais agregados
4. ✅ **View `vwHistoricoJokenpo`** para consulta de partidas

**[📖 Ver documentação completa →](./EXERCICIO_02.md)**

<details>
<summary><b>Ver código completo.</b></summary>

## 🔗 Código Completo

### 📄 `Exercício 2: Jogo Jokenpô em PL/SQL`

```sql

-- ============================================================
-- EXERCÍCIO 02: JOGO JOKENPÔ EM PL/SQL
-- Banco de Dados: Oracle
-- Pontuação: 0.5 ponto
-- ============================================================

-- ============================================================
-- 1. CRIAR TABELA PARA ARMAZENAR JOGADAS
-- Requisito: Salvar cada jogada realizada
-- ============================================================
CREATE TABLE tbJokenpo (
    idJogada NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    jogadaUsuario VARCHAR2(10) NOT NULL,
    jogadaPC VARCHAR2(10) NOT NULL,
    resultado VARCHAR2(20) NOT NULL,
    dataJogada DATE DEFAULT SYSDATE
);

-- ============================================================
-- 2. PROCEDURE: JOGAR JOKENPÔ
-- Requisito a: Usuário informa jogada, Oracle gera do PC
-- Requisito b: Comparar e definir resultado
-- Requisito c: Salvar na tabela
-- ============================================================
CREATE OR REPLACE PROCEDURE jogarJokenpo (
    p_jogadaUsuario IN VARCHAR2
) AS
    v_jogadaPC VARCHAR2(10);
    v_resultado VARCHAR2(20);
    v_numero NUMBER;
BEGIN
    -- Gerar jogada aleatória do PC
    v_numero := DBMS_RANDOM.VALUE(1, 4);
    
    IF v_numero < 2 THEN
        v_jogadaPC := 'Pedra';
    ELSIF v_numero < 3 THEN
        v_jogadaPC := 'Papel';
    ELSE
        v_jogadaPC := 'Tesoura';
    END IF;

    -- Comparar jogadas e definir resultado
    IF p_jogadaUsuario = v_jogadaPC THEN
        v_resultado := 'Empate';
    ELSIF (p_jogadaUsuario = 'Pedra' AND v_jogadaPC = 'Tesoura') OR
          (p_jogadaUsuario = 'Papel' AND v_jogadaPC = 'Pedra') OR
          (p_jogadaUsuario = 'Tesoura' AND v_jogadaPC = 'Papel') THEN
        v_resultado := 'Vitória do Usuário';
    ELSE
        v_resultado := 'Vitória do PC';
    END IF;

    -- Salvar jogada na tabela
    INSERT INTO tbJokenpo (jogadaUsuario, jogadaPC, resultado)
    VALUES (p_jogadaUsuario, v_jogadaPC, v_resultado);
    
    COMMIT;
    
    -- Exibir resultado
    DBMS_OUTPUT.PUT_LINE('Você jogou: ' || p_jogadaUsuario);
    DBMS_OUTPUT.PUT_LINE('PC jogou: ' || v_jogadaPC);
    DBMS_OUTPUT.PUT_LINE('Resultado: ' || v_resultado);
    DBMS_OUTPUT.PUT_LINE('------------------------');
END;
/

-- ============================================================
-- 3. VIEW: ESTATÍSTICAS DO JOGO
-- Requisito c: Consulta com total de vitórias e empates
-- ============================================================
CREATE OR REPLACE VIEW vwEstatisticasJokenpo AS
SELECT
    COUNT(*) AS "Total de Jogadas",
    SUM(CASE WHEN resultado = 'Vitória do Usuário' THEN 1 ELSE 0 END) AS "Vitórias do Usuário",
    SUM(CASE WHEN resultado = 'Vitória do PC' THEN 1 ELSE 0 END) AS "Vitórias do PC",
    SUM(CASE WHEN resultado = 'Empate' THEN 1 ELSE 0 END) AS "Empates"
FROM tbJokenpo;

-- ============================================================
-- 4. VIEW: HISTÓRICO DE JOGADAS
-- ============================================================
CREATE OR REPLACE VIEW vwHistoricoJokenpo AS
SELECT 
    idJogada AS "ID",
    jogadaUsuario AS "Jogada Usuário",
    jogadaPC AS "Jogada PC",
    resultado AS "Resultado",
    TO_CHAR(dataJogada, 'DD/MM/YYYY HH24:MI:SS') AS "Data/Hora"
FROM tbJokenpo
ORDER BY idJogada DESC;

-- ============================================================
-- 5. TESTES - EXECUTAR JOGADAS
-- ============================================================
SET SERVEROUTPUT ON;

BEGIN
    -- Jogar 5 rodadas
    jogarJokenpo('Pedra');
    jogarJokenpo('Papel');
    jogarJokenpo('Tesoura');
    jogarJokenpo('Pedra');
    jogarJokenpo('Papel');
END;
/

-- ============================================================
-- 6. CONSULTAS - VISUALIZAR RESULTADOS
-- ============================================================

-- Ver todas as jogadas
SELECT * FROM vwHistoricoJokenpo;

-- Ver estatísticas
SELECT * FROM vwEstatisticasJokenpo;

-- Consulta adicional: Percentual de vitórias
SELECT 
    resultado,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tbJokenpo), 2) AS percentual
FROM tbJokenpo
GROUP BY resultado
ORDER BY total DESC;

-- ============================================================
-- 7. LIMPEZA (OPCIONAL - USAR APENAS PARA RESETAR)
-- ============================================================
/*
-- Apagar dados
DELETE FROM tbJokenpo;
COMMIT;

-- Dropar objetos
DROP VIEW vwHistoricoJokenpo;
DROP VIEW vwEstatisticasJokenpo;
DROP PROCEDURE jogarJokenpo;
DROP TABLE tbJokenpo;
*/

```

</details>

---

### 🔹 [Exercício 3: Controle de Estoque com Cursor](./EXERCICIO_03.md)

**Pontuação:** 0.5 ponto

#### 📌 Enunciado

Crie e execute uma procedure que receba o ID de um produto e sua quantidade, verifique estoque e processe adequadamente. Além disso, crie uma procedure com cursor que exiba produtos críticos.

#### 🎯 Requisitos Obrigatórios

| # | Requisito | Peso |
|---|-----------|------|
| 1 | Procedure recebe **ID do produto e quantidade** | 20% |
| 2 | **Verificar estoque disponível** | 20% |
| 3 | Se OK: **inserir em tbPedidos e baixar estoque** | 20% |
| 4 | Se não: **registrar em tabela de log** | 20% |
| 5 | Procedure com **CURSOR** para listar produtos com **classificação baixa ou sem estoque** | 20% |

#### ✅ Critérios de Avaliação

- **Validação de estoque** correta
- **Transações consistentes** (pedidos e baixa sincronizados)
- **Log de erros** implementado
- **CURSOR explícito** corretamente declarado e utilizado
- **Tratamento de exceções** (produto inexistente, etc.)

#### 🛠️ Tecnologias

- Oracle Database (Oracle SQL Live)
- PL/SQL
- Cursores explícitos
- Tratamento de exceções

#### 📊 Resumo da Solução

A solução implementa:
1. ✅ **3 tabelas relacionadas**: `tbProdutos`, `tbPedidos`, `tbLogEstoque`
2. ✅ **Procedure `realizarPedido`** com validação e tratamento de exceções
3. ✅ **Procedure `listarProdutosCriticos`** com CURSOR explícito
4. ✅ **3 views** para consulta: pedidos, logs e produtos críticos

**[📖 Ver documentação completa →](./EXERCICIO_03.md)**

<details>
<summary><b>Ver código completo.</b></summary>

## 🔗 Código Completo

### 📄 `database.sql`

```sql

-- ============================================================
-- EXERCÍCIO 03: CONTROLE DE ESTOQUE COM CURSOR
-- Banco de Dados: Oracle
-- Pontuação: 0.5 ponto
-- ============================================================

-- ============================================================
-- 1. CRIAR TABELAS
-- ============================================================

-- Tabela de produtos
CREATE TABLE tbProdutos (
    idProduto NUMBER PRIMARY KEY,
    nomeProduto VARCHAR2(100) NOT NULL,
    classificacao NUMBER NOT NULL,  -- 0 a 10
    estoque NUMBER NOT NULL
);

-- Tabela de pedidos
CREATE TABLE tbPedidos (
    idPedido NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idProduto NUMBER NOT NULL,
    quantidade NUMBER NOT NULL,
    dataPedido DATE DEFAULT SYSDATE,
    FOREIGN KEY (idProduto) REFERENCES tbProdutos(idProduto)
);

-- Tabela de log
CREATE TABLE tbLogEstoque (
    idLog NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idProduto NUMBER,
    quantidadeSolicitada NUMBER NOT NULL,
    mensagem VARCHAR2(200) NOT NULL,
    dataLog DATE DEFAULT SYSDATE
);

-- ============================================================
-- 2. PROCEDURE: REALIZAR PEDIDO
-- Requisito: Receber ID e quantidade, verificar estoque
-- Se OK: inserir pedido e baixar estoque
-- Se NÃO: registrar em log
-- ============================================================
CREATE OR REPLACE PROCEDURE realizarPedido (
    p_idProduto IN NUMBER,
    p_quantidade IN NUMBER
) AS
    v_estoque NUMBER;
    v_nomeProduto VARCHAR2(100);
BEGIN
    -- Verificar se produto existe e pegar estoque
    BEGIN
        SELECT estoque, nomeProduto 
        INTO v_estoque, v_nomeProduto
        FROM tbProdutos
        WHERE idProduto = p_idProduto;
        
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            -- Produto não encontrado - registrar em log
            INSERT INTO tbLogEstoque (idProduto, quantidadeSolicitada, mensagem)
            VALUES (p_idProduto, p_quantidade, 'Produto não encontrado');
            COMMIT;
            
            DBMS_OUTPUT.PUT_LINE('✗ Erro: Produto ' || p_idProduto || ' não existe');
            RETURN;
    END;
    
    -- Verificar se há estoque disponível
    IF v_estoque >= p_quantidade THEN
        -- Estoque OK: inserir pedido
        INSERT INTO tbPedidos (idProduto, quantidade)
        VALUES (p_idProduto, p_quantidade);
        
        -- Baixar estoque
        UPDATE tbProdutos
        SET estoque = estoque - p_quantidade
        WHERE idProduto = p_idProduto;
        
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('✓ Pedido realizado: ' || v_nomeProduto || 
                           ' (Qtd: ' || p_quantidade || ')');
    ELSE
        -- Estoque insuficiente: registrar em log
        INSERT INTO tbLogEstoque (idProduto, quantidadeSolicitada, mensagem)
        VALUES (p_idProduto, p_quantidade, 
                'Estoque insuficiente (Disponível: ' || v_estoque || ')');
        COMMIT;
        
        DBMS_OUTPUT.PUT_LINE('✗ Estoque insuficiente: ' || v_nomeProduto || 
                           ' (Solicitado: ' || p_quantidade || 
                           ', Disponível: ' || v_estoque || ')');
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ Erro inesperado: ' || SQLERRM);
        ROLLBACK;
END;
/

-- ============================================================
-- 3. PROCEDURE: LISTAR PRODUTOS CRÍTICOS COM CURSOR
-- Requisito: Usar cursor para produtos com classificação baixa
-- ou sem estoque
-- ============================================================
CREATE OR REPLACE PROCEDURE listarProdutosCriticos AS
    -- Declarar cursor para produtos críticos
    CURSOR c_criticos IS
        SELECT idProduto, nomeProduto, classificacao, estoque
        FROM tbProdutos
        WHERE classificacao <= 3 OR estoque = 0
        ORDER BY 
            CASE WHEN estoque = 0 THEN 1 ELSE 2 END,
            classificacao;
    
    v_contador NUMBER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE('========================================');
    DBMS_OUTPUT.PUT_LINE('    PRODUTOS CRÍTICOS');
    DBMS_OUTPUT.PUT_LINE('========================================');
    DBMS_OUTPUT.PUT_LINE('');
    
    -- Iterar pelo cursor
    FOR produto IN c_criticos LOOP
        v_contador := v_contador + 1;
        
        DBMS_OUTPUT.PUT_LINE('Produto #' || v_contador);
        DBMS_OUTPUT.PUT_LINE('  ID: ' || produto.idProduto);
        DBMS_OUTPUT.PUT_LINE('  Nome: ' || produto.nomeProduto);
        DBMS_OUTPUT.PUT_LINE('  Classificação: ' || produto.classificacao || '/10');
        DBMS_OUTPUT.PUT_LINE('  Estoque: ' || produto.estoque);
        
        -- Identificar motivo crítico
        IF produto.estoque = 0 THEN
            DBMS_OUTPUT.PUT_LINE('  Status: ⚠️  SEM ESTOQUE');
        ELSIF produto.classificacao <= 3 THEN
            DBMS_OUTPUT.PUT_LINE('  Status: ⚠️  CLASSIFICAÇÃO BAIXA');
        END IF;
        
        DBMS_OUTPUT.PUT_LINE('----------------------------------------');
    END LOOP;
    
    IF v_contador = 0 THEN
        DBMS_OUTPUT.PUT_LINE('✓ Nenhum produto crítico encontrado');
    ELSE
        DBMS_OUTPUT.PUT_LINE('');
        DBMS_OUTPUT.PUT_LINE('Total de produtos críticos: ' || v_contador);
    END IF;
    
    DBMS_OUTPUT.PUT_LINE('========================================');
END;
/

-- ============================================================
-- 4. VIEWS PARA CONSULTA
-- ============================================================

-- View: Histórico de pedidos
CREATE OR REPLACE VIEW vwPedidosRealizados AS
SELECT 
    p.idPedido AS "ID Pedido",
    pr.nomeProduto AS "Produto",
    p.quantidade AS "Quantidade",
    TO_CHAR(p.dataPedido, 'DD/MM/YYYY HH24:MI:SS') AS "Data"
FROM tbPedidos p
JOIN tbProdutos pr ON p.idProduto = pr.idProduto
ORDER BY p.dataPedido DESC;

-- View: Log de erros
CREATE OR REPLACE VIEW vwLogEstoque AS
SELECT 
    l.idLog AS "ID",
    NVL(pr.nomeProduto, 'Produto ID: ' || l.idProduto) AS "Produto",
    l.quantidadeSolicitada AS "Qtd Solicitada",
    l.mensagem AS "Mensagem",
    TO_CHAR(l.dataLog, 'DD/MM/YYYY HH24:MI:SS') AS "Data"
FROM tbLogEstoque l
LEFT JOIN tbProdutos pr ON l.idProduto = pr.idProduto
ORDER BY l.dataLog DESC;

-- View: Produtos críticos
CREATE OR REPLACE VIEW vwProdutosCriticos AS
SELECT 
    idProduto AS "ID",
    nomeProduto AS "Produto",
    classificacao AS "Classificação",
    estoque AS "Estoque",
    CASE 
        WHEN estoque = 0 THEN 'SEM ESTOQUE'
        WHEN classificacao <= 3 THEN 'CLASSIFICAÇÃO BAIXA'
    END AS "Status"
FROM tbProdutos
WHERE classificacao <= 3 OR estoque = 0;

-- ============================================================
-- 5. INSERIR DADOS DE TESTE
-- ============================================================
INSERT INTO tbProdutos VALUES (1, 'Mouse Gamer RGB', 2, 0);
INSERT INTO tbProdutos VALUES (2, 'Teclado Mecâ

```

</details>

---

## 📦 Formato de Entrega

Conforme especificado no enunciado:

### 📄 Arquivos Obrigatórios

1. **Código-fonte** de cada um dos exercícios
2. **Print da tela** após a execução de cada código
3. **(Opcional)** Vídeo demonstrando a aplicação do Exercício 1

### 📁 Estrutura de Arquivos Deste Repositório

```
LBDA_Exercicios/
├── README.md                    # Este arquivo (visão geral)
├── EXERCICIO_01.md             # Documentação completa - Web Scraping
├── EXERCICIO_02.md             # Documentação completa - Jokenpô
├── EXERCICIO_03.md             # Documentação completa - Estoque
│
├── exercicio01/
│   ├── database.sql            # Script MySQL
│   ├── main.py                 # Aplicação Python
│   └── requirements.txt        # Dependências
│
├── exercicio02/
│   └── jokenpo.sql            # Script Oracle completo
│
├── exercicio03/
│   └── estoque.sql            # Script Oracle completo
│
└── prints/
    ├── ex01_python_output.png
    ├── ex01_mysql_tables.png
    ├── ex02_jogadas.png
    ├── ex02_estatisticas.png
    ├── ex03_testes.png
    ├── ex03_cursor.png
    └── ex03_views.png
```

---

## 🎯 Critérios Gerais de Avaliação

### Pontuação por Exercício

| Exercício | Pontos | Descrição |
|-----------|--------|-----------|
| 1 - Web Scraping | 1.0 | Python + MySQL + BeautifulSoup + Procedure |
| 2 - Jokenpô | 0.5 | PL/SQL + Aleatoriedade + Persistência |
| 3 - Estoque | 0.5 | PL/SQL + Cursor + Validação + Log |
| **TOTAL** | **2.0** | **Nota máxima da atividade** |

### Critérios Transversais

- ✅ **Funcionalidade completa** (atende todos os requisitos)
- ✅ **Qualidade do código** (organização, indentação, nomenclatura)
- ✅ **Documentação** (comentários, README, explicações)
- ✅ **Tratamento de erros** (exceções, validações)
- ✅ **Boas práticas** (SQL injection prevention, commits adequados)

---

## 🚀 Como Usar Este Repositório

### 1️⃣ Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd LBDA_Exercicios
```

### 2️⃣ Exercício 1 (Python + MySQL)

```bash
cd exercicio01
pip install -r requirements.txt
# Configurar senha no arquivo main.py
mysql -u root -p < database.sql
python main.py
```

### 3️⃣ Exercício 2 (Oracle)

Acessar [Oracle SQL Live](https://livesql.oracle.com/) e executar `exercicio02/jokenpo.sql`

### 4️⃣ Exercício 3 (Oracle)

Acessar [Oracle SQL Live](https://livesql.oracle.com/) e executar `exercicio03/estoque.sql`

---

## 📚 Conteúdo das Aulas Aplicado

### Conceitos Utilizados

| Conceito | Exercício | Aula |
|----------|-----------|------|
| **Stored Procedures** | 1, 2, 3 | Aula 08 |
| **Views** | 2, 3 | Aula 04 |
| **Cursores Explícitos** | 3 | Aula 09 |
| **PL/SQL Básico** | 2, 3 | Aula 05 |
| **IF-ELSIF-ELSE** | 2, 3 | Aula 05 |
| **CASE WHEN** | 1, 2, 3 | Aula 07 |
| **Tratamento de Exceções** | 3 | Aula 08 |
| **Parâmetros IN/OUT** | 1, 2, 3 | Aula 08 |
| **INSERT, UPDATE, DELETE** | 1, 2, 3 | Aula 03 |

---

## 🔗 Links Úteis

- [Oracle SQL Live](https://livesql.oracle.com/) - Ambiente Oracle online
- [MySQL Documentation](https://dev.mysql.com/doc/) - Documentação MySQL
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Documentação BeautifulSoup
- [Python mysql-connector](https://dev.mysql.com/doc/connector-python/en/) - Conector Python-MySQL

---

## 👥 Equipe

- **Integrante 1:** [Nome]
- **Integrante 2:** [Nome]
- **Integrante 3:** [Nome]

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Laboratório de Banco de Dados Avançado.

---

## ✅ Checklist de Entrega

- [ ] Código do Exercício 1 completo e testado
- [ ] Código do Exercício 2 completo e testado
- [ ] Código do Exercício 3 completo e testado
- [ ] Prints de todos os exercícios capturados
- [ ] Documentação de cada exercício completa
- [ ] README.md principal atualizado
- [ ] (Opcional) Vídeo do Exercício 1
- [ ] Revisão final de todos os arquivos

---

**📅 Data de Entrega:** [Inserir data]  
**📧 Contato:** [Inserir email para dúvidas]

---

> 💡 **Dica:** Leia atentamente cada documento específico (EXERCICIO_XX.md) para instruções detalhadas de execução e explicações técnicas.
