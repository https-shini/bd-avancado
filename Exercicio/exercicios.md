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
