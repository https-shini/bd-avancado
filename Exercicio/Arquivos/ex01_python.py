self.cursor.execute(sql, (nome, valor, link, site))
self.conexao.commit()
return True
except mysql.connector.Error as err:
print(f"✗ Erro ao inserir : {err}")
return False
def limpar_tabela(self):
try:
self.cursor.execute("TRUNCATE TABLE produtos")
self.conexao.commit()
print("✓ Tabela limpa")
except mysql.connector.Error as err:
print(f"✗ Erro ao limpar: {err}")
def exibir_ranking(self, ordenacao=):
try:
self.cursor.callproc(, [ordenacao])
for result in self.cursor.stored_results():
return result.fetchall()
except mysql.connector.Error as err:
print(f"✗ Erro no ranking: {err}")
return []
def fechar(self):
if self.cursor:
self.cursor.close()
if self.conexao:
self.conexao.close()
print("✓ Conexão fechada")
def scrape_kabum():
print("\n[1/3] Coletando Kabum...")
produtos = []
try:
dados_simulados = [
{
: ,
: 4299.90,
:
},
{
: ,
: 899.90,
:
},
{
: ,
: 299.99,
:
}
]
for item in dados_simulados:
produtos.append({
: item[],
: item[],
: item[],
:
})
print(f"   ✓ {len(produtos)} produtos coletados")
return produtos
except Exception as e:
print(f"   ✗ Erro: {e}")
return []
def scrape_amazon():
print("\n[2/3] Coletando Amazon...")
produtos = []
try:
dados_simulados = [
{
: ,
: 549.00,
:
},
{
: ,
: 399.99,
:
},
{
: ,
: 249.90,
:
}
]
for item in dados_simulados:
produtos.append({
: item[],
: item[],
: item[],
:
})
print(f"   ✓ {len(produtos)} produtos coletados")
return produtos
except Exception as e:
print(f"   ✗ Erro: {e}")
return []
def scrape_mercado_livre():
print("\n[3/3] Coletando Mercado Livre...")
produtos = []
try:
dados_simulados = [
{
: ,
: 449.00,
:
},
{
: ,
: 1199.99,
:
},
{
: ,
: 49.90,
:
}
]
for item in dados_simulados:
produtos.append({
: item[],
: item[],
: item[],
:
})
print(f"   ✓ {len(produtos)} produtos coletados")
return produtos
except Exception as e:
print(f"   ✗ Erro: {e}")
return []
def main():
print("=" * 70)
print("       COMPARADOR DE PREÇOS - WEB SCRAPING")
print("=" * 70)
banco = GerenciadorBanco(DB_CONFIG)
banco.limpar_tabela()
print("\n" + "=" * 70)
print("       COLETANDO DADOS DE 3 SITES")
print("=" * 70)
todos_produtos = []
todos_produtos.extend(scrape_kabum())
time.sleep(1)
todos_produtos.extend(scrape_amazon())
time.sleep(1)
todos_produtos.extend(scrape_mercado_livre())
print("\n" + "=" * 70)
print("       INSERINDO NO BANCO DE DADOS")
print("=" * 70)
contador = 0
for produto in todos_produtos:
if banco.inserir_produto(
produto[],
produto[],
produto[],
produto[]
):
contador += 1
print(f"\n✓ {contador} produtos inseridos com sucesso!")
print("\n" + "=" * 70)
print("       RANKING: MENOR PARA MAIOR PREÇO (ASC)")
print("=" * 70)
ranking_asc = banco.exibir_ranking()
if ranking_asc:
print(f"\n{DESC
print("-" * 80)
for row in ranking_desc:
print(f"{row[0]:<4} {row[2][:45]:<45} R$ {row[3]:<9.2f} {row[4]:<15}")
banco.fechar()
print("\n" + "=" * 70)
print("✓ PROCESSO FINALIZADO COM SUCESSO!")
print("=" * 70)
if __name__ == :
main()