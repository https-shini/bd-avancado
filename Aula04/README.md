<h1 align="center">Aula 04 — Views e Abstração de Consultas</h1>

<p align="center">
  <a href="../README.md">Home</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-resumo">Resumo</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-conteúdo-abordado">Conteúdo</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-arquivos-da-aula">Arquivos</a>
</p>

## 📜 Resumo
A **Aula 04** introduz um novo estudo de caso, o agendamento de consultas para uma **clínica médica**, com o objetivo de ensinar um dos recursos mais importantes do SQL avançado: as **Views**. A aula foca em como utilizar `Views` para criar tabelas virtuais que simplificam consultas complexas, aumentam a segurança dos dados e abstraem a lógica de negócio, além de apresentar conceitos como *soft delete* e colunas de auditoria.

## 🔍 Conteúdo abordado
-   **Novo Estudo de Caso:** Modelagem e implementação de um banco de dados para uma clínica médica, com as tabelas `tbEspecialidade`, `tbMedico`, `tbPaciente` e `tbAgendaConsulta`.
-   **Conceitos de Views:**
    -   O que são `Views` (tabelas virtuais) e suas principais vantagens (simplificação, segurança, flexibilidade).
    -   Sintaxe para criação (`CREATE VIEW`), alteração (`CREATE OR REPLACE VIEW`) e exclusão (`DROP VIEW`).
-   **Técnicas Adicionais:**
    -   **Soft Delete:** Implementação da lógica de "exclusão suave" com a coluna `deleted`, que marca um registro como inativo em vez de apagá-lo.
    -   **Auditoria:** Uso de colunas como `data_criacao` e `data_alteracao` com `SYSDATE` para rastrear modificações.
-   **Exercícios Práticos:** Criação de 6 `Views` para resolver problemas comuns, como listar médicos com suas especialidades, encontrar consultas futuras e filtrar pacientes ativos.

## 📎 Arquivos da Aula
-   `CodigoFinal.md`: Script SQL completo e aprimorado, contendo a criação das tabelas, inserção de dados, a resolução de todos os exercícios de `Views` e uma seção para limpeza do ambiente.
-   `Aula04.pdf`: Material de apoio com a teoria sobre `Views`, o enunciado do novo estudo de caso e a lista de exercícios propostos.
