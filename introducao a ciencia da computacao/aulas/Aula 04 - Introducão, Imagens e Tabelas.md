# Walkthrough — LaTeX e Escrita Acadêmica

## 1. Objetivo da aula

Ao final deste walkthrough, o estudante deve ser capaz de:

1. Criar um documento simples em LaTeX.
2. Organizar um texto com seções, subseções e parágrafos.
3. Inserir imagens em um documento.
4. Inserir tabelas em um documento.
5. Compreender como estruturar a introdução de um artigo acadêmico.

---

# Parte 1 — Estrutura básica de um documento LaTeX

Um documento LaTeX possui duas partes principais:

1. **Preâmbulo**: onde são definidos o tipo do documento e os pacotes usados.
2. **Corpo do documento**: onde o conteúdo é escrito.

Exemplo mínimo:

```latex
\documentclass[12pt]{article}

\usepackage[utf8]{inputenc}
\usepackage[brazil]{babel}
\usepackage{graphicx}
\usepackage{booktabs}

\title{Título do Artigo}
\author{Nome do Autor}
\date{\today}

\begin{document}

\maketitle

\section{Introdução}

Este é o primeiro parágrafo do artigo. Aqui o autor apresenta o tema geral do trabalho.

\section{Desenvolvimento}

Nesta seção, o conteúdo principal do texto é apresentado.

\section{Conclusão}

Nesta seção, são apresentadas as considerações finais.

\end{document}
```

## Explicação dos principais comandos

```latex
\documentclass[12pt]{article}
```

Define que o documento será um artigo, com fonte tamanho 12.

```latex
\usepackage[utf8]{inputenc}
```

Permite o uso de caracteres acentuados, como “ação”, “método” e “introdução”.

```latex
\usepackage[brazil]{babel}
```

Configura o idioma do documento para português do Brasil.

```latex
\usepackage{graphicx}
```

Permite inserir imagens.

```latex
\usepackage{booktabs}
```

Permite criar tabelas com melhor aparência visual.

```latex
\begin{document}
...
\end{document}
```

Delimita o conteúdo principal do documento.

---

# Parte 2 — Organização do texto

Em LaTeX, o texto pode ser organizado em seções e subseções.

```latex
\section{Introdução}

Texto da introdução.

\subsection{Contexto}

Texto sobre o contexto do trabalho.

\subsection{Problema}

Texto sobre o problema investigado.

\section{Metodologia}

Texto sobre os procedimentos metodológicos.
```

A hierarquia mais comum é:

```latex
\section{}
\subsection{}
\subsubsection{}
```

Exemplo:

```latex
\section{Introdução}

A escrita acadêmica exige clareza, organização e objetividade. Em um artigo científico, a introdução possui o papel de apresentar o tema, contextualizar o problema e indicar o objetivo do trabalho.

\subsection{Contextualização}

A contextualização ajuda o leitor a compreender em qual área o trabalho está inserido e por que o tema é relevante.

\subsection{Objetivo}

O objetivo define o que o trabalho pretende investigar, propor, avaliar ou discutir.
```

---

# Parte 3 — Como adicionar imagens ao LaTeX

Para inserir imagens, é necessário usar o pacote:

```latex
\usepackage{graphicx}
```

Esse pacote deve ser adicionado no preâmbulo do documento.

## Exemplo simples de imagem

```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.7\textwidth]{figuras/exemplo.png}
    \caption{Exemplo de imagem inserida no documento.}
    \label{fig:exemplo}
\end{figure}
```

## Explicação do código

```latex
\begin{figure}[h]
```

Cria um ambiente de figura. O `[h]` indica que o LaTeX deve tentar posicionar a imagem “aqui”, ou seja, próximo ao local onde ela foi declarada.

```latex
\centering
```

Centraliza a imagem.

```latex
\includegraphics[width=0.7\textwidth]{figuras/exemplo.png}
```

Insere a imagem. Nesse exemplo, a imagem está dentro da pasta `figuras` e possui o nome `exemplo.png`.

O parâmetro:

```latex
width=0.7\textwidth
```

define que a imagem ocupará 70% da largura do texto.

```latex
\caption{Exemplo de imagem inserida no documento.}
```

Adiciona uma legenda à imagem.

```latex
\label{fig:exemplo}
```

Cria um rótulo para que a imagem possa ser referenciada no texto.

## Como referenciar uma imagem no texto

Depois de definir o `label`, a imagem pode ser referenciada assim:

```latex
Como apresentado na Figura~\ref{fig:exemplo}, o modelo possui três etapas principais.
```

O símbolo `~` evita que “Figura” e o número fiquem separados em linhas diferentes.

## Exemplo completo com imagem

```latex
\documentclass[12pt]{article}

\usepackage[utf8]{inputenc}
\usepackage[brazil]{babel}
\usepackage{graphicx}

\title{Exemplo com Imagem}
\author{Nome do Autor}
\date{\today}

\begin{document}

\maketitle

\section{Introdução}

As imagens são úteis para representar modelos, arquiteturas, diagramas, fluxos de execução e resultados experimentais.

A Figura~\ref{fig:modelo} apresenta um exemplo de fluxo utilizado em um processo de análise de dados.

\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{figuras/modelo.png}
    \caption{Exemplo de fluxo de análise de dados.}
    \label{fig:modelo}
\end{figure}

\end{document}
```

## Boas práticas ao usar imagens

Uma imagem acadêmica deve:

1. Ser mencionada no texto antes ou próximo de aparecer.
2. Ter legenda clara.
3. Ter boa resolução.
4. Não ser apenas decorativa.
5. Ajudar a explicar algum conceito, resultado ou processo.

Exemplo ruim:

```latex
Abaixo temos uma imagem.
```

Exemplo melhor:

```latex
A Figura~\ref{fig:arquitetura} apresenta a arquitetura geral da solução proposta, destacando os três componentes principais: interface, serviço de processamento e banco de dados.
```

---

# Parte 4 — Como adicionar tabelas ao LaTeX

Tabelas são usadas para organizar dados, comparações, resultados e classificações.

Para tabelas com melhor aparência, recomenda-se usar:

```latex
\usepackage{booktabs}
```

## Exemplo simples de tabela

```latex
\begin{table}[h]
    \centering
    \caption{Exemplo de tabela com dados de estudantes.}
    \label{tab:estudantes}
    \begin{tabular}{lll}
        \toprule
        Nome & Curso & Média \\
        \midrule
        Ana & Engenharia de Software & 8,5 \\
        Bruno & Ciência da Computação & 7,8 \\
        Carla & Sistemas de Informação & 9,1 \\
        \bottomrule
    \end{tabular}
\end{table}
```

## Explicação do código

```latex
\begin{table}[h]
```

Cria um ambiente de tabela.

```latex
\centering
```

Centraliza a tabela.

```latex
\caption{Exemplo de tabela com dados de estudantes.}
```

Adiciona a legenda da tabela.

```latex
\label{tab:estudantes}
```

Cria um rótulo para referenciar a tabela no texto.

```latex
\begin{tabular}{lll}
```

Cria a estrutura da tabela. Cada letra indica o alinhamento de uma coluna:

| Letra | Significado |
|---|---|
| `l` | alinhado à esquerda |
| `c` | centralizado |
| `r` | alinhado à direita |

Neste exemplo:

```latex
{lll}
```

significa que a tabela possui três colunas, todas alinhadas à esquerda.

```latex
\toprule
\midrule
\bottomrule
```

Criam linhas horizontais com melhor aparência visual.

## Como referenciar uma tabela no texto

```latex
A Tabela~\ref{tab:estudantes} apresenta a média final dos estudantes avaliados.
```

## Exemplo completo com tabela

```latex
\documentclass[12pt]{article}

\usepackage[utf8]{inputenc}
\usepackage[brazil]{babel}
\usepackage{booktabs}

\title{Exemplo com Tabela}
\author{Nome do Autor}
\date{\today}

\begin{document}

\maketitle

\section{Resultados}

A Tabela~\ref{tab:ferramentas} apresenta uma comparação entre três ferramentas de análise de código.

\begin{table}[h]
    \centering
    \caption{Comparação entre ferramentas de análise de código.}
    \label{tab:ferramentas}
    \begin{tabular}{lll}
        \toprule
        Ferramenta & Linguagem & Tipo de análise \\
        \midrule
        Checkstyle & Java & Estilo de código \\
        Pylint & Python & Qualidade de código \\
        ESLint & JavaScript & Padrões e erros \\
        \bottomrule
    \end{tabular}
\end{table}

\end{document}
```

## Tabela com texto mais longo

Quando uma coluna possui texto longo, pode-se definir uma largura fixa usando `p{}`.

```latex
\begin{table}[h]
    \centering
    \caption{Exemplo de tabela com descrições.}
    \label{tab:descricoes}
    \begin{tabular}{lp{8cm}}
        \toprule
        Elemento & Descrição \\
        \midrule
        Introdução & Apresenta o tema, o problema, a justificativa, o objetivo e a organização do artigo. \\
        Metodologia & Descreve os procedimentos utilizados para conduzir o estudo. \\
        Resultados & Apresenta os dados obtidos a partir da execução da pesquisa. \\
        \bottomrule
    \end{tabular}
\end{table}
```

Nesse exemplo:

```latex
p{8cm}
```

define que a segunda coluna terá largura de 8 centímetros e poderá quebrar linha automaticamente.

---

# Parte 5 — Cuidados básicos na escrita em LaTeX

## 1. Separar parágrafos corretamente

Em LaTeX, um novo parágrafo é criado deixando uma linha em branco.

Exemplo:

```latex
Este é o primeiro parágrafo do texto. Ele apresenta uma ideia inicial.

Este é o segundo parágrafo. Ele desenvolve uma nova ideia relacionada ao tema anterior.
```

## 2. Evitar excesso de formatação manual

Em vez de usar muitos comandos visuais, como negrito, sublinhado e espaçamentos manuais, prefira usar a estrutura do próprio LaTeX.

Evite:

```latex
\textbf{\Large Introdução}
```

Prefira:

```latex
\section{Introdução}
```

## 3. Usar rótulos para figuras e tabelas

Evite escrever manualmente:

```latex
Como mostra a Figura 1...
```

Prefira:

```latex
Como mostra a Figura~\ref{fig:modelo}...
```

Assim, se a numeração mudar, o LaTeX atualiza automaticamente.

---

# Parte 6 — Como escrever uma boa introdução para um artigo

A introdução é uma das partes mais importantes de um artigo acadêmico. Ela precisa preparar o leitor para compreender o restante do trabalho.

Uma boa introdução deve responder, de forma progressiva, às seguintes perguntas:

1. **Qual é o tema geral do artigo?**
2. **Por que esse tema é importante?**
3. **Qual é o problema ou desafio investigado?**
4. **O que já se sabe sobre o tema?**
5. **Qual lacuna ainda existe?**
6. **Qual é o objetivo do artigo?**
7. **Como o estudo foi conduzido?**
8. **Quais são as principais contribuições do trabalho?**
9. **Como o artigo está organizado?**

## Estrutura recomendada para uma introdução

Uma introdução pode ser organizada em seis movimentos principais:

1. Contextualização do tema.
2. Apresentação da importância do tema.
3. Apresentação do problema.
4. Identificação da lacuna.
5. Apresentação do objetivo e da abordagem metodológica.
6. Apresentação das contribuições e da estrutura do artigo.

---

# 6.1 Contextualização do tema

A contextualização apresenta o tema geral do artigo. O objetivo é situar o leitor.

Exemplo de parágrafo:

> O desenvolvimento de software tornou-se uma atividade central para organizações públicas e privadas, uma vez que sistemas computacionais apoiam processos de negócio, serviços digitais, comunicação e tomada de decisão. Nesse cenário, a qualidade do código-fonte influencia diretamente a manutenibilidade, a evolução e a confiabilidade dos sistemas desenvolvidos.

Esse parágrafo faz três coisas:

1. Apresenta o tema geral: desenvolvimento de software.
2. Mostra sua relevância: sistemas apoiam processos importantes.
3. Introduz um conceito específico: qualidade do código-fonte.

---

# 6.2 Importância do tema

Depois de contextualizar, é necessário explicar por que o tema importa.

Exemplo:

> A baixa qualidade do código pode dificultar a compreensão do sistema, aumentar o custo de manutenção e introduzir defeitos durante atividades de evolução. Por esse motivo, práticas como revisão de código, testes automatizados e análise estática têm sido utilizadas para apoiar equipes na identificação precoce de problemas técnicos.

Esse parágrafo mostra consequências práticas do problema e introduz possíveis soluções.

---

# 6.3 Apresentação do problema

O problema deve deixar claro o que ainda não está funcionando bem ou o que precisa ser investigado.

Exemplo:

> Apesar da disponibilidade de ferramentas de análise estática, muitas equipes ainda enfrentam dificuldades para incorporá-las de maneira efetiva ao processo de desenvolvimento. Em alguns casos, essas ferramentas geram muitos alertas, são configuradas de forma inadequada ou não se integram bem ao fluxo de trabalho dos desenvolvedores.

Esse parágrafo apresenta um problema específico: a dificuldade de adoção efetiva de ferramentas.

---

# 6.4 Lacuna de pesquisa

A lacuna mostra o que ainda não foi suficientemente explicado, avaliado ou resolvido.

Exemplo:

> Embora estudos anteriores tenham investigado benefícios e limitações de ferramentas de análise estática, ainda há pouca compreensão sobre como estudantes de cursos de Computação configuram, interpretam e utilizam os alertas produzidos por essas ferramentas durante atividades práticas de programação.

Esse parágrafo indica que existe conhecimento prévio, mas também aponta uma ausência: o uso por estudantes em atividades práticas.

---

# 6.5 Objetivo do artigo

O objetivo deve ser claro, direto e verificável.

Exemplo:

> Diante desse contexto, este artigo tem como objetivo analisar como estudantes de Computação utilizam ferramentas de análise estática durante a realização de exercícios de programação em Java. Para isso, foi conduzido um estudo exploratório com estudantes de uma disciplina de Programação Orientada a Objetos, no qual foram observadas as configurações adotadas, os tipos de alertas encontrados e as dificuldades relatadas pelos participantes.

Esse parágrafo apresenta:

1. O objetivo.
2. O público ou contexto investigado.
3. Uma visão geral do método.

---

# 6.6 Contribuições do artigo

As contribuições indicam o que o artigo entrega ao leitor.

Exemplo:

> Como principais contribuições, este artigo apresenta: uma caracterização dos tipos de problemas identificados por ferramentas de análise estática em exercícios de programação; uma análise das dificuldades enfrentadas pelos estudantes ao interpretar os alertas; e um conjunto de recomendações para o uso dessas ferramentas em disciplinas introdutórias de programação.

Esse parágrafo deixa claro o valor do artigo.

---

# 6.7 Organização do artigo

Ao final da introdução, é comum apresentar a estrutura do artigo.

Exemplo:

> O restante deste artigo está organizado da seguinte forma. A Seção 2 apresenta os conceitos fundamentais sobre qualidade de código e análise estática. A Seção 3 descreve os procedimentos metodológicos adotados no estudo. A Seção 4 apresenta os resultados obtidos. A Seção 5 discute as implicações dos resultados para o ensino de programação. Por fim, a Seção 6 apresenta as conclusões e trabalhos futuros.

---

# Parte 7 — Exemplo completo de introdução

A seguir, temos uma introdução completa usando os elementos discutidos.

> O desenvolvimento de software tornou-se uma atividade central para organizações públicas e privadas, uma vez que sistemas computacionais apoiam processos de negócio, serviços digitais, comunicação e tomada de decisão. Nesse cenário, a qualidade do código-fonte influencia diretamente a manutenibilidade, a evolução e a confiabilidade dos sistemas desenvolvidos.
>
> A baixa qualidade do código pode dificultar a compreensão do sistema, aumentar o custo de manutenção e introduzir defeitos durante atividades de evolução. Por esse motivo, práticas como revisão de código, testes automatizados e análise estática têm sido utilizadas para apoiar equipes na identificação precoce de problemas técnicos.
>
> Apesar da disponibilidade de ferramentas de análise estática, muitas equipes ainda enfrentam dificuldades para incorporá-las de maneira efetiva ao processo de desenvolvimento. Em alguns casos, essas ferramentas geram muitos alertas, são configuradas de forma inadequada ou não se integram bem ao fluxo de trabalho dos desenvolvedores.
>
> Embora estudos anteriores tenham investigado benefícios e limitações de ferramentas de análise estática, ainda há pouca compreensão sobre como estudantes de cursos de Computação configuram, interpretam e utilizam os alertas produzidos por essas ferramentas durante atividades práticas de programação.
>
> Diante desse contexto, este artigo tem como objetivo analisar como estudantes de Computação utilizam ferramentas de análise estática durante a realização de exercícios de programação em Java. Para isso, foi conduzido um estudo exploratório com estudantes de uma disciplina de Programação Orientada a Objetos, no qual foram observadas as configurações adotadas, os tipos de alertas encontrados e as dificuldades relatadas pelos participantes.
>
> Como principais contribuições, este artigo apresenta: uma caracterização dos tipos de problemas identificados por ferramentas de análise estática em exercícios de programação; uma análise das dificuldades enfrentadas pelos estudantes ao interpretar os alertas; e um conjunto de recomendações para o uso dessas ferramentas em disciplinas introdutórias de programação.
>
> O restante deste artigo está organizado da seguinte forma. A Seção 2 apresenta os conceitos fundamentais sobre qualidade de código e análise estática. A Seção 3 descreve os procedimentos metodológicos adotados no estudo. A Seção 4 apresenta os resultados obtidos. A Seção 5 discute as implicações dos resultados para o ensino de programação. Por fim, a Seção 6 apresenta as conclusões e trabalhos futuros.

---

# Parte 8 — Modelo de introdução para os alunos preencherem

Os alunos podem usar o seguinte modelo:

```text
[Contextualização]
Atualmente, __________________________ tem se tornado relevante porque __________________________.

[Importância]
Esse tema é importante porque __________________________. Quando esse aspecto não é considerado, podem ocorrer problemas como __________________________.

[Problema]
Apesar disso, ainda existem dificuldades relacionadas a __________________________. Em particular, __________________________.

[Lacuna]
Embora estudos ou práticas anteriores tenham abordado __________________________, ainda há pouca compreensão sobre __________________________.

[Objetivo]
Diante desse contexto, este artigo tem como objetivo __________________________.

[Método]
Para alcançar esse objetivo, foi realizado __________________________, considerando __________________________.

[Contribuições]
Como principais contribuições, este artigo apresenta __________________________.

[Organização]
O restante deste artigo está organizado da seguinte forma: __________________________.
```

---

# Parte 9 — Erros comuns em introduções

## 1. Começar de forma ampla demais

Exemplo fraco:

> Desde os primórdios da humanidade, o ser humano busca resolver problemas.

Esse tipo de abertura é genérico e não aproxima rapidamente o leitor do tema do artigo.

Melhor:

> O desenvolvimento de software educacional tem se tornado cada vez mais relevante em instituições de ensino que buscam apoiar atividades práticas de programação.

## 2. Não apresentar o problema

Uma introdução não deve apenas explicar o tema. Ela precisa mostrar qual problema motiva o trabalho.

Exemplo incompleto:

> Ferramentas de análise estática são usadas para avaliar código-fonte. Elas identificam problemas de estilo, possíveis defeitos e violações de padrões.

Esse trecho explica o tema, mas não apresenta um problema.

Melhor:

> Embora ferramentas de análise estática sejam capazes de identificar problemas no código-fonte, estudantes iniciantes podem ter dificuldade para interpretar os alertas produzidos, especialmente quando as mensagens são técnicas ou pouco relacionadas ao contexto do exercício.

## 3. Apresentar objetivo vago

Exemplo fraco:

> Este artigo tem como objetivo falar sobre análise estática.

Melhor:

> Este artigo tem como objetivo analisar as dificuldades enfrentadas por estudantes de Programação Orientada a Objetos ao utilizar ferramentas de análise estática em exercícios práticos de Java.

## 4. Não conectar os parágrafos

A introdução deve ter progressão lógica. Cada parágrafo precisa preparar o próximo.

Uma sequência adequada seria:

```text
Tema geral → importância → problema → lacuna → objetivo → método → contribuições
```

---

# Parte 10 — Atividade prática sugerida

## Atividade

Escolha um tema relacionado à Computação e escreva uma introdução acadêmica de 5 a 7 parágrafos.

A introdução deve conter:

1. Contextualização do tema.
2. Justificativa da importância do tema.
3. Apresentação do problema.
4. Lacuna ou motivação específica.
5. Objetivo do artigo.
6. Breve descrição do método.
7. Principais contribuições esperadas.

Além disso, o documento deve ser escrito em LaTeX e conter:

1. Título.
2. Nome do autor.
3. Pelo menos uma seção.
4. Pelo menos uma figura.
5. Pelo menos uma tabela.
6. Referência à figura no texto.
7. Referência à tabela no texto.

---

# Parte 11 — Código-base para a atividade

```latex
\documentclass[12pt]{article}

\usepackage[utf8]{inputenc}
\usepackage[brazil]{babel}
\usepackage{graphicx}
\usepackage{booktabs}

\title{Título do Artigo}
\author{Nome do Estudante}
\date{\today}

\begin{document}

\maketitle

\section{Introdução}

Escreva aqui o primeiro parágrafo, apresentando o contexto geral do tema.

Escreva aqui o segundo parágrafo, explicando por que o tema é importante.

Escreva aqui o terceiro parágrafo, apresentando o problema investigado.

Escreva aqui o quarto parágrafo, explicando a lacuna ou motivação específica.

Escreva aqui o quinto parágrafo, apresentando o objetivo do artigo.

Escreva aqui o sexto parágrafo, descrevendo brevemente o método.

Escreva aqui o sétimo parágrafo, apresentando as contribuições do artigo.

A Figura~\ref{fig:exemplo} apresenta um exemplo de elemento visual usado no artigo.

\begin{figure}[h]
    \centering
    \includegraphics[width=0.7\textwidth]{figuras/exemplo.png}
    \caption{Descrição da imagem utilizada no artigo.}
    \label{fig:exemplo}
\end{figure}

A Tabela~\ref{tab:exemplo} apresenta uma síntese dos principais elementos da introdução.

\begin{table}[h]
    \centering
    \caption{Elementos esperados na introdução.}
    \label{tab:exemplo}
    \begin{tabular}{lp{8cm}}
        \toprule
        Elemento & Descrição \\
        \midrule
        Contexto & Apresenta o tema geral do artigo. \\
        Problema & Explica a dificuldade, limitação ou desafio investigado. \\
        Objetivo & Define o que o artigo pretende realizar. \\
        Método & Resume como o estudo foi conduzido. \\
        Contribuições & Apresenta os principais resultados ou entregas esperadas. \\
        \bottomrule
    \end{tabular}
\end{table}

\section{Conclusão}

Escreva uma breve conclusão sobre o exercício realizado.

\end{document}
```
