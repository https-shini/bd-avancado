import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import re
import time
import random

# ======================================================
# 🎨 CONFIGURAÇÃO DE CORES PARA TERMINAL
# ======================================================
class Cores:
    HEADER = '\033[95m'
    AZUL = '\033[94m'
    CIANO = '\033[96m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    NEGRITO = '\033[1m'
    SUBLINHADO = '\033[4m'
    RESET = '\033[0m'


def limpar_terminal():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_banner():
    """Exibe banner inicial do sistema"""
    limpar_terminal()
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.CIANO}{'🛒 COMPARADOR DE PRODUTOS - WEB SCRAPING':^70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}")
    print(f"{Cores.AMARELO}Exercício 01 - Laboratório de Banco de Dados Avançado{Cores.RESET}".center(78))
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}\n")


# ======================================================
# 🌐 CONFIGURAÇÃO DE HEADERS PARA REQUISIÇÕES
# ======================================================
def gerar_headers():
    """Gera headers simples para evitar bloqueios"""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }


# ======================================================
# 💰 FUNÇÃO PARA LIMPAR E CONVERTER VALORES MONETÁRIOS
# ======================================================
def limpar_preco(valor):
    try:
        # Remove tudo exceto números e vírgula
        valor_limpo = re.sub(r'[^\d,]', '', valor)
        # Troca vírgula por ponto
        valor_limpo = valor_limpo.replace(',', '.')
        return float(valor_limpo)
    except (ValueError, AttributeError):
        return 0.0


# ======================================================
# 🌐 FUNÇÕES DE WEB SCRAPING (3 SITES)
# ======================================================
def scrape_venturi():
    url = "http://www.venturigaming.com.br/produtos/processador-amd-ryzen-7-5700x-8-core-16-threads-cache-36mb-3-4ghz-4-6ghz-max-turbo-am4-100-100000926wof/"
    loja = "Venturi Gaming"

    try:
        print(f"{Cores.AMARELO}🔍 Coletando dados de {loja}...{Cores.RESET}")

        resposta = requests.get(url, headers=gerar_headers(), timeout=15)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Buscar nome do produto
        nome = soup.find("h1", class_="js-product-name h2 h1-md")
        # Buscar preço
        preco = soup.find("strong", class_="js-price-display text-primary mb-2")

        nome_produto = nome.text.strip() if nome else "Processador AMD Ryzen 7 5700X"
        preco_valor = preco.text.strip() if preco else "0"

        preco_final = limpar_preco(preco_valor)

        return {
            "loja": loja,
            "nome": nome_produto,
            "preco": preco_final,
            "link": url,
            "sucesso": preco_final > 0
        }

    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao coletar de {loja}: {str(e)[:50]}{Cores.RESET}")
        return {
            "loja": loja,
            "nome": "Processador AMD Ryzen 7 5700X (Venturi Gaming)",
            "preco": 0.0,
            "link": url,
            "sucesso": False
        }


def scrape_kabum():
    url = "https://www.kabum.com.br/produto/729769/amd-ryzen-7-5700x-8-nucleos-16-threads-3-4ghz-turbo-4-6-ghz-cache-35mb-am4-tdp-65w-100-000000926"
    loja = "Kabum"

    try:
        print(f"{Cores.AMARELO}🔍 Coletando dados de {loja}...{Cores.RESET}")

        resposta = requests.get(url, headers=gerar_headers(), timeout=15)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Buscar nome do produto
        nome = soup.find("h1", class_="text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold")
        # Buscar preço
        preco = soup.find("h4", class_="text-4xl text-secondary-500 font-bold transition-all duration-500")

        nome_produto = nome.text.strip() if nome else "AMD Ryzen 7 5700X 8-Núcleos 16-Threads"
        preco_valor = preco.text.strip() if preco else "0"

        preco_final = limpar_preco(preco_valor)

        return {
            "loja": loja,
            "nome": nome_produto,
            "preco": preco_final,
            "link": url,
            "sucesso": preco_final > 0
        }

    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao coletar de {loja}: {str(e)[:50]}{Cores.RESET}")
        return {
            "loja": loja,
            "nome": "AMD Ryzen 7 5700X 8-Núcleos 16-Threads (Kabum)",
            "preco": 0.0,
            "link": url,
            "sucesso": False
        }


def scrape_mercadolivre():
    url = "http://www.mercadolivre.com.br/processador-amd-ryzen-7-5700x-100-100000926wof-de-8-nucleos-e-46ghz/p/MLB19159879"
    loja = "Mercado Livre"

    try:
        print(f"{Cores.AMARELO}🔍 Coletando dados de {loja}...{Cores.RESET}")

        resposta = requests.get(url, headers=gerar_headers(), timeout=15)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Buscar nome do produto
        nome = soup.find("h1", class_="ui-pdp-title")
        # Buscar preço
        preco = soup.find("span", class_="andes-money-amount__fraction")

        nome_produto = nome.text.strip() if nome else "Processador AMD Ryzen 7 5700X"
        preco_valor = preco.text.strip().split()[0] if preco else "0"

        preco_final = limpar_preco(preco_valor)

        return {
            "loja": loja,
            "nome": nome_produto,
            "preco": preco_final,
            "link": url,
            "sucesso": preco_final > 0
        }

    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao coletar de {loja}: {str(e)[:50]}{Cores.RESET}")
        return {
            "loja": loja,
            "nome": "Processador AMD Ryzen 7 5700X 8-Núcleos 16-Threads (Mercado Livre)",
            "preco": 0.0,
            "link": url,
            "sucesso": False
        }


# ======================================================
# 🗄️ FUNÇÕES DE BANCO DE DADOS
# ======================================================

def obter_conexao():
    configs = [
        # Config 1: Sua configuração
        {
            "host": "localhost",
            "user": "root",
            "password": "admin",
            "database": "comparador_produtos",
            "port": 3306
        },
        # Config 2: XAMPP padrão (sem senha)
        {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "comparador_produtos",
            "port": 3306
        },
    ]

    print(f"\n{Cores.CIANO}🔌 Tentando conectar ao MySQL...{Cores.RESET}")

    for i, config in enumerate(configs):
        porta = config.get('port', 3306)
        db = config.get('database', 'N/A')

        print(f"{Cores.AMARELO}   Tentativa {i+1}: Porta {porta}, DB: {db}{Cores.RESET}", end="")

        try:
            conn = mysql.connector.connect(**config)
            print(f" {Cores.VERDE}✅{Cores.RESET}")

            # Se conectou sem banco, criar o banco
            if 'database' not in config:
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS comparador_produtos")
                cursor.execute("USE comparador_produtos")
                cursor.close()

            return conn

        except Error as e:
            print(f" {Cores.VERMELHO}❌{Cores.RESET}")
            continue

    print(f"\n{Cores.VERMELHO}{'='*70}{Cores.RESET}")
    print(f"{Cores.VERMELHO}❌ NÃO FOI POSSÍVEL CONECTAR AO MYSQL{Cores.RESET}")
    print(f"{Cores.VERMELHO}{'='*70}{Cores.RESET}\n")
    print(f"{Cores.AMARELO}📋 Soluções possíveis:{Cores.RESET}\n")
    print(f"{Cores.CIANO}1. Verifique se o MySQL está rodando{Cores.RESET}")
    print(f"{Cores.CIANO}2. Verifique usuário e senha{Cores.RESET}")
    print(f"{Cores.CIANO}3. Execute o script SQL manualmente{Cores.RESET}\n")

    return None


def criar_estrutura_banco(conn):
    #Cria a estrutura do banco se não existir
    try:
        cursor = conn.cursor()

        # Criar tabela produtos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                link TEXT NOT NULL,
                loja VARCHAR(100) NOT NULL,
                data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_preco (preco),
                INDEX idx_loja (loja)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # Verificar se procedure existe e criar
        cursor.execute("DROP PROCEDURE IF EXISTS sp_ranking_produtos")

        cursor.execute("""
            CREATE PROCEDURE sp_ranking_produtos(IN ordem VARCHAR(4))
            BEGIN
                IF UPPER(ordem) NOT IN ('ASC', 'DESC') THEN
                    SELECT 'ERRO: Parâmetro inválido. Use ASC ou DESC' AS mensagem;
                ELSE
                    IF UPPER(ordem) = 'ASC' THEN
                        SELECT nome, preco, loja, link
                        FROM produtos
                        ORDER BY preco ASC, id DESC;
                    ELSE
                        SELECT nome, preco, loja, link
                        FROM produtos
                        ORDER BY preco DESC, id DESC;
                    END IF;
                END IF;
            END
        """)

        conn.commit()
        cursor.close()
        print(f"{Cores.VERDE}✅ Estrutura do banco criada com sucesso!{Cores.RESET}")

    except Error as e:
        print(f"{Cores.VERMELHO}❌ Erro ao criar estrutura: {e}{Cores.RESET}")


def inserir_produtos_banco(produtos):
    # Insere lista de produtos no banco de dados
    conn = obter_conexao()
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        # Query SEM data_coleta - usa DEFAULT CURRENT_TIMESTAMP
        query = """
            INSERT INTO produtos (nome, preco, link, loja)
            VALUES (%s, %s, %s, %s)
        """

        sucesso = 0
        for p in produtos:
            if p["preco"] > 0:  # Só insere se coletou preço válido
                valores = (
                    p["nome"],
                    p["preco"],
                    p["link"],
                    p["loja"]
                )
                cursor.execute(query, valores)
                sucesso += 1

        conn.commit()
        print(f"\n{Cores.VERDE}✅ {sucesso} produto(s) inserido(s) no banco de dados!{Cores.RESET}")
        return True

    except Error as e:
        print(f"{Cores.VERMELHO}❌ Erro ao inserir produtos: {e}{Cores.RESET}")
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def exibir_ranking(ordem="ASC"):
    # Chama a procedure sp_ranking_produtos e exibe resultados formatados
    conn = obter_conexao()
    if not conn:
        input(f"\n{Cores.AMARELO}🔌 Pressione ENTER para voltar ao menu...{Cores.RESET}")
        return

    try:
        cursor = conn.cursor()
        cursor.callproc("sp_ranking_produtos", [ordem.upper()])

        limpar_terminal()
        titulo = "📊 RANKING DE PRODUTOS"
        subtitulo = "Menor → Maior Preço" if ordem.upper() == "ASC" else "Maior → Menor Preço"

        print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}")
        print(f"{Cores.NEGRITO}{Cores.CIANO}{titulo:^70}{Cores.RESET}")
        print(f"{Cores.AMARELO}{subtitulo:^70}{Cores.RESET}")
        print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}\n")

        posicao = 1
        for result in cursor.stored_results():
            rows = result.fetchall()

            if not rows:
                print(f"{Cores.AMARELO}⚠️  Nenhum produto encontrado no banco.{Cores.RESET}")
                print(f"{Cores.AMARELO}💡 Execute a coleta de dados primeiro (opção 1).{Cores.RESET}\n")
                break

            for row in rows:
                nome, preco, origem, link = row

                # Determinar cor baseada na posição
                if posicao == 1:
                    cor_posicao = Cores.VERDE
                    emoji = "🥇"
                elif posicao == 2:
                    cor_posicao = Cores.CIANO
                    emoji = "🥈"
                elif posicao == 3:
                    cor_posicao = Cores.AMARELO
                    emoji = "🥉"
                else:
                    cor_posicao = Cores.RESET
                    emoji = f"{posicao}º"

                print(f"{cor_posicao}{Cores.NEGRITO}{emoji} {nome}{Cores.RESET}")
                print(f"   💰 Preço: {Cores.VERDE}R$ {preco:,.2f}{Cores.RESET}")
                print(f"   🏪 Loja: {origem}")
                print(f"   🔗 Link: {link[:60]}...")
                print(f"{Cores.AZUL}{'-'*70}{Cores.RESET}\n")

                posicao += 1

    except Error as e:
        print(f"{Cores.VERMELHO}❌ Erro ao consultar ranking: {e}{Cores.RESET}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def coletar_dados_lojas():
    # Executa web scraping de todas as lojas e exibe resultados
    exibir_banner()
    print(f"{Cores.CIANO}🌐 Iniciando coleta de dados das lojas...{Cores.RESET}\n")

    # Executar scraping de todas as lojas
    produtos = [
        scrape_venturi(),
        scrape_kabum(),
        scrape_mercadolivre()
    ]

    print(f"\n{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.CIANO}{'📦 PRODUTOS COLETADOS':^70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}\n")

    # Exibir produtos coletados
    for p in produtos:
        status = "✅" if p["sucesso"] else "⚠️"
        cor = Cores.VERDE if p["sucesso"] else Cores.AMARELO

        print(f"{cor}{status} {Cores.NEGRITO}{p['loja']}{Cores.RESET}")
        print(f"   📦 Produto: {p['nome'][:60]}...")

        if p["preco"] > 0:
            print(f"   💰 Preço: {Cores.VERDE}R$ {p['preco']:,.2f}{Cores.RESET}")
        else:
            print(f"   💰 Preço: {Cores.VERMELHO}Não disponível{Cores.RESET}")

        print(f"   🔗 Link: {p['link'][:60]}...")
        print()

    return produtos


# ======================================================
# 🎮 MENU PRINCIPAL
# ======================================================

def exibir_menu():
    # Exibe menu de opções
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.CIANO}{'📋 MENU PRINCIPAL':^70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}\n")

    print(f"{Cores.AMARELO}1 {Cores.RESET}- 🌐 Coletar dados das lojas (Web Scraping)")
    print(f"{Cores.AMARELO}2 {Cores.RESET}- 📊 Ranking ASC (Menor → Maior Preço)")
    print(f"{Cores.AMARELO}3 {Cores.RESET}- 📊 Ranking DESC (Maior → Menor Preço)")
    print(f"{Cores.AMARELO}4 {Cores.RESET}- 📋 Exibir informações do sistema")
    print(f"{Cores.AMARELO}5 {Cores.RESET}- 🔧 Testar conexão com MySQL")
    print(f"{Cores.AMARELO}0 {Cores.RESET}- 🚪 Sair do programa\n")
    print(f"{Cores.AZUL}{'-'*70}{Cores.RESET}")


def exibir_info_sistema():
    # Exibe informações sobre o sistema
    limpar_terminal()
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.CIANO}{'ℹ️  INFORMAÇÕES DO SISTEMA':^70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}\n")

    info = f"""
{Cores.NEGRITO}📌 Requisitos Atendidos:{Cores.RESET}

{Cores.VERDE}✅ a) Web Scraping de 3 sites diferentes:{Cores.RESET}
   • Venturi Gaming
   • Kabum
   • Mercado Livre

{Cores.VERDE}✅ b) Armazenamento em MySQL:{Cores.RESET}
   • Banco: comparador_produtos
   • Tabela: produtos (id, nome, preco, link, loja, data_coleta)

{Cores.VERDE}✅ c) Procedure para ranking ordenável:{Cores.RESET}
   • sp_ranking_produtos(ordem)
   • Parâmetros: 'ASC' ou 'DESC'

{Cores.NEGRITO}🛠️  Tecnologias Utilizadas:{Cores.RESET}
   • Python 3.x
   • BeautifulSoup4 (Web Scraping)
   • MySQL Connector
   • Requests

{Cores.NEGRITO}📊 Funcionalidades:{Cores.RESET}
   • Coleta automática de preços
   • Armazenamento com timestamp
   • Rankings ordenáveis
   • Interface colorida no terminal

{Cores.AMARELO}💡 Dica: Execute a opção 1 para coletar dados antes de visualizar rankings!{Cores.RESET}
    """

    print(info)


def testar_mysql():
    # Testa conexão com MySQL e exibe informações
    limpar_terminal()
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.CIANO}{'🔧 TESTE DE CONEXÃO MySQL':^70}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.AZUL}{'='*70}{Cores.RESET}\n")

    conn = obter_conexao()

    if conn:
        print(f"\n{Cores.VERDE}{'='*70}{Cores.RESET}")
        print(f"{Cores.VERDE}✅ CONEXÃO BEM-SUCEDIDA!{Cores.RESET}")
        print(f"{Cores.VERDE}{'='*70}{Cores.RESET}\n")

        try:
            cursor = conn.cursor()

            # Verificar tabela
            cursor.execute("SHOW TABLES LIKE 'produtos'")
            tabela = cursor.fetchone()

            if tabela:
                print(f"{Cores.VERDE}✅ Tabela 'produtos' encontrada{Cores.RESET}")

                # Contar registros
                cursor.execute("SELECT COUNT(*) FROM produtos")
                count = cursor.fetchone()[0]
                print(f"{Cores.CIANO}📊 Registros na tabela: {count}{Cores.RESET}")
            else:
                print(f"{Cores.AMARELO}⚠️  Tabela 'produtos' não encontrada. Criando...{Cores.RESET}")

            # Verificar procedure
            cursor.execute("SHOW PROCEDURE STATUS WHERE Name = 'sp_ranking_produtos'")
            procedure = cursor.fetchone()

            if procedure:
                print(f"{Cores.VERDE}✅ Procedure 'sp_ranking_produtos' encontrada{Cores.RESET}")
            else:
                print(f"{Cores.AMARELO}⚠️  Procedure não encontrada. Criando...{Cores.RESET}")

            cursor.close()
            conn.close()

        except Error as e:
            print(f"{Cores.VERMELHO}❌ Erro ao verificar banco: {e}{Cores.RESET}")
    else:
        print(f"\n{Cores.VERMELHO}{'='*70}{Cores.RESET}")
        print(f"{Cores.VERMELHO}❌ FALHA NA CONEXÃO{Cores.RESET}")
        print(f"{Cores.VERMELHO}{'='*70}{Cores.RESET}")


def main():
    # Função principal do programa
    exibir_banner()

    while True:
        exibir_menu()

        escolha = input(f"{Cores.NEGRITO}{Cores.CIANO}👉 Escolha uma opção: {Cores.RESET}").strip()

        if escolha == '1':
            produtos = coletar_dados_lojas()
            inserir_produtos_banco(produtos)
            input(f"\n{Cores.AMARELO}🔌 Pressione ENTER para voltar ao menu...{Cores.RESET}")
            exibir_banner()

        elif escolha == '2':
            exibir_ranking("ASC")
            input(f"\n{Cores.AMARELO}🔌 Pressione ENTER para voltar ao menu...{Cores.RESET}")
            exibir_banner()

        elif escolha == '3':
            exibir_ranking("DESC")
            input(f"\n{Cores.AMARELO}🔌 Pressione ENTER para voltar ao menu...{Cores.RESET}")
            exibir_banner()

        elif escolha == '4':
            exibir_info_sistema()
            input(f"\n{Cores.AMARELO}🔌 Pressione ENTER para voltar ao menu...{Cores.RESET}")
            exibir_banner()

        elif escolha == '5':
            testar_mysql()
            input(f"\n{Cores.AMARELO}🔌 Pressione ENTER para voltar ao menu...{Cores.RESET}")
            exibir_banner()

        elif escolha == '0':
            limpar_terminal()
            print(f"\n{Cores.VERDE}{'='*70}{Cores.RESET}")
            print(f"{Cores.NEGRITO}{Cores.CIANO}{'👋 Encerrando o Comparador de Produtos':^70}{Cores.RESET}")
            print(f"{Cores.VERDE}{'='*70}{Cores.RESET}\n")
            print(f"{Cores.AMARELO}Obrigado por usar o sistema! Até mais! 🚀{Cores.RESET}\n")
            break

        else:
            print(f"\n{Cores.VERMELHO}❌ Opção inválida! Escolha um número de 0 a 5.{Cores.RESET}")
            time.sleep(2)
            exibir_banner()


# ======================================================
# 🚀 EXECUÇÃO DO PROGRAMA
# ======================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        limpar_terminal()
        print(f"\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário.{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro inesperado: {e}{Cores.RESET}\n")
