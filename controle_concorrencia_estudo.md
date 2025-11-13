# Controle de Concorrência em Banco de Dados

## 📋 Sumário
1. [Conceitos Fundamentais](#conceitos-fundamentais)
2. [Propriedades ACID](#propriedades-acid)
3. [Níveis de Isolamento](#níveis-de-isolamento)
4. [Tipos de Locks (Bloqueios)](#tipos-de-locks)
5. [Deadlock](#deadlock)
6. [Controle Otimista](#controle-otimista)
7. [Exercícios Práticos](#exercícios-práticos)

---

## 🎯 Conceitos Fundamentais

### O que é Controle de Concorrência?

São **técnicas utilizadas para gerenciar o acesso simultâneo a dados** por várias transações ou usuários em um sistema de banco de dados.

### Por que é importante?

- Garante que múltiplos processos possam acessar dados simultaneamente
- Mantém a **integridade dos dados**
- Evita conflitos e inconsistências
- Fundamental em ambientes multiusuário

---

## 🔐 Propriedades ACID

O controle de concorrência está diretamente relacionado ao **isolamento de transações**. As propriedades ACID garantem a confiabilidade das transações:

### **A** - Atomicidade
- **"Tudo ou nada"**
- Todas as operações são executadas completamente OU não são executadas
- Não existe estado intermediário

**Exemplo:** Transferência bancária - o débito e crédito devem ocorrer juntos ou não ocorrer.

### **C** - Consistência (Consistency)
- A transação leva o banco de um **estado consistente para outro estado consistente**
- Todas as regras de integridade são mantidas
- As restrições do banco não são violadas

### **I** - Isolamento (Isolation)
- **Transações concorrentes não interferem umas nas outras**
- Cada transação é executada como se fosse a única no sistema
- Evita problemas como leituras sujas e fantasmas

### **D** - Durabilidade (Durability)
- Após o COMMIT, os efeitos são **permanentes**
- Mesmo em caso de falha do sistema, os dados persistem
- Garantido através de logs de transação

---

## 💻 Comandos Básicos de Transação

```sql
-- Iniciar uma transação
BEGIN TRANSACTION;

-- Executar operações
UPDATE conta SET saldo = saldo - 100 WHERE id = 1;
UPDATE conta SET saldo = saldo + 100 WHERE id = 2;

-- Confirmar a transação (tornar permanente)
COMMIT;

-- OU desfazer a transação (em caso de erro)
ROLLBACK;
```

---

## 📊 Níveis de Isolamento de Transações (Oracle)

### 1. READ UNCOMMITTED
- **Menos restritivo**
- Permite leitura de dados **não confirmados** (dirty read)
- ⚠️ Risco: Pode ler dados que serão desfeitos

### 2. READ COMMITTED (Padrão no Oracle)
- Lê apenas dados **confirmados**
- ⚠️ Problema: **Non-repeatable read** - mesma consulta pode retornar resultados diferentes

**Exemplo de Non-repeatable Read:**
```sql
-- Transação 1
SELECT saldo FROM conta WHERE id = 1; -- Retorna 1000

-- Transação 2 (em paralelo) faz UPDATE e COMMIT

-- Transação 1 (mesma transação)
SELECT saldo FROM conta WHERE id = 1; -- Retorna 500 (diferente!)
```

### 3. REPEATABLE READ
- Garante que a **mesma leitura retorne os mesmos dados**
- Protege contra non-repeatable reads
- Mantém consistência dentro da transação

### 4. SERIALIZABLE
- **Nível mais alto de isolamento**
- Transações parecem executar **sequencialmente**
- Elimina todos os problemas de concorrência
- ⚠️ Pode reduzir significativamente a performance

### Definindo o Nível de Isolamento

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

---

## 🔒 Tipos de Locks (Bloqueios)

Locks garantem que duas ou mais transações não modifiquem os mesmos dados simultaneamente.

### 1. Bloqueio de Linha (Row-level Lock)
- Bloqueia **apenas uma linha específica**
- Maior granularidade = maior concorrência
- Outras linhas permanecem acessíveis

```sql
SELECT * FROM tabela WHERE id = 1 FOR UPDATE;
```

### 2. Bloqueio de Tabela (Table-level Lock)
- Bloqueia a **tabela inteira**
- Menor granularidade = menor concorrência
- Usado em operações massivas

### 3. Bloqueio Exclusivo (Exclusive Lock)
- **Impede leitura E escrita** por outras transações
- Usado em operações de UPDATE, DELETE, INSERT
- Nenhuma outra transação pode acessar

### 4. Bloqueio Compartilhado (Shared Lock)
- **Permite leitura, mas não modificação**
- Múltiplas transações podem ter shared lock simultaneamente
- Usado em operações SELECT

### Exemplo Prático de Lock

```sql
BEGIN TRANSACTION;

-- Bloqueia a linha para atualização
SELECT * FROM conta WHERE id = 1 FOR UPDATE;

-- Outras transações ficam aguardando
UPDATE conta SET saldo = saldo - 100 WHERE id = 1;

COMMIT; -- Libera o lock
```

---

## ⚠️ Deadlock e Detecção

### O que é Deadlock?

Ocorre quando **duas ou mais transações esperam umas pelas outras** para liberar recursos, criando um **ciclo de dependências**.

### Exemplo Clássico de Deadlock

```
Transação A          Transação B
----------------     ----------------
Lock na Linha 1      Lock na Linha 2
Espera Linha 2  ←→   Espera Linha 1
(DEADLOCK!)
```

### Como o Oracle Lida com Deadlocks?

- **Detecta automaticamente** deadlocks
- **Aborta uma das transações** para quebrar o ciclo
- A transação abortada recebe um erro
- As demais transações continuam normalmente

### Boas Práticas para Minimizar Deadlocks

✅ **Acesse recursos sempre na mesma ordem**
```sql
-- Sempre acessar conta menor primeiro
UPDATE conta WHERE id = 1;
UPDATE conta WHERE id = 2;
```

✅ **Evite transações longas**
- Quanto mais tempo uma transação dura, maior a chance de deadlock

✅ **Use transações pequenas e rápidas**
- Minimize o tempo de retenção de locks

✅ **Evite interação com usuário dentro de transações**
- Não espere input do usuário com locks ativos

---

## 🎨 Controle Otimista de Concorrência

### Conceito

- **Assume que conflitos são raros**
- Não usa locks preventivos
- Verifica conflitos apenas no momento do COMMIT
- Ideal para ambientes com baixa concorrência

### Como Funciona?

1. Transação lê os dados
2. Transação processa localmente (sem locks)
3. Antes do COMMIT, verifica se houve mudanças
4. Se houve mudanças: **ROLLBACK**
5. Se não houve: **COMMIT**

### Implementação com Controle de Versão

```sql
-- Criando tabela com campo de versão
CREATE TABLE produto (
    id NUMBER PRIMARY KEY,
    produto VARCHAR2(50),
    valor NUMBER,
    versao TIMESTAMP
);

-- Ao atualizar, verificar a versão
UPDATE produto 
SET preco = 100, 
    versao = SYSTIMESTAMP
WHERE id = 17 
AND versao = :versao_antiga;

-- Se nenhuma linha foi atualizada, houve conflito!
```

### Controle Otimista vs Pessimista

| Aspecto | Otimista | Pessimista (Locks) |
|---------|----------|-------------------|
| **Quando usar** | Baixa concorrência | Alta concorrência |
| **Performance** | Melhor em leitura | Melhor em escrita |
| **Conflitos** | Detecta ao final | Previne com locks |
| **Complexidade** | Mais simples | Mais complexo |

---

## 📝 Exercícios Práticos

### Exercício 1: Transferência Bancária Segura

**Objetivo:** Criar uma transação para transferir valores entre contas com controle adequado.

```sql
-- Criando a tabela
CREATE TABLE conta (
    idConta NUMBER PRIMARY KEY,
    nomeCliente VARCHAR2(100),
    saldoConta NUMBER(10,2)
);

-- Inserindo dados de teste
INSERT INTO conta VALUES (1, 'João Silva', 1000.00);
INSERT INTO conta VALUES (2, 'Maria Santos', 500.00);
COMMIT;

-- Transação de transferência
BEGIN TRANSACTION;

DECLARE
    v_saldo_origem NUMBER;
    v_valor_transferencia NUMBER := 200.00;
BEGIN
    -- Bloqueia e verifica saldo da conta origem
    SELECT saldoConta INTO v_saldo_origem
    FROM conta
    WHERE idConta = 1
    FOR UPDATE;
    
    -- Verifica se há saldo suficiente
    IF v_saldo_origem >= v_valor_transferencia THEN
        -- Debita da conta origem
        UPDATE conta 
        SET saldoConta = saldoConta - v_valor_transferencia
        WHERE idConta = 1;
        
        -- Credita na conta destino
        UPDATE conta 
        SET saldoConta = saldoConta + v_valor_transferencia
        WHERE idConta = 2;
        
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Transferência realizada com sucesso!');
    ELSE
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Saldo insuficiente!');
    END IF;
END;
/
```

### Exercício 2: Simulando Deadlock

```sql
-- Sessão 1
BEGIN TRANSACTION;
UPDATE conta SET saldoConta = saldoConta - 100 WHERE idConta = 1;
-- Aguarda 10 segundos
UPDATE conta SET saldoConta = saldoConta + 100 WHERE idConta = 2;
COMMIT;

-- Sessão 2 (executar simultaneamente)
BEGIN TRANSACTION;
UPDATE conta SET saldoConta = saldoConta - 50 WHERE idConta = 2;
-- Aguarda 10 segundos
UPDATE conta SET saldoConta = saldoConta + 50 WHERE idConta = 1;
COMMIT;

-- Uma das transações será abortada automaticamente!
```

### Exercício 3: Controle Otimista

```sql
-- Criando tabela com controle de versão
CREATE TABLE estoque (
    id_produto NUMBER PRIMARY KEY,
    nome VARCHAR2(100),
    quantidade NUMBER,
    versao NUMBER DEFAULT 1
);

-- Inserindo produto
INSERT INTO estoque VALUES (1, 'Notebook', 10, 1);
COMMIT;

-- Simulando atualização otimista
DECLARE
    v_versao_atual NUMBER;
    v_linhas_afetadas NUMBER;
BEGIN
    -- Lê a versão atual
    SELECT versao INTO v_versao_atual
    FROM estoque
    WHERE id_produto = 1;
    
    -- Tenta atualizar verificando a versão
    UPDATE estoque
    SET quantidade = quantidade - 1,
        versao = versao + 1
    WHERE id_produto = 1
    AND versao = v_versao_atual;
    
    v_linhas_afetadas := SQL%ROWCOUNT;
    
    IF v_linhas_afetadas = 0 THEN
        DBMS_OUTPUT.PUT_LINE('Conflito detectado! Outro usuário alterou o registro.');
        ROLLBACK;
    ELSE
        DBMS_OUTPUT.PUT_LINE('Atualização realizada com sucesso!');
        COMMIT;
    END IF;
END;
/
```

---

## 🎓 Resumo para Prova

### Conceitos-Chave

1. **Controle de Concorrência** = Gerenciar acesso simultâneo a dados
2. **ACID** = Atomicidade, Consistência, Isolamento, Durabilidade
3. **Comandos**: BEGIN TRANSACTION, COMMIT, ROLLBACK

### Níveis de Isolamento (do menor ao maior)

1. READ UNCOMMITTED (permite dirty reads)
2. READ COMMITTED (padrão Oracle)
3. REPEATABLE READ (mesma leitura = mesmo resultado)
4. SERIALIZABLE (execução sequencial)

### Tipos de Lock

- **Row-level**: Bloqueia linha específica
- **Table-level**: Bloqueia tabela inteira
- **Exclusive**: Impede leitura e escrita
- **Shared**: Permite leitura, impede escrita

### Deadlock

- Ciclo de dependências entre transações
- Oracle detecta e aborta uma transação automaticamente
- **Prevenção**: acessar recursos na mesma ordem, transações curtas

### Controle Otimista

- Não usa locks preventivos
- Verifica conflitos apenas no COMMIT
- Usa campo de versão (timestamp ou version_number)
- Ideal para baixa concorrência

---

## 📚 Dicas de Estudo

✅ Entenda a diferença entre locks pessimistas e controle otimista  
✅ Saiba identificar quando ocorre deadlock  
✅ Memorize as propriedades ACID e suas definições  
✅ Pratique escrever transações com BEGIN, COMMIT e ROLLBACK  
✅ Compreenda quando usar cada nível de isolamento  
✅ Saiba usar FOR UPDATE para bloquear linhas  

---

**Disciplina:** Laboratório de Banco de Dados Avançado  
**Professor:** Allan (allan@cruzeirodosul.edu.br)