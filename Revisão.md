# Laboratório de Banco de Dados Avançado
## Guia Teórico Completo - Análise e Revisão Geral

**Professor:** Allan Vidal (allan@cruzeirodosul.edu.br)  
**Disciplina:** Análise e Desenvolvimento de Sistemas / Ciência da Computação  
**Plataforma:** Oracle Live SQL (https://livesql.oracle.com/)

---

## 📚 ESTRUTURA GERAL DA DISCIPLINA

### Ementa e Objetivos

A disciplina foca em **programação avançada de bases de dados relacionais**, com ênfase em SQL avançada e procedimentos armazenados no banco de dados. O objetivo é capacitar o aluno a criar soluções robustas, eficientes e modulares diretamente no SGBD Oracle.

### Divisão por Unidades

**UNIDADES 1-3: Fundamentos e Revisão**
- Revisão de SQL básico e modelagem
- Views (tabelas virtuais)
- Introdução ao PL/SQL
- Estruturas de controle e arrays

**UNIDADES 4-6: Programação Armazenada**
- Stored Procedures
- Functions
- Packages (agrupamento de objetos)
- Triggers (automação)

**UNIDADES 7-9: Transações e Segurança**
- Processamento de transações
- Controle de concorrência
- Controle de acesso e privilégios

### Sistema de Avaliação

- **A1** (Prova Regimental): 5,0 pontos
- **A2** (Atividades diversas): 5,0 pontos
- **Aprovação direta:** Soma ≥ 6,0
- **Avaliação Final:** Substitui a menor nota se houver possibilidade de aprovação

---

## 🗄️ PARTE 1: FUNDAMENTOS SQL E MODELAGEM

### Modelagem de Dados

A disciplina trabalha com um **estudo de caso principal**: um portal de notícias online que permite publicação de conteúdos, comentários de leitores e sistema de avaliações.

#### Conceitos de Modelagem

**Entidades Principais:**
- Representam objetos do mundo real (Jornalista, Notícia, Categoria, Leitor, Comentário)
- Cada entidade possui atributos que descrevem suas características
- Relacionamentos definem como as entidades se conectam

**Tipos de Relacionamento:**
- **1:1** (um para um) - Ex: Pessoa → Carteira de Identidade
- **1:N** (um para muitos) - Ex: Categoria → Notícias
- **N:N** (muitos para muitos) - Ex: Jornalista ↔ Notícias (requer tabela associativa)

**Chaves:**
- **Primary Key (PK):** Identificador único de cada registro
- **Foreign Key (FK):** Referência a uma PK de outra tabela
- **Constraints:** Regras que garantem integridade (NOT NULL, UNIQUE, CHECK)

### SQL Essencial

#### Linguagem de Definição de Dados (DDL)

**CREATE:** Criação de objetos (tabelas, sequences, índices)
- Define estrutura, tipos de dados e constraints
- Estabelece relacionamentos via Foreign Keys

**ALTER:** Modificação de estruturas existentes
- Adicionar/remover colunas
- Modificar tipos de dados
- Adicionar/remover constraints

**DROP:** Exclusão de objetos
- Remove permanentemente estruturas do banco
- Pode exigir CASCADE para remover dependências

#### Linguagem de Manipulação de Dados (DML)

**INSERT:** Inserção de novos registros
- Pode usar VALUES para valores diretos
- Pode usar SELECT para inserir resultados de consultas

**UPDATE:** Alteração de registros existentes
- WHERE define quais registros serão alterados
- Sem WHERE, altera TODOS os registros (perigoso!)

**DELETE:** Exclusão de registros
- WHERE define quais registros serão excluídos
- Diferente de TRUNCATE (que é DDL e mais rápido)

**SELECT:** Consulta de dados
- WHERE: filtros
- ORDER BY: ordenação
- GROUP BY: agrupamento
- HAVING: filtro após agrupamento
- JOINs: combinar tabelas

#### Tipos de JOIN

**INNER JOIN:** Retorna apenas registros que têm correspondência em ambas as tabelas

**LEFT JOIN:** Retorna todos da tabela esquerda, mesmo sem correspondência à direita

**RIGHT JOIN:** Retorna todos da tabela direita, mesmo sem correspondência à esquerda

**FULL OUTER JOIN:** Retorna todos os registros de ambas as tabelas

**CROSS JOIN:** Produto cartesiano (todas as combinações possíveis)

### Trabalhando com Datas

O Oracle possui tipos específicos para data e hora:

**DATE:** Armazena data e hora (sem frações de segundo)

**TIMESTAMP:** Armazena data, hora e frações de segundo

**SYSDATE:** Função que retorna data/hora atual do servidor

**CURRENT_TIMESTAMP:** Retorna timestamp atual com timezone

**Operações Aritméticas:**
- Adicionar/subtrair dias: SYSDATE + 1, SYSDATE - 7
- Diferença entre datas resulta em número de dias
- MONTHS_BETWEEN: diferença em meses

**Formatação:**
- TO_CHAR: converte data para string com formato
- TO_DATE: converte string para data
- EXTRACT: extrai componentes (YEAR, MONTH, DAY, HOUR)

---

## 👁️ PARTE 2: VIEWS (VISÕES)

### Conceito Fundamental

Views são **tabelas virtuais** que não armazenam dados fisicamente, mas representam o resultado de uma consulta SQL predefinida. Funcionam como uma "janela" para os dados reais.

### Características

**Não armazenam dados:** Sempre consultam as tabelas base em tempo real

**Atualizadas automaticamente:** Refletem mudanças nas tabelas base

**Podem ser consultadas como tabelas:** Usadas em SELECT, WHERE, JOIN

**Podem ter restrições:** Nem sempre permitem INSERT/UPDATE/DELETE

### Vantagens Estratégicas

**Simplificação:**
- Transforma consultas complexas em objetos simples
- Usuários acessam dados complexos através de interface simples
- Reduz repetição de código SQL complexo

**Segurança:**
- Esconde colunas sensíveis dos usuários
- Permite acesso granular (mostrar apenas colunas específicas)
- Pode filtrar linhas baseado em permissões

**Abstração:**
- Isola aplicação da estrutura física do banco
- Mudanças nas tabelas base não afetam a aplicação
- Facilita manutenção e evolução do schema

**Organização:**
- Cria camadas lógicas sobre dados físicos
- Facilita compreensão do modelo de dados
- Documenta consultas complexas importantes

### Limitações

**DML Restrito:**
- INSERT/UPDATE/DELETE só funcionam em views simples
- Views com JOIN, DISTINCT, GROUP BY geralmente são somente leitura
- Views devem incluir todas as colunas obrigatórias da tabela base

**Performance:**
- Views complexas podem ser lentas
- Não têm índices próprios (usam índices das tabelas base)
- Views aninhadas podem degradar performance

**Manutenção:**
- Multiplicam objetos no banco de dados
- Podem criar dependências complexas
- Documentação é essencial para entender propósito

### Tipos de Views

**Views Simples:**
- Baseadas em uma única tabela
- Sem funções de grupo, DISTINCT, JOIN
- Permitem DML (INSERT/UPDATE/DELETE)

**Views Complexas:**
- Baseadas em múltiplas tabelas
- Com JOINs, funções de grupo, subconsultas
- Geralmente somente leitura

**Views Materializadas:**
- Armazenam dados fisicamente (cache)
- Precisam ser atualizadas/refreshed
- Melhor performance em consultas pesadas

### Casos de Uso Comuns

**Relatórios:** Views que agregam dados para dashboards

**Segurança:** Views que filtram dados sensíveis por departamento/usuário

**Compatibilidade:** Manter interface antiga após reestruturação do banco

**Simplificação:** Facilitar acesso a dados denormalizados

---

## 💻 PARTE 3: PL/SQL - FUNDAMENTOS

### O que é PL/SQL?

**PL/SQL** (Procedural Language/Structured Query Language) é a linguagem procedural da Oracle que **estende o SQL** adicionando estruturas de programação:

- Variáveis e constantes
- Estruturas condicionais (IF, CASE)
- Estruturas de repetição (LOOP, WHILE, FOR)
- Tratamento de exceções
- Modularização (procedures, functions, packages)

### Filosofia e Propósito

**Por que PL/SQL?**

SQL é uma linguagem **declarativa** (você diz O QUE quer, não COMO obter). PL/SQL adiciona capacidades **procedurais** (você define COMO processar), permitindo:

- Lógica de negócio complexa no banco
- Processamento batch eficiente
- Redução de tráfego entre aplicação e banco
- Centralização de regras de negócio
- Reutilização de código

### Vantagens

**Integração Perfeita com SQL:**
- Comandos SQL nativos dentro do código
- Sem conversão de tipos ou impedância
- Performance otimizada

**Processamento no Servidor:**
- Menos tráfego de rede
- Processamento próximo aos dados
- Melhor performance em operações massivas

**Segurança:**
- Lógica de negócio protegida no banco
- Controle de acesso granular
- Auditoria facilitada

**Reutilização:**
- Código compartilhado entre aplicações
- Manutenção centralizada
- Versionamento no banco

### Desvantagens

**Dependência de Plataforma:**
- PL/SQL é específico do Oracle
- Migração para outros SGBDs é complexa
- Vendor lock-in

**Curva de Aprendizado:**
- Mais complexo que SQL puro
- Requer conhecimento de programação procedural
- Debugging pode ser desafiador

**Manutenção:**
- Lógica distribuída entre aplicação e banco
- Pode criar acoplamento forte
- Versionamento requer estratégia específica

### Estrutura de Blocos

PL/SQL trabalha com **blocos** que podem ser anônimos ou nomeados (procedures, functions).

**Seções de um Bloco:**

**DECLARE (opcional):**
- Declaração de variáveis
- Declaração de cursores
- Declaração de exceções customizadas
- Declaração de tipos

**BEGIN (obrigatório):**
- Código executável
- Comandos SQL e PL/SQL
- Lógica de negócio

**EXCEPTION (opcional):**
- Tratamento de erros
- Logging de exceções
- Recuperação de falhas

### Variáveis e Tipos de Dados

**Tipos Escalares:**
- NUMBER: numérico (inteiro ou decimal)
- VARCHAR2: string de tamanho variável
- CHAR: string de tamanho fixo
- DATE: data e hora
- TIMESTAMP: data e hora com precisão
- BOOLEAN: TRUE, FALSE, NULL

**Tipos de Referência:**
- %TYPE: mesmo tipo de uma coluna
- %ROWTYPE: estrutura de uma linha completa

**Vantagens de %TYPE:**
- Sincronização automática com tabela
- Manutenção facilitada
- Menos propensão a erros

### Estruturas Condicionais

**IF-THEN:**
- Execução condicional simples
- Sem alternativa para falso

**IF-THEN-ELSE:**
- Duas alternativas (verdadeiro/falso)
- Útil para decisões binárias

**IF-THEN-ELSIF-ELSE:**
- Múltiplas condições encadeadas
- Primeira condição verdadeira é executada
- ELSE captura todos os outros casos

**CASE:**
- Alternativa mais elegante ao IF encadeado
- Pode ser usado como expressão ou statement
- Mais legível para múltiplas condições

### Estruturas de Repetição

**LOOP Básico:**
- Loop infinito até EXIT
- Controle manual de saída
- Flexível mas requer cuidado

**WHILE:**
- Testa condição antes de executar
- Pode não executar nenhuma vez
- Ideal quando não se sabe quantas iterações

**FOR:**
- Número definido de iterações
- Variável de controle automática
- Pode ser crescente ou decrescente (REVERSE)
- Mais seguro que LOOP básico

### Arrays e Coleções

PL/SQL oferece três tipos de coleções:

**Tabelas Associativas (Index-By Tables):**
- Array associativo (como hash map)
- Índice pode ser numérico ou string
- Somente em memória
- Tamanho dinâmico
- Mais eficiente para acesso direto

**VARRAYs (Variable-Size Arrays):**
- Array de tamanho fixo (definido na criação)
- Índice sempre numérico e contíguo
- Pode ser armazenado no banco
- Densidade obrigatória (sem buracos)

**Nested Tables:**
- Array de tamanho dinâmico
- Pode ter buracos (elementos deletados)
- Pode ser armazenado no banco
- Mais flexível que VARRAY

### Cursores

**Conceito:**
Cursor é um **ponteiro para o resultado de uma consulta SQL**, permitindo processar linha por linha.

**Cursor Implícito:**
- Criado automaticamente pelo Oracle
- Para comandos SQL simples (SELECT INTO, UPDATE, DELETE)
- Gerenciamento automático

**Cursor Explícito:**
- Declarado pelo programador
- Controle total sobre abertura, fetch e fechamento
- Necessário para processar múltiplas linhas
- Mais eficiente em grandes volumes

**Ciclo de Vida do Cursor:**
1. **DECLARE:** Declarar o cursor
2. **OPEN:** Abrir (executar a query)
3. **FETCH:** Buscar próxima linha
4. **CLOSE:** Fechar e liberar recursos

**Atributos de Cursor:**
- %FOUND: TRUE se última busca retornou dados
- %NOTFOUND: TRUE se não retornou dados
- %ROWCOUNT: número de linhas processadas
- %ISOPEN: TRUE se cursor está aberto

**Cursor FOR Loop:**
- Simplificação do cursor explícito
- Gerenciamento automático (open, fetch, close)
- Código mais limpo e seguro

---

## 📦 PARTE 4: STORED PROCEDURES

### Conceito e Propósito

**Stored Procedures** são **subprogramas PL/SQL armazenados permanentemente no banco de dados**. São como "funções" que podem executar lógica complexa, mas não necessariamente retornam um valor.

### Por que Usar Procedures?

**Reaproveitamento de Código:**
- Escrever uma vez, usar em vários lugares
- Evita duplicação de lógica
- Facilita padronização
- Exemplo: validação de CPF usada em múltiplos módulos

**Rapidez:**
- Código pré-compilado no banco
- Acesso direto sem chamadas externas
- Oracle otimiza automaticamente
- Cache de plano de execução

**Controle de Alterações:**
- Código centralizado em um único lugar
- Mudanças refletem automaticamente em todas as aplicações
- Versionamento facilitado
- Menor risco de inconsistências

**Controle de Acesso:**
- Permissões granulares por procedure
- Usuários podem executar sem acesso direto às tabelas
- Auditoria de quem executa o quê
- Segurança em camadas

**Modularização:**
- Organização em packages
- Separação de responsabilidades
- Código mais legível e manutenível
- Facilita trabalho em equipe

### Diferença: Procedure vs Function

| Característica | Procedure | Function |
|----------------|-----------|----------|
| **Retorno** | Opcional (via OUT) | Obrigatório (RETURN) |
| **DML** | Permitido | Proibido (apenas SELECT) |
| **Uso em SELECT** | Não | Sim |
| **Objetivo** | Executar ações | Calcular/retornar valor |
| **Parâmetros OUT** | Sim | Raramente |

### Parâmetros

**IN (Entrada - padrão):**
- Passa valores PARA dentro da procedure
- Somente leitura dentro da procedure
- Não pode ser modificado
- Se não especificar, assume IN

**OUT (Saída):**
- Retorna valores PARA FORA da procedure
- Somente escrita dentro da procedure
- Não pode ser lido inicialmente
- Usado para retornar múltiplos valores

**IN OUT (Entrada e Saída):**
- Passa valor para dentro E retorna para fora
- Pode ser lido e modificado
- Útil para transformações
- Menos comum, use com cuidado

### Quando Usar Procedures?

**Operações CRUD:**
- Inserção com validações complexas
- Atualização com regras de negócio
- Exclusão lógica (marcar como inativo)
- Consultas com formatação específica

**Processos Batch:**
- Importação de dados
- Cálculos em massa
- Limpeza de dados antigos
- Consolidação de informações

**Regras de Negócio:**
- Validações complexas
- Cálculos financeiros
- Aplicação de políticas
- Workflows

**Integrações:**
- Sincronização entre sistemas
- Processamento de filas
- Comunicação com APIs externas

### Ciclo de Vida

**Criação:**
- CREATE PROCEDURE ou CREATE OR REPLACE
- Compilação automática
- Armazenada no banco

**Execução:**
- EXEC procedure_name
- BEGIN procedure_name; END;
- Chamada de outra procedure/function

**Alteração:**
- CREATE OR REPLACE (recompila)
- ALTER PROCEDURE COMPILE (apenas recompila)

**Exclusão:**
- DROP PROCEDURE

**Consulta:**
- USER_OBJECTS: informações gerais
- USER_SOURCE: código fonte
- DESCRIBE: assinatura (parâmetros)

### Best Practices

**Nomenclatura:**
- Use prefixo: proc_ ou sp_
- Nome descritivo da ação: proc_inserir_cliente
- Consistência no projeto

**Documentação:**
- Comentários explicando propósito
- Descrever parâmetros
- Exemplos de uso

**Tratamento de Erros:**
- EXCEPTION em todas as procedures
- ROLLBACK em caso de erro
- Mensagens de erro claras
- Log de erros críticos

**Transações:**
- COMMIT apenas em sucesso
- SAVEPOINT para operações complexas
- ROLLBACK em exceções

**Validações:**
- Verificar existência de registros
- Validar formatos de dados
- Checar permissões
- Mensagens amigáveis

---

## 🔧 PARTE 5: FUNCTIONS

### Conceito Fundamental

**Functions** são subprogramas que **SEMPRE retornam um valor**. A diferença crucial para procedures é que functions são projetadas para **calcular e retornar**, não para executar ações.

### Filosofia das Functions

Functions seguem o paradigma de **programação funcional**:

- Recebem entrada
- Processam
- Retornam saída
- Idealmente sem efeitos colaterais (sem DML)

**Analogia:** Functions são como fórmulas do Excel - você passa valores, ela retorna um resultado.

### Restrições Importantes

**NÃO PODE:**
- INSERT, UPDATE, DELETE (comandos DML)
- COMMIT, ROLLBACK (controle de transação)
- DDL (CREATE, ALTER, DROP)

**PODE:**
- SELECT (consultar dados)
- Cálculos e transformações
- Lógica condicional
- Processamento de strings/datas

**Por quê essas restrições?**
Functions podem ser chamadas dentro de SELECT, e permitir DML causaria efeitos colaterais imprevisíveis durante consultas.

### Retorno de Valores

**RETURN é obrigatório:**
- Deve haver pelo menos um RETURN no código
- Tipo de retorno deve ser especificado
- Pode haver múltiplos RETURNs (diferentes caminhos)

**Tipos de Retorno Comuns:**
- NUMBER: cálculos numéricos
- VARCHAR2: formatações, concatenações
- DATE/TIMESTAMP: manipulação de datas
- BOOLEAN: validações (apenas em PL/SQL, não em SQL)

### Uso em Consultas SQL

Grande vantagem das functions: podem ser usadas em SELECT, WHERE, ORDER BY, etc.

**Exemplo conceitual:**
- SELECT nome, func_calcular_idade(data_nascimento) FROM clientes
- WHERE func_validar_email(email) = 'VALIDO'
- ORDER BY func_calcular_score(id_cliente) DESC

### Tipos de Functions

**Functions de Cálculo:**
- Retornam valores numéricos
- Exemplo: calcular desconto, juros, comissão, idade

**Functions de Formatação:**
- Retornam strings formatadas
- Exemplo: formatar CPF, telefone, nome completo

**Functions de Validação:**
- Retornam TRUE/FALSE ou VARCHAR2 ('VALIDO'/'INVALIDO')
- Exemplo: validar email, CPF, senha forte

**Functions de Transformação:**
- Convertem dados de um formato para outro
- Exemplo: data para string customizada, número para texto

**Functions de Consulta:**
- Retornam dados do banco baseado em parâmetros
- Exemplo: buscar último ID inserido, contar registros com filtro

### Functions vs Procedures: Quando Usar?

**Use FUNCTION quando:**
- Precisa retornar UM valor
- Vai usar em SELECT
- É uma operação de consulta/cálculo
- Não precisa modificar dados
- Exemplo: calcular idade, formatar CPF, validar email

**Use PROCEDURE quando:**
- Precisa executar AÇÕES
- Vai modificar dados (INSERT/UPDATE/DELETE)
- Precisa retornar múltiplos valores (OUT)
- É um processo de negócio
- Exemplo: cadastrar cliente, processar pedido, gerar relatório

### Performance

**Cuidados:**
- Functions em WHERE podem degradar performance
- Function chamada para cada linha do resultado
- Evite SELECT dentro de function chamada em loop
- Cache resultados quando possível

**Otimização:**
- Use deterministic quando aplicável (resultado sempre igual para mesma entrada)
- Minimize lógica dentro da function
- Use índices nas tabelas consultadas
- Considere materializar resultados para grandes volumes

### Composição de Functions

Functions podem chamar outras functions, criando hierarquia:

**Exemplo conceitual:**
- func_validar_cadastro chama:
  - func_validar_nome
  - func_validar_email
  - func_validar_telefone

**Vantagens:**
- Modularização
- Reutilização
- Testes isolados
- Manutenção facilitada

### Integration com Procedures

Pattern comum: **Procedures usam Functions para validações**

**Fluxo típico:**
1. Procedure recebe dados
2. Chama functions de validação
3. Se todas retornam OK, executa INSERT/UPDATE
4. Se alguma falha, retorna erro

Isso separa responsabilidades:
- Functions: validação (pura, sem efeitos colaterais)
- Procedures: ação (modifica dados)

---

## 📚 PARTE 6: PACKAGES

### Conceito e Arquitetura

**Package** é um **container que agrupa procedures, functions, variáveis, cursores e tipos relacionados**. É o mecanismo de modularização mais poderoso do PL/SQL.

**Analogia:** Pense num package como uma "classe" em POO ou um "módulo" em outras linguagens.

### Estrutura Dual

Todo package completo tem DUAS partes:

**SPECIFICATION (Interface Pública):**
- Define O QUE está disponível
- Declara assinaturas de procedures/functions
- Variáveis e constantes públicas
- Cursores públicos
- É o "contrato" do package

**BODY (Implementação):**
- Define COMO funciona
- Implementação das procedures/functions
- Código privado (não acessível externamente)
- Variáveis e procedures privadas

**Regra importante:** Pode existir SPEC sem BODY, mas nunca BODY sem SPEC.

### Por Que Usar Packages?

**Encapsulamento:**
- Esconde detalhes de implementação
- Expõe apenas interface necessária
- Protege código interno
- Facilita mudanças sem quebrar dependências

**Organização:**
- Agrupa funcionalidades relacionadas
- Estrutura lógica do código
- Facilita navegação e compreensão
- Documenta arquitetura

**Namespace:**
- Evita conflitos de nomes
- package1.inserir vs package2.inserir
- Contexto claro de cada objeto

**Performance:**
- Carregado uma vez na memória
- Compartilhado entre sessões
- Variáveis de package mantêm estado na sessão
- Plano de execução otimizado

**Modularização:**
- Separação de responsabilidades
- Trabalho em equipe facilitado
- Testes isolados
- Substituição de implementação

### Elementos de um Package

**Na SPECIFICATION podem ter:**
- Declarações de procedures e functions
- Variáveis públicas (compartilhadas na sessão)
- Constantes públicas
- Cursores públicos
- Tipos customizados (TYPE)
- Exceções customizadas

**No BODY podem ter:**
- Implementação de tudo declarado no SPEC
- Procedures e functions PRIVADAS (não no SPEC)
- Variáveis privadas
- Código de inicialização (executado uma vez)

### Visibilidade (Público vs Privado)

**Público (no SPEC):**
- Acessível de fora: package_name.objeto
- Parte do contrato
- Mudanças afetam dependentes

**Privado (só no BODY):**
- Acessível apenas dentro do package
- Detalhes de implementação
- Pode mudar sem afetar externos
- Segurança e encapsulamento

### Patterns Comuns

**Package de Entidade:**
- Agrupa todas operações de uma tabela
- INSERT, UPDATE, DELETE, SELECT da entidade
- Exemplo: pkg_cliente, pkg_produto

**Package de Domínio:**
- Funcionalidades de uma área de negócio
- Exemplo: pkg_financeiro, pkg_vendas

**Package Utilitário:**
- Funções genéricas reutilizáveis
- Exemplo: pkg_utils (formatações, validações)

**Package de Constantes:**
- Apenas SPEC com constantes
- Centraliza valores mágicos
- Facilita manutenção

### Ciclo de Vida

**Compilação:**
1. Compilar SPEC primeiro
2. Depois compilar BODY
3. Mudança no SPEC invalida BODY
4. Mudança no BODY não invalida SPEC

**Invalidação:**
- Dependências são automaticamente invalidadas
- Recompilação automática no próximo uso
- Ou manual: ALTER PACKAGE COMPILE

**Estado:**
- Variáveis de package mantêm valor durante sessão
- Resetam quando sessão termina
- Útil para caching e controle de estado

### Vantagens Estratégicas

**Manutenção:**
- Mudanças localizadas
- Menos risco de quebrar código
- Versionamento mais claro

**Segurança:**
- Controle granular de acesso
- GRANT EXECUTE no package, não nas tabelas
- Usuários executam sem ver implementação

**Performance:**
- Menos parsing
- Plano de execução reutilizado
- Menos overhead de chamadas

**Arquitetura:**
- Camadas bem definidas
- Separação de apresentação/lógica/dados
- Facilita refatoração

---

## ⚡ PARTE 7: TRIGGERS

### Conceito e Filosofia

**Trigger** é um **bloco PL/SQL que dispara AUTOMATICAMENTE** em resposta a eventos específicos no banco de dados. É programação **reativa** ao invés de imperativa.

**Analogia:** Triggers são como "alarmes" ou "hooks" - você configura uma vez, e eles agem sozinhos quando algo acontece.

### Filosofia do Uso

Triggers devem ser usados para:
- **Automação:** Ações que SEMPRE devem ocorrer
- **Consistência:** Garantir regras sem depender da aplicação
- **Auditoria:** Rastrear mudanças automaticamente
- **Validações:** Impor restrições complexas

**Cuidado:** Não abuse de triggers - podem criar "lógica invisível" difícil de debugar.

### Tipos de Triggers

**Triggers de DML (Banco de Dados):**
- Disparados por INSERT, UPDATE, DELETE
- Operam em tabelas específicas
- Podem ser BEFORE ou AFTER
- Podem ser por statement ou por linha (FOR EACH ROW)

**Triggers de Sistema:**
- Disparados por eventos do banco
- LOGON, LOGOFF, STARTUP, SHUTDOWN
- DDL: CREATE, ALTER, DROP
- Usados principalmente por DBAs

### BEFORE vs AFTER

**BEFORE (Antes):**
- Executado ANTES da operação
- Dados ainda não commitados
- Pode MODIFICAR valores (:NEW)
- Pode CANCELAR operação (RAISE_APPLICATION_ERROR)
- **Uso:** Validações, ajustes de valores, impedir operações

**AFTER (Depois):**
- Executado APÓS a operação
- Dados já commitados no buffer (mas não no disco até COMMIT)
- NÃO pode modificar valores
- Pode fazer ações complementares
- **Uso:** Logs, auditoria, notificações, cascata

### Statement vs Row Level

**Statement Level (padrão):**
- Executa UMA vez por comando SQL
- Mesmo que afete múltiplas linhas
- Sem acesso a :NEW e :OLD
- **Uso:** Validações gerais, controle de horário

**Row Level (FOR EACH ROW):**
- Executa para CADA linha afetada
- Acesso a :NEW e :OLD
- Pode ser pesado em operações massivas
- **Uso:** Logs detalhados, cálculos por linha
