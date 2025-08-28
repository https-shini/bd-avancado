<h1 align="center">Aula 03 — Manipulação Avançada de Dados (DML)</h1>

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
A **Aula 03** aprofundou os conhecimentos em manipulação de dados, indo além das consultas (`SELECT`) para focar na modificação e gestão dos registos com os comandos `UPDATE` e `DELETE`. O destaque da aula foi a introdução a técnicas avançadas para a inserção de dados, com ênfase na manipulação de **datas e horas**, utilizando funções específicas do Oracle como `TO_DATE`, `TO_TIMESTAMP`, `SYSDATE` e `CURRENT_TIMESTAMP`.

## 🔍 Conteúdo abordado
-   **Inserção com Datas e Horas:**
    -   Uso de `TO_DATE` para inserir apenas a data.
    -   Uso de `TO_TIMESTAMP` para inserir data e hora com precisão.
    -   Utilização de `SYSDATE` para registar a data e hora atuais do servidor.
    -   Aplicação de `CURRENT_TIMESTAMP AT TIME ZONE` para registos com fusos horários específicos.
-   **Inserção com Subconsultas:** Demonstração de como usar um `SELECT` dentro de um `INSERT` para obter valores dinamicamente.
-   **Consulta com Formatação de Data/Hora:** Uso da função `TO_CHAR` para exibir datas e horas em formatos legíveis (`dd/mm/yyyy`, `hh24:mi:ss`).
-   **Alteração de Dados (`UPDATE`):** Sintaxe e exemplo prático para modificar registos existentes numa tabela com base em condições.
-   **Exclusão de Dados (`DELETE`):** Comando para remover registos específicos de uma tabela utilizando a cláusula `WHERE`.

## 📎 Arquivos da Aula
-   `codigo.txt`: Script SQL completo e atualizado, contendo as novas seções (Partes 5, 6 e 7) com exemplos de manipulação de data/hora, `UPDATE` e `DELETE`.
-   `insert_update_delete_date_time.pdf`: Material de apoio com a teoria e exemplos dos comandos e funções de data/hora abordados.
-   `ExerciciosRevisaoSelect_com_respostas.docx`: Documento de referência com os 16 exercícios de `SELECT` e suas respetivas soluções.
-   `scripts_tables_inserts_portal_noticias.txt`: Script simplificado com `CREATE` e `INSERT` para exercícios focados em consultas.
