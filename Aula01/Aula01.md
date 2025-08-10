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
  <a href="#-atividade">Atividade</a>
</p>

## 📜 Resumo  
Nesta aula, foi apresentado um estudo de caso para a criação de um banco de dados para um **portal de notícias online**. O sistema contempla o cadastro de jornalistas, leitores, notícias, categorias, mídias, comentários, avaliações e favoritos.  
O desafio principal foi identificar entidades, listar atributos e definir os relacionamentos, gerando um **Modelo Entidade-Relacionamento (MER)** e o script SQL para implementação.

## 🔍 Conteúdo abordado  
- Análise de requisitos do sistema  
- Definição de entidades e atributos  
- Modelagem de relacionamentos (1:1, 1:N, N:N)  
- Criação do Modelo Entidade-Relacionamento (MER)  
- Implementação no Oracle Live SQL

## 📎 Arquivos da Aula 01  
- `Aula_01_ementa.pptx` — Ementa da disciplina e objetivos  
- `Estudo_caso_portal_noticias.pptx` — Requisitos e enunciado da atividade  
- `Resp_Ex123.pptx` — Respostas iniciais da modelagem  
- `Atividade_Aula_01.md` — Enunciado, perguntas e respostas da atividade  
- `Diagrama_MER_Portal_Noticias.md` — Diagrama MER em formato Mermaid  
- `script_portal_noticias.sql` — Script SQL para implementação no Oracle Live SQL

## 📎 Atividade

### 📜 Enunciado da Atividade

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

### ❓ Perguntas da Atividade

1. **Identifique as entidades necessárias para o banco de dados da empresa de mídia digital.**  
2. **Para cada entidade, liste os atributos necessários.**  
3. **Defina os relacionamentos entre as entidades, especificando os tipos de cardinalidade (1:1, 1:N, N:N).**

---

### ✅ Respostas

### 1. Entidades Identificadas

- **Jornalista**
- **Notícia**
- **Categoria**
- **Mídia** (imagens e vídeos)
- **Leitor**
- **Comentário**
- **Avaliação**
- **Favorito**
- **StatusNoticia** (opcional como entidade separada, se for tabela de domínio)

---

### 2. Entidades e Atributos

**a) Jornalista**  
- id_jornalista (PK)  
- nome_completo  
- email  
- telefone  
- data_contratacao  

**b) Notícia**  
- id_noticia (PK)  
- titulo  
- conteudo  
- data_criacao  
- hora_criacao  
- id_status (FK → StatusNoticia)  
- id_categoria (FK → Categoria)  

**c) StatusNoticia** (Tabela de domínio)  
- id_status (PK)  
- descricao_status (Rascunho, Publicada, Arquivada)  

**d) Categoria**  
- id_categoria (PK)  
- nome_categoria  

**e) Mídia**  
- id_midia (PK)  
- tipo_midia (Imagem/Vídeo)  
- descricao  
- link_arquivo  
- id_noticia (FK → Notícia)  

**f) Leitor**  
- id_leitor (PK)  
- nome_completo  
- email  
- data_nascimento  

**g) Comentário**  
- id_comentario (PK)  
- conteudo  
- data_envio  
- hora_envio  
- id_leitor (FK → Leitor)  
- id_noticia (FK → Notícia)  

**h) Avaliação**  
- id_avaliacao (PK)  
- nota (1 a 5)  
- id_leitor (FK → Leitor)  
- id_noticia (FK → Notícia)  

**i) Favorito**  
- id_favorito (PK)  
- id_leitor (FK → Leitor)  
- id_noticia (FK → Notícia)  

**j) Jornalista_Noticia** (tabela associativa para relação N:N)  
- id_jornalista (FK → Jornalista)  
- id_noticia (FK → Notícia)  



---

### 3. Relacionamentos e Cardinalidades

1. **Jornalista ↔ Notícia**  
   - Relação **N:N** (um jornalista pode escrever várias notícias e uma notícia pode ser escrita por vários jornalistas).  
   - Implementada por **Jornalista_Noticia**.

2. **Notícia ↔ Categoria**  
   - Relação **1:N** (uma categoria pode ter várias notícias, mas cada notícia pertence a uma única categoria).

3. **Notícia ↔ Mídia**  
   - Relação **1:N** (uma notícia pode ter várias mídias, mas cada mídia pertence a uma única notícia).

4. **Notícia ↔ Comentário**  
   - Relação **1:N** (uma notícia pode ter vários comentários, mas cada comentário pertence a uma única notícia).

5. **Leitor ↔ Comentário**  
   - Relação **1:N** (um leitor pode fazer vários comentários, mas cada comentário é de um único leitor).

6. **Leitor ↔ Avaliação**  
   - Relação **1:N** (um leitor pode avaliar várias notícias, mas cada avaliação é de um único leitor para uma única notícia).

7. **Leitor ↔ Favorito**  
   - Relação **1:N** (um leitor pode favoritar várias notícias, mas cada favorito é de um único leitor).

8. **Notícia ↔ StatusNoticia**  
   - Relação **1:N** (um status pode estar associado a várias notícias, mas cada notícia possui apenas um status).

<!--

### Diagrama MER - Portal de Notícias

```mermaid
erDiagram
    Jornalista {
        int id_jornalista PK
        string nome_completo
        string email
        string telefone
        date data_contratacao
    }
    Noticia {
        int id_noticia PK
        string titulo
        string conteudo
        date data_criacao
        time hora_criacao
        int id_status FK
        int id_categoria FK
    }
    StatusNoticia {
        int id_status PK
        string descricao_status
    }
    Categoria {
        int id_categoria PK
        string nome_categoria
    }
    Midia {
        int id_midia PK
        string tipo_midia
        string descricao
        string link_arquivo
        int id_noticia FK
    }
    Leitor {
        int id_leitor PK
        string nome_completo
        string email
        date data_nascimento
    }
    Comentario {
        int id_comentario PK
        string conteudo
        date data_envio
        time hora_envio
        int id_leitor FK
        int id_noticia FK
    }
    Avaliacao {
        int id_avaliacao PK
        int nota
        int id_leitor FK
        int id_noticia FK
    }
    Favorito {
        int id_favorito PK
        int id_leitor FK
        int id_noticia FK
    }
    Jornalista_Noticia {
        int id_jornalista FK
        int id_noticia FK
    }

    Jornalista ||--o{ Jornalista_Noticia : escreve
    Noticia ||--o{ Jornalista_Noticia : "é escrita por"
    Categoria ||--o{ Noticia : "possui"
    StatusNoticia ||--o{ Noticia : "tem"
    Noticia ||--o{ Midia : "contém"
    Noticia ||--o{ Comentario : "recebe"
    Leitor ||--o{ Comentario : "faz"
    Leitor ||--o{ Avaliacao : "avalia"
    Noticia ||--o{ Avaliacao : "é avaliada"
    Leitor ||--o{ Favorito : "favorita"
    Noticia ||--o{ Favorito : "é favoritada"
```

-->

---

> *Este repositório é dedicado ao registro completo e organizado das atividades, estudos, materiais e práticas desenvolvidas na disciplina de Banco de Dados Avançado, servindo como recurso de consulta e suporte para o aprendizado contínuo.*
