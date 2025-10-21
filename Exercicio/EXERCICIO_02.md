# 🎮 Exercício 2: Jogo Jokenpô em PL/SQL

**Pontuação:** 0.5 ponto (25% da nota total)

---

## 📋 Enunciado Completo

> Utilizando PL/SQL, crie um script que simule o jogo Jokenpô (Pedra, Papel e Tesoura), com os seguintes requisitos:

### Requisitos Técnicos

#### a) Jogadas - Usuário e Computador (30%)
- O usuário deverá **informar a sua jogada** (Pedra, Papel ou Tesoura)
- O Oracle deverá **gerar automaticamente a jogada do PC**, de forma **aleatória**

#### b) Comparação e Resultado (30%)
- O script deve **comparar as jogadas** do usuário e do computador
- **Definir** se a jogada resultou em:
  - Empate
  - Vitória do usuário
  - Vitória do PC

#### c) Persistência e Estatísticas (40%)
- **Salvar cada jogada** realizada em uma tabela (INSERT)
- Criar uma **consulta** que exiba:
  - Total de vitórias do Usuário
  - Total de vitórias do PC
  - Total de empates

---

## 🎯 Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Geração Aleatória** | 25% | Uso correto de `DBMS_RANDOM` |
| **Lógica de Comparação** | 25% | Todas as combinações implementadas |
| **Persistência** | 25% | INSERT correto após cada jogada |
| **Consultas/Views** | 25% | Estatísticas completas e corretas |

---

## 🏗️ Arquitetura da Solução

```
┌────────────────────────────────────────────────────────┐
│                   ORACLE DATABASE                      │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │           Tabela: tbJokenpo                     │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │ idJogada | jogadaUsuario | jogadaPC |   │  │  │
│  │  │ resultado | dataJogada                   │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │      Procedure: jogarJokenpo(p_jogada)         │  │
│  │  1. Gera jogada PC (DBMS_RANDOM)               │  │
│  │  2. Compara jogadas (IF-ELSIF-ELSE)            │  │
│  │  3. Determina resultado                         │  │
│  │  4. INSERT na tabela                            │  │
│  │  5. DBMS_OUTPUT resultado                       │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │        View: vwEstatisticasJokenpo             │  │
│  │  - Total de Jogadas                            │  │
│  │  - Vitórias do Usuário                         │  │
│  │  - Vitórias do PC                              │  │
│  │  - Empates                                     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │        View: vwHistoricoJokenpo                │  │
│  │  - Histórico completo de partidas              │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## 💾 Estrutura do Banco de Dados Oracle

### Tabela: `tbJokenpo`

```sql
CREATE TABLE tbJokenpo (
    idJogada NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    jogadaUsuario VARCHAR2(10) NOT NULL,
    jogadaPC VARCHAR2(10) NOT NULL,
    resultado VARCHAR2(20) NOT NULL,
    dataJogada DATE DEFAULT SYSDATE
);
```

**Campos:**
- `idJogada`: Identificador único (auto-incremento Oracle 12c+)
- `jogadaUsuario`: Jogada do usuário (Pedra/Papel/Tesoura)
- `jogadaPC`: Jogada gerada pelo computador
- `resultado`: Resultado da partida (Empate/Vitória do Usuário/Vitória do PC)
- `dataJogada`: Data e hora da jogada (automático)

---

## 🎲 Lógica do Jogo Jokenpô

### Regras do Jogo

```
Pedra    vs Tesoura  → Pedra vence
Papel    vs Pedra    → Papel vence
Tesoura  vs Papel    → Tesoura vence
X        vs X        → Empate
```

### Matriz de Resultados

| Usuário ↓ / PC → | Pedra | Papel | Tesoura |
|------------------|-------|-------|---------|
| **Pedra**        | Empate | PC vence | Usuário vence |
| **Papel**        | Usuário vence | Empate | PC vence |
| **Tesoura**      | PC vence | Usuário vence | Empate |

---

## 🔧 Stored Procedure: `jogarJokenpo`

### Código Completo

```sql
CREATE OR REPLACE PROCEDURE jogarJokenpo (
    p_jogadaUsuario IN VARCHAR2
) AS
    v_jogadaPC VARCHAR2(10);
    v_resultado VARCHAR2(20);
    v_numero NUMBER;
BEGIN
    -- 1. Gerar jogada aleatória do PC
    v_numero := DBMS_RANDOM.VALUE(1, 4);
    
    IF v_numero < 2 THEN
        v_jogadaPC := 'Pedra';
    ELSIF v_numero < 3 THEN
        v_jogadaPC := 'Papel';
    ELSE
        v_jogadaPC := 'Tesoura';
    END IF;

    -- 2. Comparar jogadas e definir resultado
    IF p_jogadaUsuario = v_jogadaPC THEN
        v_resultado := 'Empate';
        
    ELSIF (p_jogadaUsuario = 'Pedra' AND v_jogadaPC = 'Tesoura') OR
          (p_jogadaUsuario = 'Papel' AND v_jogadaPC = 'Pedra') OR
          (p_jogadaUsuario = 'Tesoura' AND v_jogadaPC = 'Papel') THEN
        v_resultado := 'Vitória do Usuário';
        
    ELSE
        v_resultado := 'Vitória do PC';
    END IF;

    -- 3. Salvar jogada na tabela
    INSERT INTO tbJokenpo (jogadaUsuario, jogadaPC, resultado)
    VALUES (p_jogadaUsuario, v_jogadaPC, v_resultado);
    
    COMMIT;
    
    -- 4. Exibir resultado
    DBMS_OUTPUT.PUT_LINE('Você jogou: ' || p_jogadaUsuario);
    DBMS_OUTPUT.PUT_LINE('PC jogou: ' || v_jogadaPC);
    DBMS_OUTPUT.PUT_LINE('Resultado: ' || v_resultado);
    DBMS_OUTPUT.PUT_LINE('------------------------');
END;
/
```

### Detalhamento Técnico

#### 1️⃣ Geração Aleatória (DBMS_RANDOM)

```sql
v_numero := DBMS_RANDOM.VALUE(1, 4);
```

- `DBMS_RANDOM.VALUE(1, 4)` retorna número entre 1.0 e 3.999...
- Distribuição: 
  - 1.0 ≤ x < 2.0 → Pedra (33.3%)
  - 2.0 ≤ x < 3.0 → Papel (33.3%)
  - 3.0 ≤ x < 4.0 → Tesoura (33.3%)

#### 2️⃣ Comparação com IF-ELSIF-ELSE

```sql
IF p_jogadaUsuario = v_jogadaPC THEN
    -- Mesma jogada = Empate
    
ELSIF (condições de vitória usuário) THEN
    -- Usuário venceu
    
ELSE
    -- PC venceu (todas outras combinações)
END IF;
```

**Conceito aplicado:** Aula 05 - Estruturas de controle de fluxo

#### 3️⃣ Persistência

```sql
INSERT INTO tbJokenpo (jogadaUsuario, jogadaPC, resultado)
VALUES (p_jogadaUsuario, v_jogadaPC, v_resultado);
COMMIT;
```

**Conceito aplicado:** Aula 03 - DML (INSERT)

---

## 📊 Views para Consulta

### View 1: `vwEstatisticasJokenpo`

```sql
CREATE OR REPLACE VIEW vwEstatisticasJokenpo AS
SELECT
    COUNT(*) AS "Total de Jogadas",
    SUM(CASE WHEN resultado = 'Vitória do Usuário' THEN 1 ELSE 0 END) AS "Vitórias do Usuário",
    SUM(CASE WHEN resultado = 'Vitória do PC' THEN 1 ELSE 0 END) AS "Vitórias do PC",
    SUM(CASE WHEN resultado = 'Empate' THEN 1 ELSE 0 END) AS "Empates"
FROM tbJokenpo;
```

**Conceitos aplicados:**
- Aula 04 - Views
- Aula 07 - CASE WHEN
- Funções agregadas (COUNT, SUM)

**Saída esperada:**

```
Total de Jogadas | Vitórias do Usuário | Vitórias do PC | Empates
-----------------|---------------------|----------------|--------
      10         |          3          |       5        |    2
```

### View 2: `vwHistoricoJokenpo`

```sql
CREATE OR REPLACE VIEW vwHistoricoJokenpo AS
SELECT 
    idJogada AS "ID",
    jogadaUsuario AS "Jogada Usuário",
    jogadaPC AS "Jogada PC",
    resultado AS "Resultado",
    TO_CHAR(dataJogada, 'DD/MM/YYYY HH24:MI:SS') AS "Data/Hora"
FROM tbJokenpo
ORDER BY idJogada DESC;
```

**Conceitos aplicados:**
- Aula 04 - Views
- Formatação de datas com `TO_CHAR`

**Saída esperada:**

```
ID | Jogada Usuário | Jogada PC | Resultado            | Data/Hora
---|----------------|-----------|----------------------|-------------------
5  | Tesoura        | Pedra     | Vitória do PC        | 20/10/2025 14:30:15
4  | Papel          | Pedra     | Vitória do Usuário   | 20/10/2025 14:29:42
3  | Pedra          | Pedra     | Empate               | 20/10/2025 14:29:10
```

---

## ▶️ Execução no Oracle SQL Live

### 🌐 Acesse: https://livesql.oracle.com/

### Passo 1: Criar Tabela

```sql
-- Copiar e executar
CREATE TABLE tbJokenpo (
    idJogada NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    jogadaUsuario VARCHAR2(10) NOT NULL,
    jogadaPC VARCHAR2(10) NOT NULL,
    resultado VARCHAR2(20) NOT NULL,
    dataJogada DATE DEFAULT SYSDATE
);
```

✅ **Resultado esperado:** "Table TBJOKENPO created."

---

### Passo 2: Criar Procedure

```sql
-- Copiar e executar
CREATE OR REPLACE PROCEDURE jogarJokenpo (
    p_jogadaUsuario IN VARCHAR2
) AS
    v_jogadaPC VARCHAR2(10);
    v_resultado VARCHAR2(20);
    v_numero NUMBER;
BEGIN
    v_numero := DBMS_RANDOM.VALUE(1, 4);
    
    IF v_numero < 2 THEN
        v_jogadaPC := 'Pedra';
    ELSIF v_numero < 3 THEN
        v_jogadaPC := 'Papel';
    ELSE
        v_jogadaPC := 'Tesoura';
    END IF;

    IF p_jogadaUsuario = v_jogadaPC THEN
        v_resultado := 'Empate';
    ELSIF (p_jogadaUsuario = 'Pedra' AND v_jogadaPC = 'Tesoura') OR
          (p_jogadaUsuario = 'Papel' AND v_jogadaPC = 'Pedra') OR
          (p_jogadaUsuario = 'Tesoura' AND v_jogadaPC = 'Papel') THEN
        v_resultado := 'Vitória do Usuário';
    ELSE
        v_resultado := 'Vitória do PC';
    END IF;

    INSERT INTO tbJokenpo (jogadaUsuario, jogadaPC, resultado)
    VALUES (p_jogadaUsuario, v_jogadaPC, v_resultado);
    
    COMMIT;
    
    DBMS_OUTPUT.PUT_LINE('Você jogou: ' || p_jogadaUsuario);
    DBMS_OUTPUT.PUT_LINE('PC jogou: ' || v_jogadaPC);
    DBMS_OUTPUT.PUT_LINE('Resultado: ' || v_resultado);
    DBMS_OUTPUT.PUT_LINE('------------------------');
END;
/
```

✅ **Resultado esperado:** "Procedure JOGARJOKENPO compiled"

---

### Passo 3: Criar Views

```sql
-- View de Estatísticas
CREATE OR REPLACE VIEW vwEstatisticasJokenpo AS
SELECT
    COUNT(*) AS "Total de Jogadas",
    SUM(CASE WHEN resultado = 'Vitória do Usuário' THEN 1 ELSE 0 END) AS "Vitórias do Usuário",
    SUM(CASE WHEN resultado = 'Vitória do PC' THEN 1 ELSE 0 END) AS "Vitórias do PC",
    SUM(CASE WHEN resultado = 'Empate' THEN 1 ELSE 0 END) AS "Empates"
FROM tbJokenpo;

-- View de Histórico
CREATE OR REPLACE VIEW vwHistoricoJokenpo AS
SELECT 
    idJogada AS "ID",
    jogadaUsuario AS "Jogada Usuário",
    jogadaPC AS "Jogada PC",
    resultado AS "Resultado",
    TO_CHAR(dataJogada, 'DD/MM/YYYY HH24:MI:SS') AS "Data/Hora"
FROM tbJokenpo
ORDER BY idJogada DESC;
```

✅ **Resultado esperado:** "View created."

---

### Passo 4: Executar Jogadas

```sql
-- ⚠️ IMPORTANTE: Habilitar saída
SET SERVEROUTPUT ON;

-- Jogar 5 rodadas
BEGIN
    jogarJokenpo('Pedra');
    jogarJokenpo('Papel');
    jogarJokenpo('Tesoura');
    jogarJokenpo('Pedra');
    jogarJokenpo('Papel');
END;
/
```

✅ **Saída esperada:**

```
Você jogou: Pedra
PC jogou: Tesoura
Resultado: Vitória do Usuário
------------------------
Você jogou: Papel
PC jogou: Papel
Resultado: Empate
------------------------
Você jogou: Tesoura
PC jogou: Pedra
Resultado: Vitória do PC
------------------------
...
```

---

### Passo 5: Consultar Resultados

```sql
-- Ver todas as jogadas
SELECT * FROM vwHistoricoJokenpo;

-- Ver estatísticas
SELECT * FROM vwEstatisticasJokenpo;

-- Consulta adicional: Percentuais
SELECT 
    resultado,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tbJokenpo), 2) AS percentual
FROM tbJokenpo
GROUP BY resultado
ORDER BY total DESC;
```

---

## 🧪 Testes e Validação

### Teste 1: Todas as Combinações

```sql
SET SERVEROUTPUT ON;

BEGIN
    -- Testar todas as possibilidades
    jogarJokenpo('Pedra');
    jogarJokenpo('Pedra');
    jogarJokenpo('Pedra');
    jogarJokenpo('Papel');
    jogarJokenpo('Papel');
    jogarJokenpo('Papel');
    jogarJokenpo('Tesoura');
    jogarJokenpo('Tesoura');
    jogarJokenpo('Tesoura');
END;
/
```

**Validar:**
- ✅ Pelo menos 1 empate
- ✅ Pelo menos 1 vitória usuário
- ✅ Pelo menos 1 vitória PC

---

### Teste 2: Verificar Distribuição Aleatória

```sql
-- Jogar 100 vezes e verificar distribuição
BEGIN
    FOR i IN 1..100 LOOP
        jogarJokenpo('Pedra');
    END LOOP;
END;
/

-- Verificar distribuição das jogadas do PC
SELECT 
    jogadaPC,
    COUNT(*) AS vezes,
    ROUND(COUNT(*) * 100.0 / 100, 2) AS percentual
FROM tbJokenpo
GROUP BY jogadaPC
ORDER BY jogadaPC;
```

**Resultado esperado:** Cada jogada deve aparecer ~33% das vezes

---

### Teste 3: Integridade dos Dados

```sql
-- Verificar se todas as jogadas foram salvas
SELECT COUNT(*) AS total_registros FROM tbJokenpo;

-- Verificar se não há valores NULL
SELECT 
    COUNT(*) AS total,
    COUNT(jogadaUsuario) AS com_jogada_usuario,
    COUNT(jogadaPC) AS com_jogada_pc,
    COUNT(resultado) AS com_resultado
FROM tbJokenpo;
```

**Validar:** Todos os COUNTs devem ser iguais

---

## 📸 Prints para Entrega

### Print 1: Criação dos Objetos
Capturar:
- ✅ CREATE TABLE com sucesso
- ✅ CREATE PROCEDURE com sucesso
- ✅ CREATE VIEW com sucesso

### Print 2: Execução das Jogadas
Capturar terminal com:
- ✅ SET SERVEROUTPUT ON
- ✅ Resultado de 5 jogadas diferentes
- ✅ Mensagens de cada partida

### Print 3: View de Estatísticas
```sql
SELECT * FROM vwEstatisticasJokenpo;
```
Capturar tabela mostrando:
- Total de Jogadas
- Vitórias do Usuário
- Vitórias do PC
- Empates

### Print 4: View de Histórico
```sql
SELECT * FROM vwHistoricoJokenpo;
```
Capturar primeiras 10 linhas do histórico

---

## 📚 Conceitos de PL/SQL Aplicados

### 1. **Blocos Anônimos e Procedures** (Aula 08)
- Estrutura BEGIN...END
- Parâmetros IN
- Criação de procedures

### 2. **IF-ELSIF-ELSE** (Aula 05)
- Estruturas condicionais
- Comparação de strings
- Operadores lógicos (OR, AND)

### 3. **DBMS_RANDOM** (Aula 05)
- Geração de números aleatórios
- `DBMS_RANDOM.VALUE(min, max)`

### 4. **DBMS_OUTPUT** (Aula 05)
- Exibição de mensagens
- `PUT_LINE` para output
- `SET SERVEROUTPUT ON`

### 5. **DML - INSERT** (Aula 03)
- Inserção de dados
- COMMIT de transações

### 6. **Views** (Aula 04)
- CREATE OR REPLACE VIEW
- Abstração de consultas complexas

### 7. **CASE WHEN** (Aula 07)
- Expressões condicionais em SELECT
- SUM com CASE para agregações

### 8. **Funções Agregadas**
- COUNT(*), SUM()
- GROUP BY

---

## 🔄 Fluxograma da Procedure

```
┌─────────────────────────┐
│   jogarJokenpo(jogada)  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Gerar número aleatório  │
│ DBMS_RANDOM.VALUE(1,4)  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Determinar jogada PC    │
│ 1-2: Pedra              │
│ 2-3: Papel              │
│ 3-4: Tesoura            │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Comparar jogadas        │
│ IF jogada = jogadaPC    │
└────────────┬────────────┘
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
   ┌───────┐   ┌────────────┐
   │Empate │   │Quem venceu?│
   └───┬───┘   └─────┬──────┘
       │             │
       │      ┌──────┴──────┐
       │      ▼             ▼
       │  ┌─────────┐  ┌────────┐
       │  │Usuário  │  │   PC   │
       │  │venceu   │  │ venceu │
       │  └────┬────┘  └───┬────┘
       │       │           │
       └───────┴───────────┘
               │
               ▼
┌─────────────────────────┐
│ INSERT na tabela        │
│ tbJokenpo               │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ COMMIT                  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ DBMS_OUTPUT resultado   │
└─────────────────────────┘
```

---

## 🚨 Troubleshooting

### Erro: "identifier 'DBMS_OUTPUT.PUT_LINE' must be declared"
**Solução:** Executar `SET SERVEROUTPUT ON;` antes de chamar a procedure

### Erro: "table or view does not exist"
**Solução:** Criar a tabela `tbJokenpo` primeiro

### Nenhuma saída aparece
**Solução:** 
```sql
SET SERVEROUTPUT ON SIZE 1000000;
```

### Jogada do PC sempre a mesma
**Solução:** Verificar implementação de `DBMS_RANDOM.VALUE`

---

## 📁 Arquivo Completo: `jokenpo.sql`

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

---

## ✅ Checklist de Validação

- [ ] Tabela `tbJokenpo` criada com sucesso
- [ ] Procedure `jogarJokenpo` compilada sem erros
- [ ] Views `vwEstatisticasJokenpo` e `vwHistoricoJokenpo` criadas
- [ ] Jogadas executadas com `SET SERVEROUTPUT ON`
- [ ] Saída mostra resultado de cada partida
- [ ] Dados inseridos na tabela confirmados
- [ ] View de estatísticas mostra totais corretos
- [ ] View de histórico lista todas as jogadas
- [ ] Prints capturados para entrega
- [ ] Código comentado e documentado

---

## 🎓 Aprendizados do Exercício

Este exercício demonstra:

1. **Aleatoriedade em PL/SQL** - Uso do package `DBMS_RANDOM`
2. **Lógica condicional complexa** - Múltiplas condições com OR
3. **Persistência de dados** - INSERT após cada operação
4. **Views para relatórios** - Agregação de dados com CASE WHEN
5. **Procedures parametrizadas** - Receber entrada do usuário
6. **Tratamento de transações** - COMMIT explícito

---

## 📊 Exemplo de Resultados

### Após 10 Jogadas

**vwEstatisticasJokenpo:**
```
Total de Jogadas | Vitórias do Usuário | Vitórias do PC | Empates
-----------------|---------------------|----------------|--------
      10         |          3          |       5        |    2
```

**vwHistoricoJokenpo (últimas 5):**
```
ID | Jogada Usuário | Jogada PC | Resultado            | Data/Hora
---|----------------|-----------|----------------------|-------------------
10 | Papel          | Tesoura   | Vitória do PC        | 20/10/2025 15:45:32
9  | Pedra          | Pedra     | Empate               | 20/10/2025 15:45:31
8  | Tesoura        | Papel     | Vitória do Usuário   | 20/10/2025 15:45:30
7  | Papel          | Pedra     | Vitória do Usuário   | 20/10/2025 15:45:29
6  | Pedra          | Papel     | Vitória do PC        | 20/10/2025 15:45:28
```

---

## 🔗 Referências

- [Oracle DBMS_RANDOM Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_RANDOM.html)
- [Oracle PL/SQL IF Statement](https://docs.oracle.com/en/database/oracle/oracle-database/19/lnpls/plsql-control-statements.html)
- [Oracle DBMS_OUTPUT](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_OUTPUT.html)

---

**📅 Última atualização:** 20/10/2025  
**✍️ Autor:** Equipe LBDA  
**📧 Dúvidas:** Consultar professor ou monitor
