# 🎓 Laboratório de Banco de Dados Avançado

**Disciplina:** Laboratório de Banco de Dados Avançado  
**Pontuação:** Até 2 pontos  
**Integrantes:** Máximo 3 pessoas

---

## 📚 Índice

1. [Exercício 01 - Comparador de Produtos (Python + MySQL)](#exercício-01---comparador-de-produtos)
2. [Exercício 02 - Jogo Jokenpô (PL/SQL)](#exercício-02---jogo-jokenpô)
3. [Exercício 03 - Controle de Estoque (PL/SQL)](#exercício-03---controle-de-estoque)
4. [Requisitos e Instalação](#requisitos-e-instalação)
5. [Como Executar](#como-executar)

---

## 🛒 Exercício 01 - Comparador de Produtos
**Pontuação:** 1 ponto  
**Tecnologias:** Python 3.x, MySQL, BeautifulSoup4, Requests

### 📋 Descrição
Sistema de comparação de preços que realiza web scraping em 3 lojas online, armazena os dados em MySQL e exibe rankings ordenáveis de produtos.

### ✅ Requisitos Atendidos

#### **a) Web Scraping de 3 Sites**
Coleta automática de dados do processador **AMD Ryzen 7 5700X**:

| Loja | URL | Dados Coletados |
|------|-----|----------------|
| 🎮 **Venturi Gaming** | `venturigaming.com.br` | Nome, Preço, Link |
| 💻 **Kabum** | `kabum.com.br` | Nome, Preço, Link |
| 🛍️ **Mercado Livre** | `mercadolivre.com.br` | Nome, Preço, Link |

#### **b) Banco de Dados MySQL**
```sql
Database: comparador_produtos
Tabela: produtos
├── id (INT, AUTO_INCREMENT, PRIMARY KEY)
├── nome (VARCHAR(255))
├── preco (DECIMAL(10,2))
├── link (TEXT)
├── loja (VARCHAR(100))
└── data_coleta (DATETIME, DEFAULT CURRENT_TIMESTAMP)
```

#### **c) Procedure para Ranking**
```sql
PROCEDURE sp_ranking_produtos(ordem VARCHAR(4))
```
- **Parâmetro:** `ASC` (menor→maior) ou `DESC` (maior→menor)
- **Retorna:** Produtos ordenados por preço

### 🎨 Funcionalidades

#### Menu Interativo
```
1 - 🌐 Coletar dados das lojas (Web Scraping)
2 - 📊 Ranking ASC (Menor → Maior Preço)
3 - 📊 Ranking DESC (Maior → Menor Preço)
4 - 📋 Exibir informações do sistema
5 - 🔧 Testar conexão com MySQL
0 - 🚪 Sair do programa
```

#### Características
- ✅ Interface colorida no terminal
- ✅ Tratamento robusto de erros
- ✅ Múltiplas configurações de conexão MySQL
- ✅ Timeout em requisições HTTP
- ✅ Validação automática de dados
- ✅ Limpeza e conversão de valores monetários

### 📁 Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Aplicação Python completa |
| `database.sql` | Script de criação do banco |

### 🚀 Como Executar

```bash
# 1. Instalar dependências
pip install requests beautifulsoup4 mysql-connector-python

# 2. Configurar MySQL
mysql -u root -p < database.sql

# 3. Executar aplicação
python main.py
```

### 📸 Exemplo de Saída
```
======================================================================
            🛒 COMPARADOR DE PRODUTOS - WEB SCRAPING
======================================================================

🔍 Coletando dados de Venturi Gaming...
🔍 Coletando dados de Kabum...
🔍 Coletando dados de Mercado Livre...

======================================================================
                        📦 PRODUTOS COLETADOS
======================================================================

✅ Venturi Gaming
   📦 Produto: Processador AMD Ryzen 7 5700X...
   💰 Preço: R$ 899,90
   🔗 Link: http://www.venturigaming.com.br/produtos/...

✅ Kabum
   📦 Produto: AMD Ryzen 7 5700X 8-Núcleos 16-Threads...
   💰 Preço: R$ 949,99
   🔗 Link: https://www.kabum.com.br/produto/729769/...
```

---

## 🎮 Exercício 02 - Jogo Jokenpô
**Pontuação:** 0,5 pontos  
**Tecnologia:** PL/SQL (Oracle Database)

### 📋 Descrição
Implementação do jogo Pedra, Papel e Tesoura com armazenamento de jogadas e estatísticas em Oracle Database.

### ✅ Requisitos Atendidos

#### **a) Sistema de Jogadas**
- Usuário informa sua jogada (Pedra/Papel/Tesoura)
- Oracle gera jogada aleatória do PC usando `DBMS_RANDOM`

#### **b) Comparação e Resultado**
Lógica de vitória:
- **Pedra** vence **Tesoura**
- **Papel** vence **Pedra**
- **Tesoura** vence **Papel**
- Jogadas iguais = **Empate**

#### **c) Armazenamento e Consultas**
Tabela `tbJokenpo` armazena todas as jogadas com:
- ID da jogada (auto-incremento)
- Jogada do usuário
- Jogada do PC
- Resultado (Vitória Usuário/PC/Empate)
- Data/hora da jogada

### 🗄️ Estrutura do Banco

```sql
CREATE TABLE tbJokenpo (
    idJogada NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    jogadaUsuario VARCHAR2(10) NOT NULL,
    jogadaPC VARCHAR2(10) NOT NULL,
    resultado VARCHAR2(20) NOT NULL,
    dataJogada DATE DEFAULT SYSDATE
);
```

### 🔧 Procedures e Views

#### **Procedure Principal**
```sql
PROCEDURE jogarJokenpo(p_jogadaUsuario IN VARCHAR2)
```
- Gera jogada aleatória do PC
- Compara jogadas
- Salva resultado no banco
- Exibe resultado no terminal

#### **Views Criadas**

1. **vwEstatisticasJokenpo** - Estatísticas gerais
```sql
SELECT * FROM vwEstatisticasJokenpo;
-- Retorna: Total de Jogadas, Vitórias Usuário, Vitórias PC, Empates
```

2. **vwHistoricoJokenpo** - Histórico completo
```sql
SELECT * FROM vwHistoricoJokenpo;
-- Retorna: ID, Jogadas, Resultado, Data/Hora
```

### 🎯 Exemplo de Uso

```sql
-- Ativar saída no console
SET SERVEROUTPUT ON;

-- Jogar várias rodadas
BEGIN
    jogarJokenpo('Pedra');
    jogarJokenpo('Papel');
    jogarJokenpo('Tesoura');
    jogarJokenpo('Pedra');
    jogarJokenpo('Papel');
END;
/

-- Visualizar estatísticas
SELECT * FROM vwEstatisticasJokenpo;
```

### 📊 Exemplo de Saída
```
Você jogou: Pedra
PC jogou: Tesoura
Resultado: Vitória do Usuário
------------------------
Você jogou: Papel
PC jogou: Papel
Resultado: Empate
------------------------
```

### 📈 Consultas Adicionais

**Percentual de vitórias:**
```sql
SELECT 
    resultado,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tbJokenpo), 2) AS percentual
FROM tbJokenpo
GROUP BY resultado
ORDER BY total DESC;
```

---

## 📦 Exercício 03 - Controle de Estoque
**Pontuação:** 0,5 pontos  
**Tecnologia:** PL/SQL (Oracle Database)

### 📋 Descrição
Sistema completo de controle de estoque com procedures, cursors e logs para gerenciamento de produtos e pedidos.

### ✅ Requisitos Atendidos

#### **a) Procedure de Pedidos**
Recebe ID do produto e quantidade:
- ✅ Verifica disponibilidade em estoque
- ✅ Realiza pedido se houver estoque
- ✅ Dá baixa automática no estoque
- ✅ Registra em log se não houver estoque

#### **b) Procedure com Cursor**
Exibe produtos críticos:
- ✅ Classificação baixa (≤ 3)
- ✅ Sem estoque (= 0)
- ✅ Ordenação por prioridade

### 🗄️ Estrutura do Banco

```sql
-- Tabela de Produtos
CREATE TABLE tbProdutos (
    idProduto NUMBER PRIMARY KEY,
    nomeProduto VARCHAR2(100) NOT NULL,
    classificacao NUMBER NOT NULL,  -- 1 a 10
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

### 🔧 Procedures

#### **1. realizarPedido** - Processar Pedidos
```sql
PROCEDURE realizarPedido(
    p_idProduto IN NUMBER,
    p_quantidade IN NUMBER
)
```

**Fluxo de execução:**
1. Verifica se produto existe
2. Consulta estoque disponível
3. Se **estoque suficiente**:
   - Insere pedido em `tbPedidos`
   - Atualiza estoque em `tbProdutos`
   - Exibe confirmação
4. Se **estoque insuficiente**:
   - Registra em `tbLogEstoque`
   - Exibe mensagem de erro

#### **2. listarProdutosCriticos** - Produtos com Problemas
```sql
PROCEDURE listarProdutosCriticos
```

**Usa CURSOR para selecionar:**
- Produtos com classificação ≤ 3
- Produtos com estoque = 0
- Ordenados por prioridade (sem estoque primeiro)

### 📊 Views Criadas

#### **1. vwPedidosRealizados**
```sql
SELECT * FROM vwPedidosRealizados;
```
Exibe: ID Pedido, Produto, Quantidade, Data

#### **2. vwLogEstoque**
```sql
SELECT * FROM vwLogEstoque;
```
Exibe: ID Log, Produto, Quantidade Solicitada, Mensagem, Data

#### **3. vwProdutosCriticos**
```sql
SELECT * FROM vwProdutosCriticos;
```
Exibe: ID, Produto, Classificação, Estoque, Status

### 🎯 Exemplo de Uso

```sql
-- Inserir produtos de teste
INSERT INTO tbProdutos VALUES (1, 'Mouse Gamer', 2, 0);
INSERT INTO tbProdutos VALUES (2, 'Teclado Mecânico', 9, 10);
INSERT INTO tbProdutos VALUES (3, 'Monitor 24"', 3, 5);
COMMIT;

-- Ativar saída
SET SERVEROUTPUT ON;

-- Realizar pedidos
BEGIN
    realizarPedido(2, 3);   -- Sucesso: tem estoque
    realizarPedido(1, 1);   -- Falha: sem estoque
    realizarPedido(99, 1);  -- Falha: produto não existe
END;
/

-- Listar produtos críticos
BEGIN
    listarProdutosCriticos;
END;
/

-- Consultar resultados
SELECT * FROM vwPedidosRealizados;
SELECT * FROM vwLogEstoque;
SELECT * FROM vwProdutosCriticos;
```

### 📸 Exemplo de Saída

```
✔ Pedido realizado: Teclado Mecânico (Qtd: 3)
✗ Estoque insuficiente: Mouse Gamer (Solicitado: 1, Disponível: 0)
✗ Erro: Produto 99 não existe

========================================
     PRODUTOS CRÍTICOS
========================================

Produto #1
  ID: 1
  Nome: Mouse Gamer
  Classificação: 2/10
  Estoque: 0
  Status: ⚠️ SEM ESTOQUE
----------------------------------------

Produto #2
  ID: 3
  Nome: Monitor 24"
  Classificação: 3/10
  Estoque: 5
  Status: ⚠️ CLASSIFICAÇÃO BAIXA
----------------------------------------

Total de produtos críticos: 2
========================================
```

---

## 💻 Requisitos e Instalação

### Exercício 01 (Python)

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
# ou
mysql.server start        # macOS
# ou iniciar XAMPP/WAMP  # Windows

# Executar script
mysql -u root -p < database.sql
```

### Exercícios 02 e 03 (Oracle)

**Requisitos:**
- Oracle Database 11g+
- SQL*Plus ou SQL Developer
- Oracle Client instalado

**Configuração Oracle:**
```bash
# Conectar ao Oracle
sqlplus usuario/senha@banco

# Executar scripts
@Exercicio02.txt
@Exercicio03.txt
```

---

## 🚀 Como Executar

### Exercício 01 - Comparador de Produtos

```bash
# 1. Clonar/baixar arquivos
git clone <repositorio>
cd laboratorio-bd-avancado

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar banco
mysql -u root -p < database.sql

# 4. Executar
python main.py
```

**Fluxo recomendado:**
1. Execute opção **5** para testar conexão MySQL
2. Execute opção **1** para coletar dados
3. Execute opção **2** ou **3** para ver rankings

### Exercício 02 - Jokenpô

```sql
-- 1. Conectar ao Oracle
sqlplus usuario/senha@banco

-- 2. Executar script completo
@Exercicio02.txt

-- 3. Ou executar manualmente:
-- Criar tabela
CREATE TABLE tbJokenpo (...);

-- Criar procedure
CREATE OR REPLACE PROCEDURE jogarJokenpo (...);

-- Jogar
SET SERVEROUTPUT ON;
BEGIN
    jogarJokenpo('Pedra');
END;
/

-- Ver resultados
SELECT * FROM vwEstatisticasJokenpo;
```

### Exercício 03 - Controle de Estoque

```sql
-- 1. Conectar ao Oracle
sqlplus usuario/senha@banco

-- 2. Executar script completo
@Exercicio03.txt

-- 3. Ou executar etapas:
-- Criar tabelas
CREATE TABLE tbProdutos (...);
CREATE TABLE tbPedidos (...);
CREATE TABLE tbLogEstoque (...);

-- Criar procedures
CREATE OR REPLACE PROCEDURE realizarPedido (...);
CREATE OR REPLACE PROCEDURE listarProdutosCriticos (...);

-- Inserir dados de teste
INSERT INTO tbProdutos VALUES (1, 'Mouse Gamer', 2, 0);
INSERT INTO tbProdutos VALUES (2, 'Teclado Mecânico', 9, 10);
COMMIT;

-- Testar
SET SERVEROUTPUT ON;
BEGIN
    realizarPedido(2, 3);
END;
/
```

---

## 📂 Estrutura de Arquivos

```
laboratorio-bd-avancado/
├── main.py                 # Exercício 01 - Aplicação Python
├── database.sql            # Exercício 01 - Script MySQL
├── Exercicio02.txt         # Exercício 02 - Jokenpô PL/SQL
├── Exercicio03.txt         # Exercício 03 - Estoque PL/SQL
├── exercicios_lbda.pdf     # Documento com requisitos
└── README.md               # Este arquivo
```

---

## 🎓 Observações Importantes

### Exercício 01
- ⚠️ Seletores HTML podem mudar se sites atualizarem
- 💡 Configure corretamente usuário/senha do MySQL
- 🔄 Recomendado executar coleta periodicamente

### Exercício 02
- 🎲 Jogadas do PC são verdadeiramente aleatórias
- 📊 Estatísticas acumulam ao longo do tempo
- 🗑️ Use script de limpeza para resetar

### Exercício 03
- 🔒 Transações garantem integridade dos dados
- 📝 Todos os erros são registrados em log
- 🎯 Cursor otimiza busca de produtos críticos

---

## 🏆 Critérios de Avaliação

| Exercício | Pontuação | Status |
|-----------|-----------|--------|
| 01 - Comparador de Produtos | 1,0 ponto | ✅ Completo |
| 02 - Jogo Jokenpô | 0,5 pontos | ✅ Completo |
| 03 - Controle de Estoque | 0,5 pontos | ✅ Completo |
| **TOTAL** | **2,0 pontos** | ✅ **100%** |

---

## 📝 Formato de Entrega

- ✅ Código de cada exercício
- ✅ Prints da tela após execução
- ✅ Vídeo demonstrativo (Exercício 01)
- ✅ Documentação (este README)

---

## 👥 Equipe

| Nome | RGM |
|------|-----|
| **Flávio Caramit Gomes** | 34637109 |
| **Guilherme de Souza Cruz** | 34032207 |
| **Vitor Stratikopoulos França** | 35700033 |

---

## 📧 Contato

Para dúvidas ou sugestões, entre em contato com a equipe.

---

**Disciplina:** Laboratório de Banco de Dados Avançado  
**Instituição:** [Nome da instituição]  
**Período:** [Inserir período]

---

*Desenvolvido com ❤️ para fins educacionais*
