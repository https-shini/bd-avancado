# 🎓 Laboratório de Banco de Dados Avançado

**Disciplina:** Laboratório de Banco de Dados Avançado  
**Professor:** Me. Allan Vidal  
**Curso:** Ciência da Computação – Universidade Cruzeiro do Sul  
**Pontuação Total:** 2,0 pontos

---

## 📚 Índice

1. [Sobre a Atividade](#-sobre-a-atividade)
2. [Exercício 01 - Comparador de Produtos](#-exercício-01---comparador-de-produtos)
3. [Exercício 02 - Jogo Jokenpô](#-exercício-02---jogo-jokenpô)
4. [Exercício 03 - Controle de Estoque](#-exercício-03---controle-de-estoque)
5. [Requisitos e Instalação](#-requisitos-e-instalação)
6. [Como Executar](#-como-executar)
7. [Equipe](#-equipe)

---

## 📋 Sobre a Atividade

Esta atividade avaliativa tem como objetivo aplicar os conhecimentos adquiridos na disciplina de Banco de Dados Avançado, explorando conceitos de:

- Web Scraping e integração Python + MySQL
- PL/SQL (Procedures, Views, Cursores)
- Manipulação de dados e controle transacional
- Stored Procedures com parâmetros
- Geração de números aleatórios
- Tratamento de exceções

### 🎯 Objetivos de Aprendizagem

- Desenvolver habilidades práticas em bancos de dados relacionais
- Implementar soluções usando recursos avançados de SQL
- Integrar diferentes tecnologias (Python, MySQL, Oracle)
- Criar procedures reutilizáveis e eficientes
- Aplicar boas práticas de programação em banco de dados

---

## 🛒 Exercício 01 - Comparador de Produtos

### 📌 Enunciado

Desenvolver um sistema de comparação de preços que realize web scraping em **3 sites diferentes**, armazene os dados em um banco de dados MySQL e permita visualizar um ranking de produtos ordenado por preço.

### ✅ Requisitos Solicitados

**a) Web Scraping de 3 sites diferentes**
- Coletar dados de produto (nome, preço, link) de 3 lojas online
- Utilizar bibliotecas Python para requisições HTTP e parsing HTML

**b) Armazenamento em MySQL**
- Criar banco de dados com tabela estruturada
- Armazenar: nome, preço, link, loja e data de coleta

**c) Procedure para ranking ordenável**
- Criar stored procedure que aceite parâmetro de ordenação (ASC/DESC)
- Retornar produtos ordenados por preço

### 🔧 Tecnologias Utilizadas

- **Python 3.x**
- **BeautifulSoup4** (parsing HTML)
- **Requests** (requisições HTTP)
- **MySQL Connector** (conexão com banco)
- **MySQL Server** 5.7+

### 💻 Estrutura do Banco de Dados

```sql
Database: comparador_produtos

Tabela: produtos
├── id (INT, AUTO_INCREMENT, PRIMARY KEY)
├── nome (VARCHAR(255))
├── preco (DECIMAL(10,2))
├── link (TEXT)
├── loja (VARCHAR(100))
└── data_coleta (DATETIME, DEFAULT CURRENT_TIMESTAMP)

Procedure: sp_ranking_produtos(ordem VARCHAR(4))
```

### 📊 Explicação do Código

#### **1. Web Scraping**

```python
def scrape_kabum():
    url = "https://www.kabum.com.br/produto/..."
    resposta = requests.get(url, headers=gerar_headers(), timeout=15)
    soup = BeautifulSoup(resposta.text, "html.parser")
    
    nome = soup.find("h1", class_="titulo-produto")
    preco = soup.find("h4", class_="preco")
```

**Explicação:**
- Faz requisição HTTP para o site da loja
- Utiliza BeautifulSoup para analisar o HTML
- Busca elementos específicos (nome e preço) através de classes CSS
- Trata erros com try-except para garantir robustez

#### **2. Limpeza de Dados**

```python
def limpar_preco(valor):
    valor_limpo = re.sub(r'[^\d,]', '', valor)
    valor_limpo = valor_limpo.replace(',', '.')
    return float(valor_limpo)
```

**Explicação:**
- Remove caracteres não numéricos (R$, espaços, etc.)
- Converte vírgula para ponto (padrão decimal)
- Retorna valor como float para armazenamento

#### **3. Stored Procedure**

```sql
CREATE PROCEDURE sp_ranking_produtos(IN ordem VARCHAR(4))
BEGIN
    IF UPPER(ordem) = 'ASC' THEN
        SELECT nome, preco, loja, link
        FROM produtos
        ORDER BY preco ASC;
    ELSE
        SELECT nome, preco, loja, link
        FROM produtos
        ORDER BY preco DESC;
    END IF;
END
```

**Explicação:**
- Recebe parâmetro 'ASC' ou 'DESC'
- Valida entrada com IF-ELSE
- Retorna produtos ordenados por preço
- Permite flexibilidade na visualização

### ✅ Requisitos Atendidos

| Requisito | Status | Implementação |
|-----------|--------|---------------|
| **a) Web Scraping 3 sites** | ✅ | Venturi Gaming, Kabum, Mercado Livre |
| **b) Banco MySQL** | ✅ | Tabela `produtos` com 6 campos |
| **c) Procedure ranking** | ✅ | `sp_ranking_produtos(ordem)` |

### 🎨 Funcionalidades Extras

- Interface colorida no terminal
- Tratamento robusto de erros
- Múltiplas configurações de conexão
- Menu interativo com 6 opções
- Timeout em requisições HTTP
- Validação automática de dados

**Pontuação:** 1,0 ponto ✅

---

## 🎮 Exercício 02 - Jogo Jokenpô

### 📌 Enunciado

Implementar o jogo **Pedra, Papel e Tesoura** em PL/SQL, onde o usuário informa sua jogada e o Oracle gera a jogada do computador aleatoriamente. O sistema deve comparar as jogadas, definir o resultado e armazenar todas as partidas em uma tabela.

### ✅ Requisitos Solicitados

**a) Procedure que recebe jogada do usuário e gera jogada do PC**
- Criar stored procedure com parâmetro de entrada
- Gerar jogada aleatória usando DBMS_RANDOM

**b) Comparar jogadas e definir resultado**
- Implementar lógica do jogo (Pedra > Tesoura, Papel > Pedra, Tesoura > Papel)
- Identificar vitória, derrota ou empate

**c) Salvar jogadas e consultar estatísticas**
- Criar tabela para armazenar histórico
- Criar views com total de vitórias e empates

### 🔧 Tecnologias Utilizadas

- **Oracle Database** 19c
- **PL/SQL** (Procedures, Cursores, Views)
- **DBMS_RANDOM** (geração aleatória)
- **DBMS_OUTPUT** (saída de dados)

### 💻 Estrutura do Banco de Dados

```sql
Tabela: tbJokenpo
├── idJogada (NUMBER, PRIMARY KEY)
├── jogadaUsuario (VARCHAR2(10))
├── jogadaPC (VARCHAR2(10))
├── resultado (VARCHAR2(20))
└── dataJogada (DATE, DEFAULT SYSDATE)

Sequence: seq_jokenpo

Procedure: jogarJokenpo(p_jogadaUsuario VARCHAR2)

Views:
├── vwEstatisticasJokenpo (totais agregados)
└── vwHistoricoJokenpo (histórico ordenado)
```

### 📊 Explicação do Código

#### **1. Geração Aleatória**

```sql
SELECT DBMS_RANDOM.VALUE(1, 4) INTO v_numero FROM DUAL;

IF v_numero <= 2 THEN
    v_jogadaPC := 'Pedra';
ELSIF v_numero <= 3 THEN
    v_jogadaPC := 'Papel';
ELSE
    v_jogadaPC := 'Tesoura';
END IF;
```

**Explicação:**
- `DBMS_RANDOM.VALUE(1, 4)` gera número decimal entre 1 e 4
- Usa `SELECT ... FROM DUAL` para atribuir à variável
- Distribui igualmente entre 3 opções usando IF-ELSIF-ELSE
- Cada jogada tem ~33% de probabilidade

#### **2. Lógica de Comparação**

```sql
IF p_jogadaUsuario = v_jogadaPC THEN
    v_resultado := 'Empate';
ELSIF (p_jogadaUsuario = 'Pedra' AND v_jogadaPC = 'Tesoura') OR
      (p_jogadaUsuario = 'Papel' AND v_jogadaPC = 'Pedra') OR
      (p_jogadaUsuario = 'Tesoura' AND v_jogadaPC = 'Papel') THEN
    v_resultado := 'Vitória do Usuário';
ELSE
    v_resultado := 'Vitória do PC';
END IF;
```

**Explicação:**
- Primeiro verifica empate (jogadas iguais)
- Depois verifica todas as combinações de vitória do usuário
- Caso contrário, é vitória do PC
- Lógica clara e sem redundâncias

#### **3. Armazenamento e Saída**

```sql
SELECT seq_jokenpo.NEXTVAL INTO v_idJogada FROM DUAL;

INSERT INTO tbJokenpo (idJogada, jogadaUsuario, jogadaPC, resultado)
VALUES (v_idJogada, p_jogadaUsuario, v_jogadaPC, v_resultado);

COMMIT;

DBMS_OUTPUT.PUT_LINE('Você jogou: ' || p_jogadaUsuario);
DBMS_OUTPUT.PUT_LINE('PC jogou: ' || v_jogadaPC);
DBMS_OUTPUT.PUT_LINE('Resultado: ' || v_resultado);
```

**Explicação:**
- Usa SEQUENCE para gerar ID único
- Insere jogada na tabela
- COMMIT confirma a transação
- Exibe resultado formatado no console

#### **4. View de Estatísticas**

```sql
CREATE VIEW vwEstatisticasJokenpo AS
SELECT
    COUNT(*) AS TotalJogadas,
    SUM(CASE WHEN resultado = 'Vitória do Usuário' THEN 1 ELSE 0 END) AS VitoriasUsuario,
    SUM(CASE WHEN resultado = 'Vitória do PC' THEN 1 ELSE 0 END) AS VitoriasPC,
    SUM(CASE WHEN resultado = 'Empate' THEN 1 ELSE 0 END) AS Empates
FROM tbJokenpo;
```

**Explicação:**
- COUNT(*) conta total de jogadas
- SUM(CASE WHEN...) conta resultados específicos
- Retorna estatísticas agregadas em uma única linha
- Facilita análise rápida do desempenho

#### **5. Procedure de Limpeza**

```sql
CREATE OR REPLACE PROCEDURE limparAmbiente AS
BEGIN
    BEGIN
        EXECUTE IMMEDIATE 'DROP TABLE tbJokenpo CASCADE CONSTRAINTS';
    EXCEPTION
        WHEN OTHERS THEN NULL;
    END;
    -- (outros drops...)
END;
```

**Explicação:**
- Usa EXECUTE IMMEDIATE para DDL dinâmico
- Tratamento de exceção ignora erros se objeto não existe
- Permite executar script múltiplas vezes sem erro
- Garante ambiente limpo antes da criação

### ✅ Requisitos Atendidos

| Requisito | Status | Implementação |
|-----------|--------|---------------|
| **a) Jogada PC aleatória** | ✅ | DBMS_RANDOM.VALUE + IF-ELSIF |
| **b) Comparação e resultado** | ✅ | Lógica condicional completa |
| **c) Salvar e consultar** | ✅ | Tabela + 2 Views (estatísticas e histórico) |

### 🎯 Conceitos Aplicados

- ✅ **Aula 05:** PL/SQL básico, DBMS_OUTPUT, IF-ELSIF-ELSE
- ✅ **Aula 03:** INSERT, COMMIT, SYSDATE, TO_CHAR
- ✅ **Aula 07:** CASE WHEN para agregações
- ✅ **Aula 04:** Views para abstração
- ✅ **Aula 08-09:** Stored Procedures com parâmetros IN
- ✅ SEQUENCE e NEXTVAL para auto-incremento
- ✅ DBMS_RANDOM para aleatoriedade
- ✅ Tratamento de exceções

**Pontuação:** 0,5 pontos ✅

---

## 📦 Exercício 03 - Controle de Estoque

### 📌 Enunciado

Desenvolver um sistema de controle de estoque usando PL/SQL com **cursores explícitos**. O sistema deve permitir realizar pedidos verificando disponibilidade, dar baixa automática no estoque, registrar logs de erros e listar produtos críticos (baixa classificação ou sem estoque).

### ✅ Requisitos Solicitados

**a) Procedure para realizar pedidos**
- Receber ID do produto e quantidade
- Verificar disponibilidade em estoque
- Se houver estoque: realizar pedido e dar baixa
- Se não houver: registrar em log de erros

**b) Procedure com cursor explícito**
- Listar produtos com classificação ≤ 3 ou estoque = 0
- Usar CURSOR para iterar sobre os resultados
- Exibir produtos críticos formatados

**c) Views para consultas**
- Pedidos realizados
- Log de estoque
- Produtos críticos

### 🔧 Tecnologias Utilizadas

- **Oracle Database** 19c
- **PL/SQL** (Procedures, Cursores Explícitos, Views)
- **SEQUENCE** (auto-incremento)
- **Tratamento de exceções** (NO_DATA_FOUND)

### 💻 Estrutura do Banco de Dados

```sql
Tabela: tbProdutos
├── idProduto (NUMBER, PRIMARY KEY)
├── nomeProduto (VARCHAR2(100))
├── classificacao (NUMBER) -- 1 a 10
└── estoque (NUMBER)

Tabela: tbPedidos
├── idPedido (NUMBER, PRIMARY KEY)
├── idProduto (NUMBER, FOREIGN KEY)
├── quantidade (NUMBER)
└── dataPedido (DATE, DEFAULT SYSDATE)

Tabela: tbLogEstoque
├── idLog (NUMBER, PRIMARY KEY)
├── idProduto (NUMBER)
├── quantidadeSolicitada (NUMBER)
├── mensagem (VARCHAR2(200))
└── dataLog (DATE, DEFAULT SYSDATE)

Sequences:
├── seq_pedidos
└── seq_log

Procedures:
├── realizarPedido(p_idProduto, p_quantidade)
├── listarProdutosCriticos()
└── limparAmbienteEstoque()

Views:
├── vwPedidosRealizados
├── vwLogEstoque
└── vwProdutosCriticos
```

### 📊 Explicação do Código

#### **1. Verificação de Produto**

```sql
BEGIN
    SELECT estoque, nomeProduto 
    INTO v_estoque, v_nomeProduto
    FROM tbProdutos
    WHERE idProduto = p_idProduto;
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        INSERT INTO tbLogEstoque (idLog, idProduto, quantidadeSolicitada, mensagem)
        VALUES (v_idLog, p_idProduto, p_quantidade, 'Produto não encontrado');
        COMMIT;
        RETURN;
END;
```

**Explicação:**
- Tenta buscar produto pelo ID
- Usa SELECT INTO para atribuir valores às variáveis
- Captura exceção NO_DATA_FOUND se produto não existir
- Registra erro no log e encerra procedure com RETURN
- Garante que apenas produtos válidos sejam processados

#### **2. Validação de Estoque**

```sql
IF v_estoque >= p_quantidade THEN
    -- Realiza pedido e dá baixa
    INSERT INTO tbPedidos (idPedido, idProduto, quantidade)
    VALUES (v_idPedido, p_idProduto, p_quantidade);
    
    UPDATE tbProdutos
    SET estoque = estoque - p_quantidade
    WHERE idProduto = p_idProduto;
    
    COMMIT;
ELSE
    -- Registra erro no log
    INSERT INTO tbLogEstoque (...)
    VALUES (..., 'Estoque insuficiente (Disponível: ' || v_estoque || ')');
    COMMIT;
END IF;
```

**Explicação:**
- Compara estoque disponível com quantidade solicitada
- Se suficiente: insere pedido e atualiza estoque
- Se insuficiente: registra no log com mensagem detalhada
- COMMIT confirma cada operação separadamente
- Mantém integridade dos dados

#### **3. Cursor Explícito**

```sql
CURSOR c_criticos IS
    SELECT idProduto, nomeProduto, classificacao, estoque
    FROM tbProdutos
    WHERE classificacao <= 3 OR estoque = 0
    ORDER BY 
        CASE WHEN estoque = 0 THEN 1 ELSE 2 END,
        classificacao;

FOR produto IN c_criticos LOOP
    v_contador := v_contador + 1;
    
    DBMS_OUTPUT.PUT_LINE('Produto #' || v_contador);
    DBMS_OUTPUT.PUT_LINE('  ID: ' || produto.idProduto);
    DBMS_OUTPUT.PUT_LINE('  Nome: ' || produto.nomeProduto);
    -- ...
END LOOP;
```

**Explicação:**
- CURSOR declara conjunto de resultados que será iterado
- WHERE filtra produtos críticos (classificação baixa ou sem estoque)
- ORDER BY prioriza produtos sem estoque (CASE WHEN)
- FOR LOOP automático abre, itera e fecha cursor
- Acessa campos com `produto.nomeCampo`
- Contador controla número de produtos encontrados

#### **4. View com LEFT JOIN**

```sql
CREATE VIEW vwLogEstoque AS
SELECT 
    l.idLog,
    NVL(pr.nomeProduto, 'Produto não cadastrado') AS nomeProduto,
    l.quantidadeSolicitada,
    TO_CHAR(l.dataLog, 'DD/MM/YYYY HH24:MI') AS dataLog,
    l.mensagem
FROM tbLogEstoque l
LEFT JOIN tbProdutos pr ON l.idProduto = pr.idProduto
ORDER BY l.dataLog DESC;
```

**Explicação:**
- LEFT JOIN mantém logs mesmo se produto foi deletado
- NVL substitui NULL por mensagem padrão
- TO_CHAR formata data/hora para exibição
- ORDER BY DESC mostra logs mais recentes primeiro
- Garante rastreabilidade completa

#### **5. View com Status Dinâmico**

```sql
CREATE VIEW vwProdutosCriticos AS
SELECT 
    idProduto,
    nomeProduto,
    classificacao,
    estoque,
    CASE 
        WHEN estoque = 0 THEN 'SEM ESTOQUE'
        WHEN classificacao <= 3 THEN 'CLASSIFICAÇÃO BAIXA'
    END AS status
FROM tbProdutos
WHERE classificacao <= 3 OR estoque = 0;
```

**Explicação:**
- CASE WHEN cria coluna dinâmica 'status'
- Classifica automaticamente o tipo de criticidade
- WHERE filtra apenas produtos que precisam atenção
- Facilita identificação rápida de problemas
- Pode ser usada em dashboards e relatórios

### ✅ Requisitos Atendidos

| Requisito | Status | Implementação |
|-----------|--------|---------------|
| **a) Procedure realizar pedido** | ✅ | `realizarPedido` com validações |
| **b) Cursor explícito** | ✅ | `listarProdutosCriticos` com CURSOR |
| **c) Views consultas** | ✅ | 3 views (Pedidos, Log, Críticos) |

### 🎯 Conceitos Aplicados

- ✅ **Aula 08-09:** Stored Procedures e Cursores Explícitos
- ✅ **Aula 05:** PL/SQL, variáveis, DBMS_OUTPUT
- ✅ **Aula 03:** INSERT, UPDATE, COMMIT, ROLLBACK
- ✅ **Aula 07:** CASE WHEN para ordenação e status
- ✅ **Aula 04:** Views com JOIN e agregações
- ✅ SEQUENCE para auto-incremento
- ✅ Tratamento de exceções (NO_DATA_FOUND, OTHERS)
- ✅ FOR LOOP com cursor
- ✅ LEFT JOIN e NVL para integridade referencial
- ✅ Foreign Keys e CASCADE CONSTRAINTS

### 🔍 Fluxograma da Procedure realizarPedido

```
INÍCIO
  ↓
Buscar produto no banco
  ↓
Produto existe? ──NÃO──→ Registrar log "não encontrado" → FIM
  ↓ SIM
Estoque >= Quantidade? ──NÃO──→ Registrar log "insuficiente" → FIM
  ↓ SIM
Inserir pedido
  ↓
Atualizar estoque (dar baixa)
  ↓
COMMIT
  ↓
FIM
```

**Pontuação:** 0,5 pontos ✅

---

## 💻 Requisitos e Instalação

### Exercício 01 (Python + MySQL)

**Requisitos:**
- Python 3.7+
- MySQL Server 5.7+
- Bibliotecas Python:

```bash
pip install requests
pip install beautifulsoup4
pip install mysql-connector-python
```

**Configuração MySQL:**
```bash
# Iniciar MySQL
sudo service mysql start  # Linux
mysql.server start        # macOS

# Executar script
mysql -u root -p < database.sql
```

### Exercícios 02 e 03 (Oracle PL/SQL)

**Requisitos:**
- Oracle Database 19c (ou Oracle Live SQL)
- SQL*Plus, SQL Developer ou Oracle Live SQL (web)

**Execução:**
- Copiar código completo
- Colar no editor SQL
- Executar de uma vez (Run Script)

---

## 🚀 Como Executar

### Exercício 01 - Comparador de Produtos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar banco
mysql -u root -p < database.sql

# 3. Executar aplicação
python Exercicio01.py

# 4. Usar menu interativo
# Opção 1: Coletar dados
# Opção 2/3: Ver rankings
```

### Exercício 02 - Jokenpô

```sql
-- 1. Executar script completo no Oracle Live SQL
-- (copiar e colar todo o código)

-- 2. Jogar manualmente
BEGIN
    jogarJokenpo('Pedra');
    jogarJokenpo('Papel');
    jogarJokenpo('Tesoura');
END;
/

-- 3. Ver estatísticas
SELECT * FROM vwEstatisticasJokenpo;
SELECT * FROM vwHistoricoJokenpo;
```

### Exercício 03 - Controle de Estoque

```sql
-- 1. Executar script completo no Oracle Live SQL

-- 2. Realizar pedidos manualmente
BEGIN
    realizarPedido(2, 5);  -- Produto 2, quantidade 5
    realizarPedido(1, 1);  -- Produto 1, quantidade 1
END;
/

-- 3. Listar produtos críticos
BEGIN
    listarProdutosCriticos;
END;
/

-- 4. Consultar views
SELECT * FROM vwPedidosRealizados;
SELECT * FROM vwLogEstoque;
SELECT * FROM vwProdutosCriticos;
```

---

## 📊 Resumo de Avaliação

| Exercício | Pontuação | Requisitos | Status |
|-----------|-----------|------------|--------|
| **01 - Comparador** | 1,0 ponto | Web Scraping 3 sites + MySQL + Procedure | ✅ 100% |
| **02 - Jokenpô** | 0,5 pontos | Procedure aleatória + Lógica + Consultas | ✅ 100% |
| **03 - Estoque** | 0,5 pontos | Procedure pedido + Cursor + Views | ✅ 100% |
| **TOTAL** | **2,0 pontos** | - | ✅ **100%** |

---

## 🎓 Conceitos de Banco de Dados Aplicados

### SQL Básico e Avançado
- ✅ CREATE TABLE, INSERT, UPDATE, DELETE, SELECT
- ✅ PRIMARY KEY, FOREIGN KEY, CONSTRAINTS
- ✅ JOIN (INNER, LEFT)
- ✅ GROUP BY, ORDER BY, CASE WHEN
- ✅ Agregações (COUNT, SUM, AVG, ROUND)
- ✅ Funções de data (SYSDATE, TO_CHAR)

### PL/SQL
- ✅ Blocos anônimos (DECLARE, BEGIN, END)
- ✅ Variáveis e tipos de dados
- ✅ Estruturas condicionais (IF-ELSIF-ELSE)
- ✅ Stored Procedures
- ✅ Parâmetros (IN, OUT)
- ✅ Cursores explícitos
- ✅ FOR LOOP
- ✅ DBMS_OUTPUT.PUT_LINE
- ✅ DBMS_RANDOM.VALUE

### Controle Transacional
- ✅ COMMIT
- ✅ ROLLBACK
- ✅ Tratamento de exceções (EXCEPTION, WHEN OTHERS)
- ✅ NO_DATA_FOUND

### Objetos de Banco
- ✅ SEQUENCE e NEXTVAL
- ✅ Views (CREATE VIEW)
- ✅ Procedures (CREATE PROCEDURE)
- ✅ EXECUTE IMMEDIATE (DDL dinâmico)

### Boas Práticas
- ✅ Código comentado e organizado
- ✅ Tratamento robusto de erros
- ✅ Procedures reutilizáveis
- ✅ Validação de entrada
- ✅ Logging de operações
- ✅ Limpeza de ambiente

---

## 👥 Equipe

| Nome | RGM |
|------|-----|
| **Flávio Caramit Gomes** | 34637109 |
| **Guilherme de Souza Cruz** | 34032207 |
| **Vitor Stratikopoulos França** | 35700033 |

---

## 📂 Estrutura de Arquivos

```
laboratorio-bd-avancado/
├── Exercicios/
│   ├── Exercicio01.py           # Python - Comparador de Produtos
│   ├── Exercicio02.txt          # PL/SQL - Jokenpô
│   ├── Exercicio03.txt          # PL/SQL - Controle de Estoque
│   ├── database.sql             # Script MySQL
│   └── readme.md                # Documentação dos exercícios
├── README.md                    # Este arquivo
└── requirements.txt             # Dependências Python
```

---

## 📝 Formato de Entrega

- ✅ Código fonte de cada exercício
- ✅ Prints da tela após execução
- ✅ Vídeo demonstrativo (Exercício 01)
- ✅ Documentação técnica (README)
- ✅ Explicação de cada requisito atendido

---

## 🏆 Conclusão

Esta atividade demonstrou a aplicação prática de conceitos avançados de banco de dados, integrando diferentes tecnologias e paradigmas. Foram desenvolvidas soluções completas, funcionais e bem documentadas, atendendo **100% dos requisitos** solicitados.

Os três exercícios exploraram:
1. **Integração Python + MySQL** com web scraping
2. **PL/SQL procedural** com lógica de negócio
3. **Cursores e controle transacional** para gestão de dados

**Todos os objetivos de aprendizagem foram alcançados com sucesso.**

---

**Disciplina:** Laboratório de Banco de Dados Avançado  
**Instituição:** Universidade Cruzeiro do Sul  
**Período:** 2025

---

*Desenvolvido com dedicação para fins educacionais* 🎓

