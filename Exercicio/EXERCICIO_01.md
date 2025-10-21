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

## 📁 Arquivos do Exercício

```
exercicio01/
├── database.sql           # Script MySQL completo
├── main.py               # Aplicação Python
├── requirements.txt      # Dependências
└── README.md            # Esta documentação
```

---

## 💾 Estrutura do Banco de Dados MySQL

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
