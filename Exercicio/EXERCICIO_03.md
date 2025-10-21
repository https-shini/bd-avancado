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

### Tabela 1: `tbProdutos`

```sql
CREATE TABLE tbProdutos (
    idProduto NUMBER PRIMARY KEY,
    nomeProduto VARCHAR2(100) NOT NULL,
    classificacao NUMBER NOT NULL,  -- 0 a 10
    estoque NUMBER NOT NULL
);
```

**Campos:**
- `idProduto`: Identificador único (chave primária)
- `nomeProduto`: Nome do produto
- `classificacao`: Nota de 0 a 10 (crítico: ≤3)
- `estoque`: Quantidade disponível

**Exemplo de dados:**
```sql
INSERT INTO tbProdutos VALUES (1, 'Mouse Gamer RGB', 2, 0);
INSERT INTO tbProdutos VALUES (2, 'Teclado Mecânico', 9, 15);
INSERT INTO tbProdutos VALUES (3, 'Monitor 24"', 3, 5);
INSERT INTO tbProdutos VALUES (4, 'Headset Gamer', 1, 2);
```

---

### Tabela 2: `tbPedidos`

```sql
CREATE TABLE tbPedidos (
    idPedido NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idProduto NUMBER NOT NULL,
    quantidade NUMBER NOT NULL,
    dataPedido DATE DEFAULT SYSDATE,
    FOREIGN KEY (idProduto) REFERENCES tbProdutos(idProduto)
);
```

**Campos:**
- `idPedido`: ID único do pedido (auto-incremento)
- `idProduto`: Referência ao produto (FK)
- `quantidade`: Quantidade solicitada
- `dataPedido`: Data/hora do pedido (automático)

---

### Tabela 3: `tbLogEstoque`

```sql
CREATE TABLE tbLogEstoque (
    idLog NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idProduto NUMBER,
    quantidadeSolicitada NUMBER NOT NULL,
    mensagem VARCHAR2(200) NOT NULL,
    dataLog DATE DEFAULT SYSDATE
);
```

**Campos:**
- `idLog`: ID único do log (auto-incremento)
- `idProduto`: ID do produto (pode ser NULL se não existe)
- `quantidadeSolicitada`: Quantidade que foi solicitada
- `mensagem`: Descrição do erro
- `dataLog`: Data/hora do erro (automático)

---

## 🔧 Procedure 1: `realizarPedido`

### Código Completo

```sql
CREATE OR REPLACE PROCEDURE realizarPedido (
    p_idProduto IN NUMBER,
    p_quantidade IN NUMBER
) AS
    v_estoque NUMBER;
    v_nomeProduto VARCHAR2(100);
BEGIN
    -- 1. Verificar se produto existe e pegar estoque
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
    
    -- 2. Verificar se há estoque disponível
    IF v_estoque >= p_quantidade THEN
        -- ESTOQUE OK: Inserir pedido e baixar estoque
        
        -- 2.1. Inserir pedido
        INSERT INTO tbPedidos (idProduto, quantidade)
        VALUES (p_idProduto, p_quantidade);
        
        -- 2.2. Baixar estoque
        UPDATE tbProdutos
        SET estoque = estoque - p_quantidade
        WHERE idProduto = p_idProduto;
        
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('✓ Pedido realizado: ' || v_nomeProduto || 
                           ' (Qtd: ' || p_quantidade || ')');
    ELSE
        -- ESTOQUE INSUFICIENTE: Registrar em log
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
```

### Detalhamento Técnico

#### 1️⃣ Bloco BEGIN-EXCEPTION Aninhado

```sql
BEGIN
    SELECT estoque, nomeProduto INTO ...
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        -- Tratar produto inexistente
        INSERT INTO tbLogEstoque ...
        RETURN; -- Sair da procedure
END;
```

**Conceito aplicado:** Aula 08 - Tratamento de exceções em PL/SQL

#### 2️⃣ Validação de Estoque

```sql
IF v_estoque >= p_quantidade THEN
    -- Caminho de sucesso
ELSE
    -- Caminho de erro
END IF;
```

**Conceito aplicado:** Aula 05 - IF-ELSE

#### 3️⃣ Transação Atômica

```sql
-- Operações que devem ocorrer juntas
INSERT INTO tbPedidos ...
UPDATE tbProdutos SET estoque = estoque - p_quantidade ...
COMMIT; -- Confirmar ambas
```

**Conceito aplicado:** Aula 03 - DML e transações

---

## 🔧 Procedure 2: `listarProdutosCriticos`

### Código Completo

```sql
CREATE OR REPLACE PROCEDURE listarProdutosCriticos AS
    -- Declarar CURSOR explícito
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
    
    -- Iterar pelo cursor usando FOR LOOP
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
```

### Detalhamento Técnico

#### 1️⃣ Declaração de CURSOR Explícito

```sql
CURSOR c_criticos IS
    SELECT idProduto, nomeProduto, classificacao, estoque
    FROM tbProdutos
    WHERE classificacao <= 3 OR estoque = 0
    ORDER BY ...
```

**Conceito aplicado:** Aula 09 - Cursores explícitos

**Características:**
- Declarado na seção de declarações (após AS)
- Nome: `c_criticos`
- Query define os registros a serem iterados

#### 2️⃣ FOR LOOP com Cursor

```sql
FOR produto IN c_criticos LOOP
    -- produto.campo acessa colunas do SELECT
    DBMS_OUTPUT.PUT_LINE(produto.nomeProduto);
END LOOP;
```

**Conceito aplicado:** Aula 09 - Iteração com cursores

**Vantagens:**
- ✅ OPEN automático
- ✅ FETCH automático
- ✅ CLOSE automático
- ✅ Código mais limpo

#### 3️⃣ Ordenação Customizada

```sql
ORDER BY 
    CASE WHEN estoque = 0 THEN 1 ELSE 2 END,
    classificacao
```

**Lógica:** 
1. Produtos sem estoque aparecem primeiro
2. Depois ordena por classificação crescente

**Conceito aplicado:** Aula 07 - CASE WHEN

---

## 📊 Views para Consulta

### View 1: `vwPedidosRealizados`

```sql
CREATE OR REPLACE VIEW vwPedidosRealizados AS
SELECT 
    p.idPedido AS "ID Pedido",
    pr.nomeProduto AS "Produto",
    p.quantidade AS "Quantidade",
    TO_CHAR(p.dataPedido, 'DD/MM/YYYY HH24:MI:SS') AS "Data"
FROM tbPedidos p
JOIN tbProdutos pr ON p.idProduto = pr.idProduto
ORDER BY p.dataPedido DESC;
```

**Propósito:** Visualizar histórico de pedidos bem-sucedidos

**Saída esperada:**
```
ID Pedido | Produto           | Quantidade | Data
----------|-------------------|------------|-------------------
    3     | Teclado Mecânico  |     3      | 20/10/2025 14:30:15
    2     | Monitor 24"       |     2      | 20/10/2025 14:25:42
    1     | Webcam Full HD    |     5      | 20/10/2025 14:20:10
```

---

### View 2: `vwLogEstoque`

```sql
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
```

**Propósito:** Rastrear tentativas de pedidos que falharam

**Funções utilizadas:**
- `NVL()`: Substitui NULL por texto alternativo
- `LEFT JOIN`: Inclui logs mesmo se produto não existir mais
- `TO_CHAR()`: Formata data

**Saída esperada:**
```
ID | Produto           | Qtd Solicitada | Mensagem                    | Data
---|-------------------|----------------|-----------------------------|-------------------
3  | Mouse Gamer RGB   |       5        | Estoque insuficiente (0)   | 20/10/2025 14:35:20
2  | Produto ID: 99    |       1        | Produto não encontrado     | 20/10/2025 14:30:15
```

---

### View 3: `vwProdutosCriticos`

```sql
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
```

**Propósito:** Identificar produtos que precisam atenção

**Saída esperada:**
```
ID | Produto           | Classificação | Estoque | Status
---|-------------------|---------------|---------|--------------------
1  | Mouse Gamer RGB   |       2       |    0    | SEM ESTOQUE
3  | Monitor 24"       |       3       |    5    | CLASSIFICAÇÃO BAIXA
4  | Headset Gamer     |       1       |    2    | CLASSIFICAÇÃO BAIXA
```

---

## ▶️ Execução no Oracle SQL Live

### 🌐 Acesse: https://livesql.oracle.com/

### Passo 1: Criar Tabelas

```sql
-- Tabela de Produtos
CREATE TABLE tbProdutos (
    idProduto NUMBER PRIMARY KEY,
    nomeProduto VARCHAR2(100) NOT NULL,
    classificacao NUMBER NOT NULL,
    estoque NUMBER NOT NULL
);

-- Tabela de Pedidos
CREATE TABLE tbPedidos (
    idPedido NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idProduto NUMBER NOT NULL,
    quantidade NUMBER NOT NULL,
    dataPedido DATE DEFAULT SYSDATE,
    FOREIGN KEY (idProduto) REFERENCES tbProdutos(idProduto)
);

-- Tabela de Log
CREATE TABLE tbLogEstoque (
    idLog NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idProduto NUMBER,
    quantidadeSolicitada NUMBER NOT NULL,
    mensagem VARCHAR2(200) NOT NULL,
    dataLog DATE DEFAULT SYSDATE
);
```

✅ **Resultado esperado:** "Table created" (3 vezes)

---

### Passo 2: Inserir Dados de Teste

```sql
INSERT INTO tbProdutos VALUES (1, 'Mouse Gamer RGB', 2, 0);
INSERT INTO tbProdutos VALUES (2, 'Teclado Mecânico', 9, 15);
INSERT INTO tbProdutos VALUES (3, 'Monitor 24 Polegadas', 3, 5);
INSERT INTO tbProdutos VALUES (4, 'Headset Gamer', 1, 2);
INSERT INTO tbProdutos VALUES (5, 'Webcam Full HD', 8, 20);
COMMIT;
```

✅ **Resultado esperado:** "5 rows inserted" + "Commit complete"

---

### Passo 3: Criar Procedures

```sql
-- Procedure 1: Realizar Pedido
CREATE OR REPLACE PROCEDURE realizarPedido (
    p_idProduto IN NUMBER,
    p_quantidade IN NUMBER
) AS
    v_estoque NUMBER;
    v_nomeProduto VARCHAR2(100);
BEGIN
    BEGIN
        SELECT estoque, nomeProduto 
        INTO v_estoque, v_nomeProduto
        FROM tbProdutos
        WHERE idProduto = p_idProduto;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            INSERT INTO tbLogEstoque (idProduto, quantidadeSolicitada, mensagem)
            VALUES (p_idProduto, p_quantidade, 'Produto não encontrado');
            COMMIT;
            DBMS_OUTPUT.PUT_LINE('✗ Erro: Produto ' || p_idProduto || ' não existe');
            RETURN;
    END;
    
    IF v_estoque >= p_quantidade THEN
        INSERT INTO tbPedidos (idProduto, quantidade)
        VALUES (p_idProduto, p_quantidade);
        
        UPDATE tbProdutos
        SET estoque = estoque - p_quantidade
        WHERE idProduto = p_idProduto;
        
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('✓ Pedido realizado: ' || v_nomeProduto || 
                           ' (Qtd: ' || p_quantidade || ')');
    ELSE
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

-- Procedure 2: Listar Produtos Críticos
CREATE OR REPLACE PROCEDURE listarProdutosCriticos AS
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
    
    FOR produto IN c_criticos LOOP
        v_contador := v_contador + 1;
        DBMS_OUTPUT.PUT_LINE('Produto #' || v_contador);
        DBMS_OUTPUT.PUT_LINE('  ID: ' || produto.idProduto);
        DBMS_OUTPUT.PUT_LINE('  Nome: ' || produto.nomeProduto);
        DBMS_OUTPUT.PUT_LINE('  Classificação: ' || produto.classificacao || '/10');
        DBMS_OUTPUT.PUT_LINE('  Estoque: ' || produto.estoque);
        
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
```

✅ **Resultado esperado:** "Procedure compiled" (2 vezes)

---

### Passo 4: Criar Views

```sql
CREATE OR REPLACE VIEW vwPedidosRealizados AS
SELECT 
    p.idPedido AS "ID Pedido",
    pr.nomeProduto AS "Produto",
    p.quantidade AS "Quantidade",
    TO_CHAR(p.dataPedido, 'DD/MM/YYYY HH24:MI:SS') AS "Data"
FROM tbPedidos p
JOIN tbProdutos pr ON p.idProduto = pr.idProduto
ORDER BY p.dataPedido DESC;

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
```

✅ **Resultado esperado:** "View created" (3 vezes)

---

### Passo 5: Executar Testes

```sql
SET SERVEROUTPUT ON;

-- Teste 1: Pedido com estoque disponível
BEGIN
    DBMS_OUTPUT.PUT_LINE('=== TESTE 1: Pedido com estoque ===');
    realizarPedido(2, 3);
    DBMS_OUTPUT.PUT_LINE('');
END
