# 📦 Exercício 3: Controle de Estoque com Cursor

**Pontuação:** 0.5 ponto (25% da nota total)

---

## 📋 Enunciado Completo

> Crie e execute uma procedure que receba o ID de um produto e sua quantidade, em seguida verifique se há estoque disponível. Caso positivo, insira o pedido na tabela tbPedidos e realize a baixa no estoque. Caso contrário, registre a ação em uma tabela de log. Além disso crie uma procedure que utilize cursor que exiba apenas os produtos com classificação baixa ou sem estoque.

### Requisitos Técnicos Detalhados

#### 1️⃣ Procedure de Pedidos (60%)
- **Receber parâmetros:** ID do produto e quantidade
- **Verificar estoque:** Consultar disponibilidade
- **Se estoque OK:**
  - Inserir pedido na tabela `tbPedidos`
  - Realizar baixa no estoque (UPDATE)
- **Se estoque insuficiente:**
  - Registrar na tabela de log (`tbLogEstoque`)
- **Tratamento de exceções:** Produto não encontrado

#### 2️⃣ Procedure com Cursor (40%)
- **Usar CURSOR explícito**
- **Listar produtos críticos:**
  - Classificação baixa (≤ 3)
  - Sem estoque (= 0)
- **Exibir informações detalhadas**

---

## 🎯 Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Validação de Estoque** | 20% | Verificação correta de disponibilidade |
| **Transações Consistentes** | 20% | INSERT em pedidos e UPDATE em estoque sincronizados |
| **Log de Erros** | 20% | Registro adequado de falhas |
| **CURSOR Explícito** | 30% | Declaração e uso correto de cursor |
| **Tratamento de Exceções** | 10% | EXCEPTION para NO_DATA_FOUND |

---

## 🏗️ Arquitetura da Solução

```
┌───────────────────────────────────────────────────────────────┐
│                     ORACLE DATABASE                           │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    TABELAS                              │ │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐     │ │
│  │  │tbProdutos  │  │ tbPedidos  │  │tbLogEstoque  │     │ │
│  │  │            │  │            │  │              │     │ │
│  │  │ ID         │  │ ID         │  │ ID           │     │ │
│  │  │ Nome       │◄─┤ idProduto  │  │ idProduto    │     │ │
│  │  │ Classificaç│  │ Quantidade │  │ Qtd Solicit. │     │ │
│  │  │ Estoque    │  │ Data       │  │ Mensagem     │     │ │
│  │  └────────────┘  └────────────┘  └──────────────┘     │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │         PROCEDURE: realizarPedido(id, qtd)              │ │
│  │                                                         │ │
│  │  1. SELECT estoque FROM tbProdutos WHERE id = ?         │ │
│  │  2. IF estoque >= quantidade THEN                       │ │
│  │     ├─ INSERT INTO tbPedidos                            │ │
│  │     └─ UPDATE tbProdutos SET estoque -= qtd             │ │
│  │     ELSE                                                │ │
│  │     └─ INSERT INTO tbLogEstoque (erro)                  │ │
│  │  3. EXCEPTION NO_DATA_FOUND → log                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │    PROCEDURE: listarProdutosCriticos (CURSOR)           │ │
│  │                                                         │ │
│  │  CURSOR c_criticos IS                                   │ │
│  │    SELECT * FROM tbProdutos                             │ │
│  │    WHERE classificacao <= 3 OR estoque = 0              │ │
│  │                                                         │ │
│  │  FOR produto IN c_criticos LOOP                         │ │
│  │    DBMS_OUTPUT.PUT_LINE(dados)                          │ │
│  │  END LOOP                                               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                      3 VIEWS                            │ │
│  │  • vwPedidosRealizados                                  │ │
│  │  • vwLogEstoque                                         │ │
│  │  • vwProdutosCriticos                                   │ │
│  └─────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

---

## 💾 Estrutura do Banco de Dados Oracle

```sql
  CREATE TABLE tbProdutos (
      idProduto NUMBER PRIMARY KEY,
      nomeProduto VARCHAR2(100),
      classificacao NUMBER,
      estoque NUMBER
  );
  
  CREATE TABLE tbPedidos (
      idPedido NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      idProduto NUMBER,
      quantidade NUMBER,
      dataPedido DATE DEFAULT SYSDATE
  );
  
  CREATE TABLE tbLogEstoque (
      idLog NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      idProduto NUMBER,
      quantidadeSolicitada NUMBER,
      dataLog DATE DEFAULT SYSDATE,
      mensagem VARCHAR2(200)
  );
  
  CREATE OR REPLACE PROCEDURE realizarPedido (
      p_idProduto IN NUMBER,
      p_quantidade IN NUMBER
  ) AS
      v_estoque NUMBER;
  BEGIN
      SELECT estoque INTO v_estoque
      FROM tbProdutos
      WHERE idProduto = p_idProduto;
  
      IF v_estoque >= p_quantidade THEN
          INSERT INTO tbPedidos (idProduto, quantidade)
          VALUES (p_idProduto, p_quantidade);
  
          UPDATE tbProdutos
          SET estoque = estoque - p_quantidade
          WHERE idProduto = p_idProduto;
  
          DBMS_OUTPUT.PUT_LINE('Pedido realizado com sucesso.');
      ELSE
          INSERT INTO tbLogEstoque (idProduto, quantidadeSolicitada, mensagem)
          VALUES (p_idProduto, p_quantidade, 'Estoque insuficiente');
  
          DBMS_OUTPUT.PUT_LINE('Estoque insuficiente. Pedido não realizado.');
      END IF;
  
  EXCEPTION
      WHEN NO_DATA_FOUND THEN
          INSERT INTO tbLogEstoque (idProduto, quantidadeSolicitada, mensagem)
          VALUES (p_idProduto, p_quantidade, 'Produto não encontrado');
  
          DBMS_OUTPUT.PUT_LINE('Produto não encontrado. Pedido não realizado.');
  END;
  /
  
  CREATE OR REPLACE PROCEDURE listarProdutosCriticos IS
      CURSOR cur_criticos IS
          SELECT idProduto, nomeProduto, classificacao, estoque
          FROM tbProdutos
          WHERE classificacao <= 3 OR estoque = 0;
  
      v_idProduto tbProdutos.idProduto%TYPE;
      v_nomeProduto tbProdutos.nomeProduto%TYPE;
      v_classificacao tbProdutos.classificacao%TYPE;
      v_estoque tbProdutos.estoque%TYPE;
  BEGIN
      DBMS_OUTPUT.PUT_LINE('==============================');
      DBMS_OUTPUT.PUT_LINE('Produtos Críticos:');
      DBMS_OUTPUT.PUT_LINE('------------------------------');
  
      OPEN cur_criticos;
      LOOP
          FETCH cur_criticos INTO v_idProduto, v_nomeProduto, v_classificacao, v_estoque;
          EXIT WHEN cur_criticos%NOTFOUND;
  
          DBMS_OUTPUT.PUT_LINE('ID: ' || v_idProduto || 
                               ' | Produto: ' || v_nomeProduto || 
                               ' | Classificação: ' || v_classificacao || 
                               ' | Estoque: ' || v_estoque);
      END LOOP;
      CLOSE cur_criticos;
  END;
  /
  
  INSERT INTO tbProdutos VALUES (1, 'Mouse Gamer', 2, 0);
  INSERT INTO tbProdutos VALUES (2, 'Teclado Mecânico', 9, 10);
  INSERT INTO tbProdutos VALUES (3, 'Monitor 24"', 3, 5);
  COMMIT;
  
  SET SERVEROUTPUT ON;
  
  BEGIN
      realizarPedido(2, 3);
      realizarPedido(1, 1);
      realizarPedido(99, 1);
  END;
  /
  
  BEGIN
      listarProdutosCriticos;
  END;
  /
  
  CREATE OR REPLACE VIEW vwPedidosRealizados AS
  SELECT 
      p.idPedido AS "ID do Pedido",
      pr.nomeProduto AS "Produto",
      p.quantidade AS "Quantidade",
      TO_CHAR(p.dataPedido, 'DD/MM/YYYY HH24:MI') AS "Data do Pedido"
  FROM tbPedidos p
  JOIN tbProdutos pr ON p.idProduto = pr.idProduto;
  
  CREATE OR REPLACE VIEW vwLogEstoque AS
  SELECT 
      l.idLog AS "ID do Log",
      NVL(pr.nomeProduto, 'Produto não cadastrado') AS "Produto",
      l.quantidadeSolicitada AS "Quantidade Solicitada",
      TO_CHAR(l.dataLog, 'DD/MM/YYYY HH24:MI') AS "Data do Log",
      l.mensagem AS "Mensagem"
  FROM tbLogEstoque l
  LEFT JOIN tbProdutos pr ON l.idProduto = pr.idProduto;
  
  CREATE OR REPLACE VIEW vwProdutosCriticos AS
  SELECT 
      idProduto AS "ID do Produto",
      nomeProduto AS "Produto",
      classificacao AS "Classificação",
      estoque AS "Estoque"
  FROM tbProdutos
  WHERE classificacao <= 3 OR estoque = 0;
  
  SELECT * FROM vwPedidosRealizados;
  SELECT * FROM vwLogEstoque;
  SELECT * FROM vwProdutosCriticos;
  
  DELETE FROM tbPedidos;
  DELETE FROM tbLogEstoque;
  DELETE FROM tbProdutos;
  COMMIT;
  
  DROP VIEW vwPedidosRealizados;
  DROP VIEW vwLogEstoque;
  DROP VIEW vwProdutosCriticos;
  
  DROP PROCEDURE realizarPedido;
  DROP PROCEDURE listarProdutosCriticos;
  
  DROP TABLE tbPedidos;
  DROP TABLE tbLogEstoque;
  DROP TABLE tbProdutos;

);
```
