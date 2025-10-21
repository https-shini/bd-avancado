CREATE TABLE tbJokenpo (
idJogada NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
jogadaUsuario VARCHAR2(10) NOT NULL,
jogadaPC VARCHAR2(10) NOT NULL,
resultado VARCHAR2(20) NOT NULL,
dataJogada DATE DEFAULT SYSDATE
);
CREATE OR REPLACE PROCEDURE jogarJokenpo (
p_jogadaUsuario IN VARCHAR2
) AS
v_jogadaPC VARCHAR2(10);
v_resultado VARCHAR2(20);
v_numero NUMBER;
BEGIN
v_numero := DBMS_RANDOM.VALUE(1, 4);
IF v_numero < 2 THEN
v_jogadaPC := 'Pedra';
ELSIF v_numero < 3 THEN
v_jogadaPC := 'Papel';
ELSE
v_jogadaPC := 'Tesoura';
END IF;
IF p_jogadaUsuario = v_jogadaPC THEN
v_resultado := 'Empate';
ELSIF (p_jogadaUsuario = 'Pedra' AND v_jogadaPC = 'Tesoura') OR
(p_jogadaUsuario = 'Papel' AND v_jogadaPC = 'Pedra') OR
(p_jogadaUsuario = 'Tesoura' AND v_jogadaPC = 'Papel') THEN
v_resultado := 'Vitória do Usuário';
ELSE
v_resultado := 'Vitória do PC';
END IF;
INSERT INTO tbJokenpo (jogadaUsuario, jogadaPC, resultado)
VALUES (p_jogadaUsuario, v_jogadaPC, v_resultado);
COMMIT;
DBMS_OUTPUT.PUT_LINE('Você jogou: ' || p_jogadaUsuario);
DBMS_OUTPUT.PUT_LINE('PC jogou: ' || v_jogadaPC);
DBMS_OUTPUT.PUT_LINE('Resultado: ' || v_resultado);
DBMS_OUTPUT.PUT_LINE('
END;
/
CREATE OR REPLACE VIEW vwEstatisticasJokenpo AS
SELECT
COUNT(*) AS "Total de Jogadas",
SUM(CASE WHEN resultado = 'Vitória do Usuário' THEN 1 ELSE 0 END) AS "Vitórias do Usuário",
SUM(CASE WHEN resultado = 'Vitória do PC' THEN 1 ELSE 0 END) AS "Vitórias do PC",
SUM(CASE WHEN resultado = 'Empate' THEN 1 ELSE 0 END) AS "Empates"
FROM tbJokenpo;
CREATE OR REPLACE VIEW vwHistoricoJokenpo AS
SELECT
idJogada AS "ID",
jogadaUsuario AS "Jogada Usuário",
jogadaPC AS "Jogada PC",
resultado AS "Resultado",
TO_CHAR(dataJogada, 'DD/MM/YYYY HH24:MI:SS') AS "Data/Hora"
FROM tbJokenpo
ORDER BY idJogada DESC;
SET SERVEROUTPUT ON;
BEGIN
jogarJokenpo('Pedra');
jogarJokenpo('Papel');
jogarJokenpo('Tesoura');
jogarJokenpo('Pedra');
jogarJokenpo('Papel');
END;
/
SELECT * FROM vwHistoricoJokenpo;
SELECT * FROM vwEstatisticasJokenpo;
SELECT
resultado,
COUNT(*) AS total,
ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tbJokenpo), 2) AS percentual
FROM tbJokenpo
GROUP BY resultado
ORDER BY total DESC;