# 🌟 Revisão de Conteúdo - Laboratório de Banco de Dados Avançado

Este guia é um resumo focado nos tópicos centrais da disciplina, com ênfase nos conteúdos de programação procedural que serão o foco principal da prova (Unidades 4 a 6).

---

## 🎯 FOCO PRINCIPAL DA PROVA (Unidades 4 a 6)

| Tópico | Subtópicos Críticos | Aplicações Práticas (O que dominar) |
| :--- | :--- | :--- |
| **1. Triggers** | `BEFORE` vs `AFTER`, `FOR EACH ROW`, Variáveis de Contexto (`:NEW` e `:OLD`), `RAISE_APPLICATION_ERROR` (para impedir DML). | Implementar Auditoria (`AFTER`) e Regras de Validação (`BEFORE`). |
| **2. Procedures & Functions** | Diferença (`FUNCTION` sempre retorna valor), Tipos de Parâmetros (`IN`, `OUT`, `IN OUT`), `SELECT INTO` e `EXCEPTION` (`NO_DATA_FOUND`). | Criar funções de validação (Ex: CPF) e procedures de negócio (CRUD). |
| **3. Cursors** | Cursor Explícito, Estrutura `FOR...LOOP` com Cursor, Atributo `%NOTFOUND`. | Listagem de dados complexos e iteração sobre resultados de `SELECT` dentro de Procedures. |
| **4. Packages** | Estrutura (`SPECIFICATION` e `BODY`), Encapsulamento, Vantagens, Acesso por ponto (`NOME_PACKAGE.OBJETO`). | Agrupar lógica relacionada (Ex: `pkg_exemplo` com `insert` e `remove` de departamentos). |

---

## 📚 RESUMO DO CONTEÚDO PROGRAMÁTICO GERAL

### **I. Revisão e Fundamentos (Unidades 1 a 3)**

| Conceito | Descrição Breve | Exemplo de Aplicação |
| :--- | :--- | :--- |
| **SQL Avançado** | Comandos DDL (`CREATE`, `DROP`), DML (`INSERT`, `UPDATE`, `DELETE`), Junções (`INNER`, `RIGHT`) e Funções de Data/Hora (`SYSDATE`, `TO_CHAR`). | Inserção com `TO_TIMESTAMP` e consultas complexas (`GROUP BY`, `COUNT`). |
| **Views** | Tabelas virtuais (`CREATE OR REPLACE VIEW`) que simplificam consultas complexas, controlam acesso a dados sensíveis e abstraem a lógica. | `vw_medico_especialidade` (combina `JOIN`s), `vw_pacientes_ativos` (aplica filtro `deleted=0`). |
| **PL/SQL Básico** | Estrutura de blocos anônimos (`DECLARE`, `BEGIN`, `END`), saída com `DBMS_OUTPUT.PUT_LINE`, e controle de fluxo (`IF-ELSIF-ELSE`). | Cálculo de média e situação do aluno, geração de números aleatórios (`DBMS_RANDOM.VALUE`). |

### **II. Temas Complementares (Unidades 7 a 9)**

| Conceito | Descrição Breve | Foco para a Disciplina |
| :--- | :--- | :--- |
| **Processamento de Transações** | Define uma sequência de operações como uma unidade única de trabalho. Controlada por `COMMIT` (salva permanentemente) e `ROLLBACK` (desfaz alterações). | Propriedades ACID e comandos de controle transacional. |
| **Controle de Concorrência** | Técnicas para gerenciar o acesso simultâneo aos dados por múltiplos usuários, garantindo que as transações não interfiram umas nas outras. | Conhecimento das técnicas e a importância do isolamento. |
| **Controle de Acesso** | Criação de usuários e a gestão de permissões (`GRANT` e `REVOKE`) para limitar o acesso a objetos do banco de dados (tabelas, procedures, etc.). | Criação de usuários e a concessão/revogação de privilégios. |

---

*Este resumo foi elaborado para fins de estudo da disciplina **Laboratório de Banco de Dados Avançado** da Universidade Cruzeiro do Sul.*
