<h1 align="center">Aula 01 — Estudo de Caso: Portal de Notícias Web</h1>

<p align="center">
  <a href="https://github.com/https-shini/bd-avancado" >Home</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-resumo">Resumo</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-conteúdo-abordado">Conteúdo</a>
    &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-arquivos-da-aula-01">Arquivos</a>
    &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/https-shini/bd-avancado/blob/main/Aula01/exemplo.md">Exemplo</a>
      &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/https-shini/bd-avancado/blob/main/Aula01/atividade.md">Atividade</a>
</p>

## 📜 Resumo
A primeira aula introduziu o estudo de caso que será a base para o desenvolvimento prático da disciplina: a criação de um banco de dados para um **portal de notícias online**. O foco foi a aplicação dos conceitos de modelagem de dados para traduzir os requisitos de negócio em uma estrutura de banco de dados relacional, resultando na criação do Modelo Entidade-Relacionamento (MER).

## 📚 Conteúdo
- **Análise de Requisitos:** Interpretação das necessidades do sistema, como cadastro de jornalistas, notícias, categorias, leitores e interações (comentários, avaliações).
- **Modelagem Conceitual:**
    - Identificação das entidades principais (`JORNALISTA`, `NOTICIA`, `CATEGORIA`, `LEITOR`, etc.).
    - Definição dos atributos para cada entidade.
    - Estabelecimento dos relacionamentos e suas cardinalidades (1:1, 1:N, N:N).
- **Ferramentas:** Apresentação do Oracle Live SQL como ambiente para os exercícios práticos.

## 📎 Arquivos da Aula 01  
- `Aula_01_ementa.pptx` — Ementa da disciplina e objetivos  
- `Estudo_caso_portal_noticias.pptx` — Requisitos e enunciado da atividade  
- `Resp_Ex123.pptx` — Respostas iniciais da modelagem
  
## 🗂️ Materiais
- **[Apresentação da Disciplina](Aula_01_ementa.pptx):** Ementa, objetivos e conteúdo programático.
- **[Enunciado do Estudo de Caso](Estudo_caso_portal_noticias.pptx):** Requisitos detalhados do portal de notícias.
- **[Detalhamento da Atividade](atividade.md):** Resolução da modelagem, com a lista completa de entidades, atributos e relacionamentos.
- **[Exemplo de Script SQL](exemplo.md):** Guia prático de como criar e popular tabelas com um exemplo simples de usuários e pedidos.

## 📜 Enunciado da Atividade

Uma empresa de mídia digital está desenvolvendo um portal de notícias online com o objetivo de publicar conteúdos informativos em diversas áreas, como política, esportes, tecnologia, cultura e economia.

Para isso, é necessário projetar um banco de dados relacional que armazenará todos os dados relevantes para o sistema.

**Requisitos:**

1. O portal possui diversos **jornalistas** cadastrados, cada um com seu nome completo, e-mail, telefone e data de contratação.  
2. As **notícias** publicadas devem conter título, conteúdo, data de criação, horário e status (rascunho, publicada ou arquivada). Cada notícia é escrita por um ou mais jornalistas.  
3. As notícias podem conter **imagens e vídeos**, com descrição e link de mídia externa ou arquivo.  
4. As notícias são organizadas em **categorias**, como esporte, política, tecnologia etc. Uma notícia deve pertencer a apenas uma categoria.  
5. Os **leitores** podem se cadastrar no portal, informando nome, e-mail e data de nascimento.  
6. **Leitores** podem comentar as notícias. Cada comentário deve ter conteúdo textual, data e hora do envio, além de estar associado a um único leitor e uma única notícia.  
7. **Leitores** também podem avaliar as notícias (nota de 1 a 5) e salvá-las em uma lista pessoal de favoritos.  
8. O sistema deve permitir buscas por palavras-chave nos títulos e conteúdos das notícias.

---

## ❓ Perguntas da Atividade

1. **Identifique as entidades necessárias para o banco de dados da empresa de mídia digital.**  
2. **Para cada entidade, liste os atributos necessários.**  
3. **Defina os relacionamentos entre as entidades, especificando os tipos de cardinalidade (1:1, 1:N, N:N).**

---

> *Este repositório é dedicado ao registro completo e organizado das atividades, estudos, materiais e práticas desenvolvidas na disciplina de Banco de Dados Avançado, servindo como recurso de consulta e suporte para o aprendizado contínuo.*
