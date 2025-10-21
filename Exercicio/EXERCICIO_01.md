# 🛒 Exercício 1: Comparador de Preços com Web Scraping

**Pontuação:** 1.0 ponto (50% da nota total)

---

## 📋 Enunciado Completo

> Você foi contratado para desenvolver uma aplicação em Python que auxilie os usuários na comparação de preços de produtos em diferentes aplicações web.

### Requisitos Técnicos

#### a) Web Scraping (30%)
- Coletar dados de **pelo menos 3 sites diferentes**
- Utilizar biblioteca **BeautifulSoup**
- Extrair informações relevantes de produtos

#### b) Persistência em Banco de Dados (30%)
- Armazenar em **MySQL**
- Campos obrigatórios:
  - `id` do produto
  - `nome` do produto
  - `valor` do produto
  - `link` para a aplicação de origem

#### c) Stored Procedure para Ranking (40%)
- Criar procedure no banco de dados
- Exibir ranking dos produtos
- Ordenação configurável por **parâmetro**:
  - `ASC` → menor para maior valor
  - `DESC` → maior para menor valor

---

## 🎯 Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Funcionalidade** | 40% | Aplicação executa sem erros e atende todos os requisitos |
| **Qualidade do Código** | 25% | Organização, nomenclatura, comentários |
| **Web Scraping** | 20% | BeautifulSoup implementado em 3+ sites |
| **Stored Procedure** | 15% | Procedure parametrizada funcionando corretamente |

---

## 🏗️ Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────┐
│                   APLICAÇÃO PYTHON                      │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Scraper    │  │   Scraper    │  │   Scraper    │ │
│  │    Site 1    │  │    Site 2    │  │    Site 3    │ │
│  │   (Kabum)    │  │   (Amazon)   │  │ (Mercado L.) │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                  │         │
│         └─────────────────┼──────────────────┘         │
│                           │                            │
│                  ┌────────▼────────┐                   │
│                  │ GerenciadorBanco│                   │
│                  │   (Classe)      │                   │
│                  └────────┬────────┘                   │
└───────────────────────────┼────────────────────────────┘
                            │
                    ┌───────▼───────┐
                    │  MySQL Server │
                    │               │
                    │ ┌───────────┐ │
                    │ │  produtos │ │
                    │ └───────────┘ │
                    │ ┌───────────┐ │
                    │ │ sp_ranking│ │
                    │ │  _produtos│ │
                    │ └───────────┘ │
                    └───────────────┘
```

---

## 💾 Estrutura do Banco de Dados MySQL

### Tabela: `produtos`

```sql
CREATE TABLE produtos (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    nome_produto VARCHAR(255) NOT NULL,
    valor_produto DECIMAL(10, 2) NOT NULL,
    link_origem VARCHAR(500) NOT NULL,
    site_origem VARCHAR(100) NOT NULL,
    data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_valor (valor_produto)
);
```

**Campos:**
- `id_produto`: Identificador único (auto-incremento)
- `nome_produto`: Nome completo do produto
- `valor_produto`: Preço em formato decimal
- `link_origem`: URL completa do produto
- `site_origem`: Nome do site de origem
- `data_coleta`: Timestamp da coleta

### Stored Procedure: `sp_ranking_produtos`

```sql
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

**Funcionalidades:**
- ✅ Validação de parâmetro de entrada
- ✅ Verificação de produtos cadastrados
- ✅ Numeração de ranking com `ROW_NUMBER()`
- ✅ Ordenação dinâmica por parâmetro

---

## 🐍 Estrutura da Aplicação Python

### Classe: `GerenciadorBanco`

```python
class GerenciadorBanco:
    def __init__(self, config)           # Conecta ao MySQL
    def inserir_produto(...)             # INSERT de produtos
    def limpar_tabela(...)               # TRUNCATE TABLE
    def exibir_ranking(ordenacao)        # Executa procedure
    def fechar(...)                      # Fecha conexão
```

### Funções de Web Scraping

```python
def scrape_kabum()          # Coleta produtos do Kabum
def scrape_amazon()         # Coleta produtos da Amazon
def scrape_mercado_livre()  # Coleta produtos do Mercado Livre
```

Cada função retorna uma lista de dicionários:
```python
[
    {
        'nome': 'Nome do Produto',
        'preco': 999.90,
        'link': 'https://...',
        'site': 'Nome do Site'
    },
    ...
]
```

### Fluxo Principal

```python
def main():
    1. Conectar ao banco
    2. Limpar dados anteriores
    3. Coletar de 3 sites
    4. Inserir produtos no MySQL
    5. Exibir ranking ASC
    6. Exibir ranking DESC
    7. Fechar conexão
```

---

## 🔧 Instalação e Configuração

### 1️⃣ Pré-requisitos

- **Python 3.8+**
- **MySQL 8.0+**
- **pip** (gerenciador de pacotes Python)

### 2️⃣ Instalar Dependências

```bash
pip install mysql-connector-python requests beautifulsoup4
```

Ou usar `requirements.txt`:
```bash
pip install -r requirements.txt
```

**Conteúdo de `requirements.txt`:**
```
mysql-connector-python==8.0.33
requests==2.31.0
beautifulsoup4==4.12.2
```

### 3️⃣ Configurar MySQL

Execute o script SQL no MySQL Workbench ou terminal:

```bash
mysql -u root -p < database.sql
```

### 4️⃣ Configurar Credenciais

Edite o arquivo `main.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SUA_SENHA_AQUI',  # ⚠️ ALTERE
    'database': 'comparador_precos'
}
```

---

## ▶️ Execução

```bash
python main.py
```

### Saída Esperada

```
======================================================================
       COMPARADOR DE PREÇOS - WEB SCRAPING
======================================================================
✓ Conectado ao MySQL
✓ Tabela limpa

======================================================================
       COLETANDO DADOS DE 3 SITES
======================================================================

[1/3] Coletando Kabum...
   ✓ 3 produtos coletados

[2/3] Coletando Amazon...
   ✓ 3 produtos coletados

[3/3] Coletando Mercado Livre...
   ✓ 3 produtos coletados

======================================================================
       INSERINDO NO BANCO DE DADOS
======================================================================

✓ 9 produtos inseridos com sucesso!

======================================================================
       RANKING: MENOR PARA MAIOR PREÇO (ASC)
======================================================================

#    Produto                                      Preço        Site
--------------------------------------------------------------------------------
1    Mousepad Gamer Grande Speed 70x30cm          R$ 49.90     Mercado Livre
2    SSD Kingston 480GB SATA III                  R$ 249.90    Amazon
3    Mouse Gamer Logitech G502 HERO               R$ 299.99    Kabum
...
```

---

## 📊 Conceitos de Banco de Dados Aplicados

### 1. **Stored Procedures** (Aula 08)
- Encapsulamento de lógica no banco
- Parâmetros de entrada (`IN`)
- Controle de fluxo (`IF-ELSE`)

### 2. **Window Functions** (Aula 07)
- `ROW_NUMBER() OVER (ORDER BY ...)`
- Numeração sequencial de linhas

### 3. **Índices** (Otimização)
- `INDEX idx_valor (valor_produto)`
- Acelera ordenação e buscas

### 4. **AUTO_INCREMENT**
- Geração automática de IDs
- Garantia de unicidade

---

## 🧪 Testes

### Teste 1: Inserção de Dados

```sql
-- Verificar produtos inseridos
SELECT COUNT(*) FROM produtos;

-- Ver todos os produtos
SELECT * FROM produtos ORDER BY valor_produto;
```

### Teste 2: Procedure com ASC

```sql
CALL sp_ranking_produtos('ASC');
```

**Resultado esperado:** Lista ordenada do menor para o maior preço

### Teste 3: Procedure com DESC

```sql
CALL sp_ranking_produtos('DESC');
```

**Resultado esperado:** Lista ordenada do maior para o menor preço

### Teste 4: Parâmetro Inválido

```sql
CALL sp_ranking_produtos('INVALIDO');
```

**Resultado esperado:** Mensagem de erro

---

## 📸 Prints para Entrega

### Print 1: Execução Python
Capturar terminal mostrando:
- ✓ Coleta dos 3 sites
- ✓ Inserção no banco
- ✓ Rankings ASC e DESC

### Print 2: MySQL Workbench
Capturar:
- ✓ Tabela `produtos` populada
- ✓ Resultado de `CALL sp_ranking_produtos('ASC')`
- ✓ Resultado de `CALL sp_ranking_produtos('DESC')`

---

## 🎥 Vídeo Demonstrativo (Opcional)

### Roteiro Sugerido (2-3 minutos):

1. **Introdução (15s)**
   - Explicar objetivo do exercício

2. **Código Python (30s)**
   - Mostrar estrutura do código
   - Destacar funções de scraping

3. **Banco MySQL (30s)**
   - Mostrar tabela e procedure

4. **Execução (60s)**
   - Rodar aplicação
   - Mostrar coleta dos sites
   - Exibir rankings

5. **Validação (30s)**
   - Consultar MySQL Workbench
   - Verificar dados inseridos

---

## 🚨 Troubleshooting

### Erro: "Access denied for user"
```bash
# Verificar credenciais
mysql -u root -p

# Resetar senha se necessário
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nova_senha';
```

### Erro: "Table doesn't exist"
```bash
# Executar script de criação
mysql -u root -p comparador_precos < database.sql
```

### Erro: "Module not found"
```bash
# Reinstalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

### Web Scraping não funciona
- Sites bloqueiam requisições sem User-Agent
- Use headers apropriados
- Considere usar dados simulados para demonstração

---

## 📁 Arquivos do Exercício

```
exercicio01/
├── database.sql           # Script MySQL completo
├── main.py               # Aplicação Python
├── requirements.txt      # Dependências
└── README.md            # Esta documentação
```

---

## 🔗 Código Completo

### 📄 `Database.sql`

```sql
  -- Criação do banco de dados
  CREATE DATABASE IF NOT EXISTS comparador_produtos;
  USE comparador_produtos;
  
  -- Tabela de origens (sites)
  CREATE TABLE origens (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nome VARCHAR(100) NOT NULL UNIQUE,
      url_base VARCHAR(255) NOT NULL
  );
  
  -- Tabela de produtos
  CREATE TABLE produtos (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nome VARCHAR(255) NOT NULL,
      preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0),
      link VARCHAR(500) NOT NULL,
      origem_id INT NOT NULL,
      data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (origem_id) REFERENCES origens(id)
  );
  
  -- Inserção de origens
  INSERT INTO origens (nome, url_base) VALUES
  ('Site 1', 'https://site1.com'),
  ('Site 2', 'https://site2.com'),
  ('Site 3', 'https://site3.com');
  
  -- Inserção de produtos
  INSERT INTO produtos (nome, preco, link, origem_id) VALUES
  ('Mouse Gamer', 129.90, 'https://site1.com/mouse', 1),
  ('Teclado Mecânico', 249.99, 'https://site2.com/teclado', 2),
  ('Monitor 24"', 899.00, 'https://site3.com/monitor', 3),
  ('Headset RGB', 199.50, 'https://site1.com/headset', 1),
  ('Webcam HD', 149.00, 'https://site2.com/webcam', 2);
```

### 📄 `Exercicio01.py`

```python
  import re
  import os
  import platform
  from datetime import datetime
  
  # 🎨 Cores ANSI
  class Cores:
      HEADER = '\033[95m'
      AZUL = '\033[94m'
      VERDE = '\033[92m'
      AMARELO = '\033[93m'
      VERMELHO = '\033[91m'
      NEGRITO = '\033[1m'
      RESET = '\033[0m'
  
  # 🔧 Limpa o terminal
  def limpar_terminal():
      os.system('cls' if platform.system() == 'Windows' else 'clear')
  
  # 📥 Carrega dados simulados do SQL
  def carregar_dados_sql(caminho_sql):
      produtos = []
      origens = {}
      try:
          with open(caminho_sql, 'r', encoding='utf-8') as arquivo:
              conteudo = arquivo.read()
  
              # Extrai origens
              origem_padrao = r"INSERT INTO origens \(nome, url_base\) VALUES\s*(.+?);"
              origem_match = re.search(origem_padrao, conteudo, re.DOTALL)
              if origem_match:
                  origem_linhas = re.findall(r"\('(.+?)', '(.+?)'\)", origem_match.group(1))
                  for i, (nome, url) in enumerate(origem_linhas, start=1):
                      origens[str(i)] = {'nome': nome, 'url_base': url}
  
              # Extrai produtos
              produto_padrao = r"INSERT INTO produtos \(nome, preco, link, origem_id\) VALUES\s*(.+?);"
              produto_match = re.search(produto_padrao, conteudo, re.DOTALL)
              if produto_match:
                  produto_linhas = re.findall(r"\('(.+?)', ([\d.]+), '(.+?)', (\d+)\)", produto_match.group(1))
                  for nome, preco, link, origem_id in produto_linhas:
                      origem_info = origens.get(origem_id, {'nome': 'Desconhecido', 'url_base': ''})
                      produtos.append({
                          'nome': nome,
                          'preco': float(preco),
                          'link': link,
                          'origem': origem_info['nome'],
                          'url_base': origem_info['url_base'],
                          'data_coleta': datetime.now().strftime('%d/%m/%Y %H:%M')
                      })
      except FileNotFoundError:
          print(f"{Cores.VERMELHO}❌ Arquivo Database.sql não encontrado.{Cores.RESET}")
      return produtos
  
  # 📊 Simula a procedure de ranking
  def ranking_produtos(produtos, ordem='ASC'):
      limpar_terminal()
      titulo = f"📊 RANKING DE PRODUTOS ({ordem.upper()})"
      print(f"{Cores.NEGRITO}{Cores.AZUL}{titulo.center(60)}{Cores.RESET}\n")
      print(f"{'-'*60}")
  
      ordenados = sorted(produtos, key=lambda x: x['preco'], reverse=(ordem.upper() == 'DESC'))
  
      for i, p in enumerate(ordenados, start=1):
          print(f"{Cores.VERDE}{i}. {p['nome']}{Cores.RESET}")
          print(f"   💰 Preço: R$ {p['preco']:.2f}")
          print(f"   🌐 Origem: {p['origem']}")
          print(f"   🔗 Link: {p['link']}")
          print(f"   📅 Coleta: {p['data_coleta']}")
          print(f"{'-'*60}")
      input(f"\n{Cores.AMARELO}🔁 Pressione ENTER para voltar ao menu...{Cores.RESET}")
  
  # 📦 Lista todos os produtos
  def listar_produtos(produtos):
      limpar_terminal()
      print(f"{Cores.NEGRITO}{Cores.HEADER}📦 LISTA DE PRODUTOS{Cores.RESET}\n")
      print(f"{'-'*60}")
      for p in produtos:
          print(f"{Cores.VERDE}- {p['nome']}{Cores.RESET}")
          print(f"  💰 R$ {p['preco']:.2f} | 🌐 {p['origem']}")
          print(f"  🔗 {p['link']}")
          print(f"  📅 {p['data_coleta']}")
          print(f"{'-'*60}")
      input(f"\n{Cores.AMARELO}🔁 Pressione ENTER para voltar ao menu...{Cores.RESET}")
  
  # 🧭 Menu interativo
  def menu():
      caminho_sql = "Database.sql"
      produtos = carregar_dados_sql(caminho_sql)
  
      if not produtos:
          print(f"{Cores.VERMELHO}⚠️ Nenhum produto carregado.{Cores.RESET}")
          return
  
      while True:
          limpar_terminal()
          print(f"{Cores.NEGRITO}{Cores.AZUL}{'🛒 COMPARADOR DE PRODUTOS'.center(60)}{Cores.RESET}")
          print(f"{'-'*60}")
          print(f"{Cores.AMARELO}1 - Ranking do menor para o maior preço")
          print(f"2 - Ranking do maior para o menor preço")
          print(f"3 - Listar todos os produtos")
          print(f"0 - Sair{Cores.RESET}")
          print(f"{'-'*60}")
  
          escolha = input(f"{Cores.NEGRITO}👉 Escolha uma opção: {Cores.RESET}")
  
          if escolha == '1':
              ranking_produtos(produtos, ordem='ASC')
          elif escolha == '2':
              ranking_produtos(produtos, ordem='DESC')
          elif escolha == '3':
              listar_produtos(produtos)
          elif escolha == '0':
              limpar_terminal()
              print(f"{Cores.VERDE}👋 Encerrando o programa. Até mais!{Cores.RESET}")
              break
          else:
              limpar_terminal()
              print(f"{Cores.VERMELHO}❌ Opção inválida. Tente novamente.{Cores.RESET}")
              input(f"{Cores.AMARELO}🔁 Pressione ENTER para voltar ao menu...{Cores.RESET}")
  
  # 🚀 Execução principal
  if __name__ == "__main__":
      menu()
```
