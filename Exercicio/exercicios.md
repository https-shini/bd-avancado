# 📚 Laboratório de Banco de Dados Avançado
## Soluções Completas dos Exercícios

> **Atividade:** Máximo 3 integrantes | **Pontuação:** Até 2 pontos

---

## 📋 Índice de Conteúdo

1. [Exercício 1 - Web Scraping de Preços](#exercício-1-comparador-de-preços-web-scraping)
2. [Exercício 2 - Jokenpô em PL/SQL](#exercício-2-jogo-jokenpô-em-plsql)
3. [Exercício 3 - Controle de Estoque](#exercício-3-controle-de-estoque-com-cursor)
4. [Formato de Entrega](#formato-de-entrega)

---

# Exercício 1: Comparador de Preços (Web Scraping)

**Pontuação:** 1.0 ponto

## 📌 Requisitos

| # | Requisito | Status |
|---|-----------|--------|
| 1 | Desenvolver aplicação em **Python** | ✅ |
| 2 | Coletar dados de **mínimo 3 sites diferentes** | ✅ |
| 3 | Usar biblioteca **BeautifulSoup** | ✅ |
| 4 | Armazenar em banco de dados **MySQL** | ✅ |
| 5 | Dados: ID, nome, valor, link de origem | ✅ |
| 6 | Criar **Procedure** para ranking | ✅ |
| 7 | Ordenação configurável (ASC/DESC) | ✅ |

---

## 💾 Solução 1A: Criar Banco de Dados (MySQL)

```sql
-- ============================================================
-- CRIAR BANCO DE DADOS
-- ============================================================
CREATE DATABASE IF NOT EXISTS comparador_precos;
USE comparador_precos;

-- ============================================================
-- TABELA PRINCIPAL DE PRODUTOS
-- ============================================================
CREATE TABLE produtos (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    nome_produto VARCHAR(255) NOT NULL,
    valor_produto DECIMAL(10, 2) NOT NULL,
    link_origem VARCHAR(500) NOT NULL,
    site_origem VARCHAR(100) NOT NULL,
    data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nome (nome_produto),
    INDEX idx_valor (valor_produto),
    INDEX idx_site (site_origem)
);

-- ============================================================
-- TABELA DE HISTÓRICO DE PREÇOS
-- ============================================================
CREATE TABLE historico_precos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_produto INT NOT NULL,
    valor_antigo DECIMAL(10, 2),
    valor_novo DECIMAL(10, 2),
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
    INDEX idx_produto (id_produto)
);

-- ============================================================
-- CONFIRMAR CRIAÇÃO
-- ============================================================
SHOW TABLES;
DESCRIBE produtos;
```

---

## 💾 Solução 1B: Criar Procedure de Ranking (MySQL)

```sql
-- ============================================================
-- PROCEDURE: RANKING DE PRODUTOS
-- Parâmetro: p_ordenacao = 'ASC' (menor→maior) ou 'DESC' (maior→menor)
-- ============================================================
DELIMITER //

CREATE PROCEDURE sp_ranking_produtos(
    IN p_ordenacao VARCHAR(10)
)
BEGIN
    DECLARE v_total INT;
    
    -- Validar parâmetro
    IF p_ordenacao NOT IN ('ASC', 'DESC') THEN
        SELECT 'ERRO: Parâmetro inválido! Use ASC ou DESC' AS mensagem;
    ELSE
        -- Contar total de produtos
        SELECT COUNT(*) INTO v_total FROM produtos;
        
        IF v_total = 0 THEN
            SELECT 'Nenhum produto registrado no banco de dados' AS mensagem;
        ELSE
            -- Exibir ranking
            IF p_ordenacao = 'ASC' THEN
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY valor_produto ASC) AS ranking,
                    id_produto,
                    nome_produto,
                    valor_produto,
                    site_origem,
                    link_origem,
                    data_coleta
                FROM produtos
                ORDER BY valor_produto ASC;
            ELSE
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY valor_produto DESC) AS ranking,
                    id_produto,
                    nome_produto,
                    valor_produto,
                    site_origem,
                    link_origem,
                    data_coleta
                FROM produtos
                ORDER BY valor_produto DESC;
            END IF;
        END IF;
    END IF;
END //

DELIMITER ;

-- ============================================================
-- TESTAR PROCEDURE
-- ============================================================
CALL sp_ranking_produtos('ASC');   -- Menor para maior preço
CALL sp_ranking_produtos('DESC');  -- Maior para menor preço
```

---

## 🐍 Solução 1C: Código Python com Web Scraping

```python
# ============================================================
# COMPARADOR DE PREÇOS - WEB SCRAPING
# Bibliotecas necessárias: pip install requests beautifulsoup4 mysql-connector-python
# ============================================================

import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import time

# ============================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sua_senha',  # ⚠️ ALTERE PARA SUA SENHA
    'database': 'comparador_precos'
}

# ============================================================
# CLASSE PARA GERENCIAR BANCO DE DADOS
# ============================================================
class GerenciadorBanco:
    def __init__(self, config):
        self.config = config
        self.conexao = None
        self.cursor = None
        self.conectar()
    
    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(**self.config)
            self.cursor = self.conexao.cursor()
            print("✓ Conexão com banco de dados estabelecida")
        except mysql.connector.Error as err:
            print(f"✗ Erro ao conectar: {err}")
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
            print(f"✗ Erro ao inserir: {err}")
            return False
    
    def limpar_dados(self):
        try:
            self.cursor.execute("TRUNCATE TABLE produtos")
            self.conexao.commit()
            print("✓ Dados anteriores removidos")
        except mysql.connector.Error as err:
            print(f"✗ Erro ao limpar: {err}")
    
    def exibir_ranking(self, ordenacao='ASC'):
        try:
            self.cursor.callproc('sp_ranking_produtos', [ordenacao])
            for result in self.cursor.stored_results():
                resultados = result.fetchall()
                return resultados
        except mysql.connector.Error as err:
            print(f"✗ Erro ao exibir ranking: {err}")
            return []
    
    def fechar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()
        print("✓ Conexão fechada")

# ============================================================
# FUNÇÃO: SCRAPING - SITE 1 (Amazon)
# ============================================================
def scrape_amazon():
    print("\n[1/3] Coletando dados do Amazon...")
    produtos = []
    
    try:
        url = "https://www.amazon.com.br/s?k=notebook"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in items[:5]:
            try:
                # Nome do produto
                nome_elem = item.find('h2', {'class': 's-size-mini'})
                nome = nome_elem.text.strip() if nome_elem else 'N/A'
                
                # Preço
                preco_elem = item.find('span', {'class': 'a-price-whole'})
                if preco_elem:
                    preco_text = preco_elem.text.replace('R$', '').replace('.', '').replace(',', '.')
                    preco = float(preco_text.strip())
                else:
                    continue
                
                # Link
                link_elem = item.find('a', {'class': 's-link'})
                link = 'https://www.amazon.com.br' + link_elem['href'] if link_elem else 'N/A'
                
                produtos.append({
                    'nome': nome,
                    'preco': preco,
                    'link': link,
                    'site': 'Amazon'
                })
                
            except Exception as e:
                continue
        
        print(f"   ✓ {len(produtos)} produtos coletados do Amazon")
        return produtos
        
    except Exception as e:
        print(f"   ✗ Erro ao coletar Amazon: {e}")
        return []

# ============================================================
# FUNÇÃO: SCRAPING - SITE 2 (Mercado Livre)
# ============================================================
def scrape_mercado_livre():
    print("\n[2/3] Coletando dados do Mercado Livre...")
    produtos = []
    
    try:
        url = "https://lista.mercadolivre.com.br/notebook"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', {'class': 'ui-search-result__wrapper'})
        
        for item in items[:5]:
            try:
                # Nome do produto
                nome_elem = item.find('h2', {'class': 'ui-search-item__title'})
                nome = nome_elem.text.strip() if nome_elem else 'N/A'
                
                # Preço
                preco_elem = item.find('span', {'class': 'price-tag-fraction'})
                if preco_elem:
                    preco_text = preco_elem.text.replace('R$', '').replace('.', '').replace(',', '.')
                    preco = float(preco_text.strip())
                else:
                    continue
                
                # Link
                link_elem = item.find('a', {'class': 'ui-search-link'})
                link = link_elem['href'] if link_elem else 'N/A'
                
                produtos.append({
                    'nome': nome,
                    'preco': preco,
                    'link': link,
                    'site': 'Mercado Livre'
                })
                
            except Exception as e:
                continue
        
        print(f"   ✓ {len(produtos)} produtos coletados do Mercado Livre")
        return produtos
        
    except Exception as e:
        print(f"   ✗ Erro ao coletar Mercado Livre: {e}")
        return []

# ============================================================
# FUNÇÃO: SCRAPING - SITE 3 (Shopee)
# ============================================================
def scrape_shopee():
    print("\n[3/3] Coletando dados do Shopee...")
    produtos = []
    
    try:
        url = "https://shopee.com.br/search?keyword=notebook"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', {'class': 'shopee-search-item-result'})
        
        for item in items[:5]:
            try:
                # Nome do produto
                nome_elem = item.find('div', {'class': 'KCqxqK'})
                nome = nome_elem.text.strip() if nome_elem else 'N/A'
                
                # Preço
                preco_elem = item.find('span', {'class': 'ooOvZ6'})
                if preco_elem:
                    preco_text = preco_elem.text.replace('R$', '').replace('.', '').replace(',', '.')
                    preco = float(preco_text.strip())
                else:
                    continue
                
                # Link
                link_elem = item.find('a')
                link = link_elem['href'] if link_elem else 'N/A'
                
                produtos.append({
                    'nome': nome,
                    'preco': preco,
                    'link': link,
                    'site': 'Shopee'
                })
                
            except Exception as e:
                continue
        
        print(f"   ✓ {len(produtos)} produtos coletados do Shopee")
        return produtos
        
    except Exception as e:
        print(f"   ✗ Erro ao coletar Shopee: {e}")
        return []

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================
def main():
    print("=" * 70)
    print("   COMPARADOR DE PREÇOS - WEB SCRAPING")
    print("=" * 70)
    
    # Conectar ao banco
    banco = GerenciadorBanco(DB_CONFIG)
    banco.limpar_dados()
    
    # Coletar de todos os sites
    todos_produtos = []
    todos_produtos.extend(scrape_amazon())
    time.sleep(2)  # Pausa para não sobrecarregar servidores
    todos_produtos.extend(scrape_mercado_livre())
    time.sleep(2)
    todos_produtos.extend(scrape_shopee())
    
    # Inserir no banco
    print("\n" + "=" * 70)
    print("   INSERINDO DADOS NO BANCO DE DADOS")
    print("=" * 70)
    
    contador = 0
    for produto in todos_produtos:
        if banco.inserir_produto(
            produto['nome'],
            produto['preco'],
            produto['link'],
            produto['site']
        ):
            contador += 1
    
    print(f"✓ {contador} produtos inseridos com sucesso!\n")
    
    # Exibir ranking
    print("=" * 70)
    print("   RANKING: MENOR PARA MAIOR PREÇO (ASC)")
    print("=" * 70)
    ranking_asc = banco.exibir_ranking('ASC')
    
    if ranking_asc:
        print(f"{'Rank':<6} {'Produto':<40} {'Preço':<12} {'Site':<20}")
        print("-" * 78)
        for row in ranking_asc:
            print(f"{row[0]:<6} {row[2][:40]:<40} R$ {row[3]:<10.2f} {row[4]:<20}")
    
    print("\n" + "=" * 70)
    print("   RANKING: MAIOR PARA MENOR PREÇO (DESC)")
    print("=" * 70)
    ranking_desc = banco.exibir_ranking('DESC')
    
    if ranking_desc:
        print(f"{'Rank':<6} {'Produto':<40} {'Preço':<12} {'Site':<20}")
        print("-" * 78)
        for row in ranking_desc:
            print(f"{row[0]:<6} {row[2][:40]:<40} R$ {row[3]:<10.2f} {row[4]:<20}")
    
    # Fechar conexão
    banco.fechar()
    print("\n✓ Processo finalizado com sucesso!")

# ============================================================
# EXECUTAR
# ============================================================
if __name__ == '__main__':
    main()
```

---

## 📦 Instalação das Dependências

```bash
# Instalar bibliotecas necessárias
pip install requests beautifulsoup4 mysql-connector-python

# Verificar instalação
pip show requests beautifulsoup4 mysql-connector-python
```

---

# Exercício 2: Jogo Jokenpô em PL/SQL

**Pontuação:** 0.5 ponto

## 📌 Requisitos

| # | Requisito | Status |
|---|-----------|--------|
| 1 | Simular jogo Jokenpô em **PL/SQL** | ✅ |
| 2 | Usuário informa sua jogada | ✅ |
| 3 | Oracle gera jogada do PC **aleatoriamente** | ✅ |
| 4 | Comparar jogadas e definir resultado | ✅ |
| 5 | Salvar jogadas em tabela | ✅ |
| 6 | Consultar: vitórias usuário, PC e empates | ✅ |

---

## 💾 Solução 2A: Criar Banco de Dados (Oracle)

```sql
-- ============================================================
-- CRIAR TABELA DE JOGADAS JOKENPÔ
-- ============================================================
CREATE TABLE tb_jogadas_jokenpo (
    id_jogada NUMBER PRIMARY KEY,
    jogada_usuario VARCHAR2(50) NOT NULL,
    jogada_pc VARCHAR2(50) NOT NULL,
    resultado VARCHAR2(50) NOT NULL,
    data_jogada TIMESTAMP DEFAULT SYSTIMESTAMP
);

-- ============================================================
-- CRIAR SEQUÊNCIA PARA AUTO_INCREMENT
-- ============================================================
CREATE SEQUENCE seq_jogadas_jokenpo
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

-- ============================================================
-- CRIAR ÍNDICES
-- ============================================================
CREATE INDEX idx_resultado ON tb_jogadas_jokenpo(resultado);
CREATE INDEX idx_data ON tb_jogadas_jokenpo(data_jogada);

-- ============================================================
-- VERIFICAR CRIAÇÃO
-- ============================================================
DESC tb_jogadas_jokenpo;
```

---

## 💾 Solução 2B: Bloco PL/SQL - Jogo Completo (Oracle)

```sql
-- ============================================================
-- BLOCO PL/SQL: JOGO JOKENPÔ
-- ============================================================

SET SERVEROUTPUT ON;

DECLARE
    -- Variáveis para o jogo
    v_jogada_usuario VARCHAR2(50);
    v_jogada_pc VARCHAR2(50);
    v_resultado VARCHAR2(50);
    v_numero_aleatorio NUMBER;
    v_num_jogadas NUMBER := 0;
    
BEGIN
    -- Inicializar gerador de números aleatórios
    DBMS_RANDOM.INITIALIZE(TO_CHAR(SYSDATE, 'DDMMYYSSHHMISS'));
    
    -- Loop para jogar múltiplas rodadas
    FOR v_rodada IN 1..5 LOOP
        DBMS_OUTPUT.PUT_LINE(CHR(10) || '========================================');
        DBMS_OUTPUT.PUT_LINE('          JOGO JOKENPÔ - RODADA ' || v_rodada);
        DBMS_OUTPUT.PUT_LINE('========================================');
        
        -- Simular entrada do usuário (trocar números para teste)
        -- Em um sistema real, receberia input do usuário
        v_numero_aleatorio := ROUND(DBMS_RANDOM.VALUE(1, 3));
        v_jogada_usuario := CASE v_numero_aleatorio
            WHEN 1 THEN 'Pedra'
            WHEN 2 THEN 'Papel'
            WHEN 3 THEN 'Tesoura'
        END;
        
        -- Gerar jogada aleatória do computador
        v_numero_aleatorio := ROUND(DBMS_RANDOM.VALUE(1, 3));
        v_jogada_pc := CASE v_numero_aleatorio
            WHEN 1 THEN 'Pedra'
            WHEN 2 THEN 'Papel'
            WHEN 3 THEN 'Tesoura'
        END;
        
        -- Determinar resultado da rodada
        IF v_jogada_usuario = v_jogada_pc THEN
            v_resultado := 'Empate';
            
        ELSIF (v_jogada_usuario = 'Pedra' AND v_jogada_pc = 'Tesoura') OR
              (v_jogada_usuario = 'Papel' AND v_jogada_pc = 'Pedra') OR
              (v_jogada_usuario = 'Tesoura' AND v_jogada_pc = 'Papel') THEN
            v_resultado := 'Vitória do Usuário';
            
        ELSE
            v_resultado := 'Vitória do PC';
            
        END IF;
        
        -- Exibir resultado da rodada
        DBMS_OUTPUT.PUT_LINE('Você jogou: ' || LPAD(v_jogada_usuario, 10));
        DBMS_OUTPUT.PUT_LINE('PC jogou:   ' || LPAD(v_jogada_pc, 10));
        DBMS_OUTPUT.PUT_LINE('Resultado:  ' || v_resultado);
        DBMS_OUTPUT.PUT_LINE('========================================');
        
        -- Inserir na tabela de histórico
        INSERT INTO tb_jogadas_jokenpo 
        VALUES (
            seq_jogadas_jokenpo.NEXTVAL, 
            v_jogada_usuario, 
            v_jogada_pc, 
            v_resultado, 
            SYSTIMESTAMP
        );
        
        v_num_jogadas := v_num_jogadas + 1;
        
    END LOOP;
    
    -- Confirmar inserção
    COMMIT;
    
    -- Exibir estatísticas finais
    DBMS_OUTPUT.PUT_LINE(CHR(10) || CHR(10) || '=======================================');
    DBMS_OUTPUT.PUT_LINE('      ESTATÍSTICAS FINAIS (5 RODADAS)');
    DBMS_OUTPUT.PUT_LINE('=======================================');
    
    FOR rec IN (
        SELECT 
            resultado,
            COUNT(*) total
        FROM tb_jogadas_jokenpo
        WHERE data_jogada >= TRUNC(SYSDATE)
        GROUP BY resultado
        ORDER BY CASE resultado
            WHEN 'Vitória do Usuário' THEN 1
            WHEN 'Vitória do PC' THEN 2
            WHEN 'Empate' THEN 3
        END
    ) LOOP
        DBMS_OUTPUT.PUT_LINE(RPAD(rec.resultado, 25) || ': ' || LPAD(rec.total, 2) || ' rodada(s)');
    END LOOP;
    
    DBMS_OUTPUT.PUT_LINE('=======================================');
    
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('ERRO: ' || SQLERRM);
        ROLLBACK;
END;
/
```

---

## 💾 Solução 2C: Procedure com Parâmetro (Oracle)

```sql
-- ============================================================
-- PROCEDURE: JOGAR JOKENPÔ
-- Parâmetro: p_jogada_usuario (Pedra, Papel, Tesoura)
-- ============================================================

CREATE OR REPLACE PROCEDURE sp_jogar_jokenpo(
    p_jogada_usuario IN VARCHAR2
) AS
    v_jogada_pc VARCHAR2(50);
    v_resultado VARCHAR2(50);
    v_numero_aleatorio NUMBER;
    
BEGIN
    -- Validar entrada
    IF UPPER(p_jogada_usuario) NOT IN ('PEDRA', 'PAPEL', 'TESOURA') THEN
        DBMS_OUTPUT.PUT_LINE('✗ ERRO: Digite uma jogada válida!');
        DBMS_OUTPUT.PUT_LINE('   Opções: Pedra, Papel ou Tesoura');
        RETURN;
    END IF;
    
    -- Gerar jogada aleatória do PC
    DBMS_RANDOM.INITIALIZE(TO_CHAR(SYSDATE, 'DDMMYYSSHHMISS'));
    v_numero_aleatorio := ROUND(DBMS_RANDOM.VALUE(1, 3));
    v_jogada_pc := CASE v_numero_aleatorio
        WHEN 1 THEN 'Pedra'
        WHEN 2 THEN 'Papel'
        WHEN 3 THEN 'Tesoura'
    END;
    
    -- Comparar jogadas
    IF UPPER(p_jogada_usuario) = v_jogada_pc THEN
        v_resultado := 'Empate';
        
    ELSIF (UPPER(p_jogada_usuario) = 'PEDRA' AND v_jogada_pc = 'Tesoura') OR
          (UPPER(p_jogada_usuario) = 'PAPEL' AND v_jogada_pc = 'Pedra') OR
          (UPPER(p_jogada_usuario) = 'TESOURA' AND v_jogada_pc = 'Papel') THEN
        v_resultado := 'Vitória do Usuário';
        
    ELSE
        v_resultado := 'Vitória do PC';
        
    END IF;
    
    -- Exibir resultado
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('╔═══════════════════════════════════════╗');
    DBMS_OUTPUT.PUT_LINE('║         RESULTADO DA RODADA           ║');
    DBMS_OUTPUT.PUT_LINE('╚═══════════════════════════════════════╝');
    DBMS_OUTPUT.PUT_LINE('  Você jogou:  ' || RPAD(UPPER(p_jogada_usuario), 15));
    DBMS_OUTPUT.PUT_LINE('  PC jogou:    ' || RPAD(v_jogada_pc, 15));
    DBMS_OUTPUT.PUT_LINE('  Resultado:   ' || v_resultado);
    DBMS_OUTPUT.PUT_LINE('');
    
    -- Inserir no histórico
    INSERT INTO tb_jogadas_jokenpo 
    VALUES (seq_jogadas_jokenpo.NEXTVAL, UPPER(p_jogada_usuario), v_jogada_pc, v_resultado, SYSTIMESTAMP);
    COMMIT;
    
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('ERRO: ' || SQLERRM);
END sp_jogar_jokenpo;
/
```

---

## 💾 Solução 2D: Consultas para Estatísticas (Oracle)

```sql
-- ============================================================
-- CONSULTA 1: TODAS AS JOGADAS REGISTRADAS
-- ============================================================
SELECT 
    id_jogada,
    jogada_usuario,
    jogada_pc,
    resultado,
    TO_CHAR(data_jogada, 'DD/MM/YYYY HH:MI:SS') AS data_hora
FROM tb_jogadas_jokenpo
ORDER BY data_jogada DESC;

-- ============================================================
-- CONSULTA 2: ESTATÍSTICAS GERAIS
-- ============================================================
SELECT 
    SUM(CASE WHEN resultado = 'Vitória do Usuário' THEN 1 ELSE 0 END) AS total_vitoria_usuario,
    SUM(CASE WHEN resultado = 'Vitória do PC' THEN 1 ELSE 0 END) AS total_vitoria_pc,
    SUM(CASE WHEN resultado = 'Empate' THEN 1 ELSE 0 END) AS total_empates,
    COUNT(*) AS total_jogadas
FROM tb_jogadas_jokenpo;

-- ============================================================
-- CONSULTA 3: PERCENTUAIS
-- ============================================================
SELECT 
    resultado,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tb_jogadas_jokenpo), 2) AS percentual
FROM tb_jogadas_jokenpo
GROUP BY resultado
ORDER BY total DESC;

-- ============================================================
-- CONSULTA 4: JOGADAS REALIZADAS HOJE
-- ============================================================
SELECT 
    COUNT(*) AS jogadas_hoje,
    SUM(CASE WHEN resultado = 'Vitória do Usuário' THEN 1 ELSE 0 END) AS vitoria_usuario_hoje,
    SUM(CASE WHEN resultado = 'Vitória do PC' THEN 1 ELSE 0 END) AS vitoria_pc_hoje
FROM tb_jogadas_jokenpo
WHERE TRUNC(data_jogada) = TRUNC(SYSDATE);

-- ============================================================
-- TESTAR PROCEDURE
-- ============================================================
SET SERVEROUTPUT ON;
EXEC sp_jogar_jokenpo('Pedra');
EXEC sp_jogar_jokenpo('Papel');
EXEC sp_jogar_jokenpo('Tesoura');
```

---

# Exercício 3: Controle de Estoque com Cursor

**Pontuação:** 0.5 ponto

## 📌 Requisitos

| # | Requisito | Status |
|---|-----------|--------|
| 1 | Procedure recebe: ID do produto e quantidade | ✅ |
| 2 | Verificar estoque disponível | ✅ |
| 3 | Se SIM: inserir em tbPedidos e baixar estoque | ✅ |
| 4 | Se NÃO: registrar em tabela de log | ✅ |
| 5 | Procedure com cursor para produtos críticos | ✅ |
| 6 | Exibir: classificação baixa ou sem estoque | ✅ |

---

## 💾 Solução 3A: Criar Banco de Dados (Oracle)

```sql
-- ============================================================
-- CRIAR TABELAS
-- ============================================================

-- Tabela de produtos
CREATE TABLE tb_produtos (
    id_produto NUMBER PRIMARY KEY,
    nome_produto VARCHAR2(100) NOT NULL,
    valor_produto NUMBER(10, 2) NOT NULL,
    quantidade_estoque NUMBER NOT NULL,
    classificacao VARCHAR2(50) DEFAULT 'Normal'
);

-- Tabela de pedidos
CREATE TABLE tb_
