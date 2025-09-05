
~~~~sql
-- =====================================================================
-- Aula 05 - PL/SQL 
-- PARTE 1: DBMS_OUTPUT e DBMS_OUTPUT
-- Introdução e comandos
-- =====================================================================

declare
	v_nome varchar2(40) := 'Bruna'
begin
	dbms_output.put_line('Olá mundo!');
	dbms_output.put_line('Seja bem-vindo' || v_nome);
end;

---

DECLARE
    numeroAleatorio NUMBER;
BEGIN
    numeroAleatorio := TRUNC(DBMS_RANDOM.VALUE(1,11));
	DBMS_OUTPUT.PUT_LINE('Número gerado: ' || numeroAleatorio);
END;


-- =====================================================================
-- AULA 05 - PARTE 5: EXERCÍCIOS DE PL/SQL (RESOLVIDOS)
-- Blocos de código para praticar a lógica procedural no Oracle.
-- =====================================================================

-- Executando Exercício 1 de PL/SQL (Média do Aluno)...
-- Bloco para calcular a média de um aluno e exibir sua situação.
DECLARE
  -- Definição das variáveis para as notas e a média.
  v_nota1 NUMBER := 6.5;
  v_nota2 NUMBER := 5.0;
  v_media NUMBER;
BEGIN
  -- Calcula a média das duas notas.
  v_media := (v_nota1 + v_nota2) / 2;

  -- Exibe a média calculada para o usuário.
  DBMS_OUTPUT.PUT_LINE('Média do aluno: ' || v_media);

  -- Utiliza a estrutura IF/ELSIF/ELSE para determinar a situação do aluno.
  IF v_media >= 6 THEN
    DBMS_OUTPUT.PUT_LINE('Situação: Aprovado');
  ELSIF v_media >= 4.01 AND v_media <= 5.99 THEN
    DBMS_OUTPUT.PUT_LINE('Situação: Exame');
  ELSE
    DBMS_OUTPUT.PUT_LINE('Situação: Reprovado');
  END IF;
END;


-- Executando Exercício 2 de PL/SQL (Sorteio de Números)...
-- Bloco que simula um sorteio e compara com números escolhidos.
DECLARE
  -- Números que o "usuário" escolheu.
  v_num1_escolhido NUMBER := 2;
  v_num2_escolhido NUMBER := 4;
  v_num3_escolhido NUMBER := 6;

  -- Variáveis para guardar os números que serão sorteados.
  v_num1_sorteado NUMBER;
  v_num2_sorteado NUMBER;
  v_num3_sorteado NUMBER;
BEGIN
  -- Gera dois números aleatórios inteiros entre 1 e 10.
  -- DBMS_RANDOM.VALUE(min, max) gera um número decimal. A função TRUNC() o converte para inteiro.
  v_num1_sorteado := TRUNC(DBMS_RANDOM.VALUE(1, 11)); -- O limite superior (11) é exclusivo.
  v_num2_sorteado := TRUNC(DBMS_RANDOM.VALUE(1, 11));
  v_num3_sorteado := TRUNC(DBMS_RANDOM.VALUE(1, 11));

  -- Exibe os números para comparação.
  DBMS_OUTPUT.PUT_LINE('Números escolhidos: ' || v_num1_escolhido || ' e ' || v_num2_escolhido || ' e '  || v_num3_escolhido);
  DBMS_OUTPUT.PUT_LINE('Números sorteados: ' || v_num1_sorteado || ' e ' || v_num2_sorteado || ' e '  || v_num3_escolhido);


  -- Compara se AMBOS os números escolhidos são iguais aos sorteados.
  IF v_num1_escolhido = v_num1_sorteado AND v_num2_escolhido = v_num2_sorteado AND v_num3_escolhido = v_num3_sorteado THEN
    DBMS_OUTPUT.PUT_LINE('Resultado: Parabéns! Você acertou em cheio!');
  ELSE
    DBMS_OUTPUT.PUT_LINE('Resultado: Não foi desta vez. Tente novamente!');
  END IF;
END;


-- Executando Exercício 3 de PL/SQL (Cálculo de Aumento Salarial)...
-- Bloco para calcular e exibir o reajuste de salário de um funcionário.
DECLARE
  -- Definição das variáveis de entrada.
  v_nome_funcionario   VARCHAR2(100) := 'Sabrina de Souza';
  v_salario_atual      NUMBER(10, 2) := 5000.00; -- Formato com 10 dígitos no total e 2 decimais.
  v_percentual_aumento NUMBER        := 10;      -- Aumento de 10%

  -- Variável para armazenar o resultado do cálculo.
  v_novo_salario       NUMBER(10, 2);
BEGIN
  -- A lógica de cálculo do novo salário.
  v_novo_salario := v_salario_atual + (v_salario_atual * (v_percentual_aumento / 100));

  -- Exibição formatada dos resultados para o usuário.
  DBMS_OUTPUT.PUT_LINE('--- Relatório de Reajuste Salarial ---');
  DBMS_OUTPUT.PUT_LINE('Funcionário: ' || v_nome_funcionario);
  DBMS_OUTPUT.PUT_LINE('Salário Atual: R$ ' || v_salario_atual);
  DBMS_OUTPUT.PUT_LINE('Novo Salário com ' || v_percentual_aumento || '% de aumento: R$ ' || v_novo_salario);
END;
~~~~
