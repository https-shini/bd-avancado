<h1 align="center">💾 Banco de Dados Avançado</h1>

<p align="center">
  <a href="#-sobre-a-disciplina">Sobre</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-conteúdo-programático">Conteúdo</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-aulas-e-projetos--laboratório-de-banco-de-dados">Aulas</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-licença">Licença</a>
</p>

## 📖 Sobre a disciplina
A disciplina **Laboratório de Banco de Dados Avançado** aprofunda os conceitos de bancos de dados relacionais, com foco em SQL avançado, PL/SQL e recursos como *Views*, *Stored Procedures*, *Packages*, *Triggers* e controle de transações.
O objetivo é capacitar o aluno a projetar, implementar e otimizar soluções de banco de dados, relacionando teoria e prática para aplicações reais.

### 🎯 Objetivos de aprendizagem
- **Cognitivos:** desenvolver conhecimentos práticos em bancos de dados relacionais e variações da linguagem SQL.
- **Habilidades:** projetar, implementar e manter soluções que utilizem recursos avançados de bancos de dados.
- **Atitudes:** compreender a importância da integração entre teoria e prática no desenvolvimento de sistemas.

**Professor:** Me. Allan Vidal <br>
**Curso:** Ciência da Computação – Universidade Cruzeiro do Sul

---

## 📚 Conteúdo programático
1.  **Unidades 1 a 3**
    -   Revisão SQL básico e avançado
    -   Views (fundamentos, especificação, implementação e atualização)
    -   PL/SQL (introdução e comandos)

2.  **Unidades 4 a 6**
    -   Stored Procedures e Packages
    -   Consultas complexas
    -   Triggers (definição, codificação e restrições)

3.  **Unidades 7 a 9**
    -   Processamento e controle de transações
    -   Controle de concorrência
    -   Controle de acesso, criação de usuários e privilégios

---

## 📊 Aulas e Projetos — Laboratório de Banco de Dados

### 📝 Aula 01 — Estudo de Caso: Modelagem do Portal de Notícias
A **Aula 01** apresentou um estudo de caso para o desenvolvimento de um banco de dados de um **portal de notícias online**. Foram definidos requisitos como cadastro de jornalistas, leitores, notícias, categorias, mídias, comentários, avaliações e favoritos. O desafio consistiu em identificar entidades, listar atributos e estabelecer relacionamentos, resultando em um **Modelo Entidade-Relacionamento (MER)** e em um **script SQL** inicial de implementação.

👉 [Acessar o conteúdo completo da Aula 01.](Aula01/README.md)

### 📝 Aula 02 — Implementação e Consultas SQL
A **Aula 02** focou na implementação prática do banco de dados do portal de notícias. Foram criadas tabelas com `CREATE TABLE`, inseridos dados de exemplo com `INSERT` e executadas consultas SQL para revisar conceitos fundamentais, como seleção, filtragem, ordenação e agregação de dados.

👉 [Acessar o conteúdo completo da Aula 02.](Aula02/README.md)

### 📝 Aula 03 — Manipulação Avançada de Dados (DML)
Na **Aula 03**, os estudos se aprofundaram na **manipulação de dados**. O conteúdo abordou os comandos `UPDATE` e `DELETE`, além de técnicas avançadas para inserção de dados, com destaque para a manipulação de **datas e horas**, utilizando funções como `TO_DATE`, `TO_TIMESTAMP`, `SYSDATE` e `CURRENT_TIMESTAMP`.

👉 [Acessar o conteúdo completo da Aula 03.](Aula03/README.md)

### 📝 Aula 04 — Views e Abstração de Consultas
A **Aula 04** introduziu um novo estudo de caso, desta vez sobre uma **clínica médica**, para apresentar o conceito de `Views`. O foco foi mostrar como as tabelas virtuais podem simplificar consultas complexas, proteger dados sensíveis e abstrair a lógica de acesso às informações, além de introduzir o conceito de *soft delete*.

👉 [Acessar o conteúdo completo da Aula 04.](Aula04/README.md)

### 📝 Aula 05 — Introdução ao PL/SQL e Comandos de Fluxo
A **Aula 05** introduziu o universo da programação procedural com **PL/SQL**. O foco principal foi na estrutura básica de um bloco anônimo (`DECLARE`, `BEGIN`, `END`) e no uso do pacote `DBMS_OUTPUT.PUT_LINE` para exibição de mensagens. Foram exploradas as estruturas de controle de fluxo e os comandos condicionais `IF-ELSIF-ELSE` para a tomada de decisões, aplicando lógicas como a determinação da situação de um aluno por média ou simulações de sorteio de números aleatórios.

### 📝 Aula 07 — Lógica de Programação: CASE WHEN, Laços e Arrays
Na **Aula 07**, aprofundamos em técnicas de programação procedural e SQL avançado. Foi introduzida a expressão `CASE WHEN` para realizar lógica condicional diretamente em consultas `SELECT`, permitindo a classificação de dados, como o status de estoque de um produto (e.g., `SEM ESTOQUE`, `DISPONÍVEL`). Além disso, foram estudados os laços de repetição (`WHILE`, `LOOP`, `FOR`) e as estruturas de dados **Arrays** (como tabelas associativas e `VARRAYs`) em blocos PL/SQL para manipulação eficiente e inserção de dados em lote.

### 📝 Aula 08 & 09 — Stored Procedures, Functions e Cursores
As aulas finais focaram em programas armazenados para persistir a lógica de negócio, introduzindo **Stored Procedures** e **Functions**. Foi detalhada a criação e execução desses subprogramas, enfatizando que as *Functions* sempre devem retornar um valor. Aprendemos a utilizar **parâmetros** para comunicação com esses programas (`IN` para entrada e `OUT` para saída) e introduzimos o conceito de **Cursores** explícitos para permitir a iteração e a manipulação de linhas de dados retornadas por um `SELECT` dentro de um bloco PL/SQL ou Procedure.

---

## 📄 Licença

Distribuído sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais informações.

---

> *Este repositório é dedicado ao registro completo e organizado das atividades, estudos, materiais e práticas desenvolvidas na disciplina de Banco de Dados Avançado, servindo como recurso de consulta e suporte para o aprendizado contínuo.*
