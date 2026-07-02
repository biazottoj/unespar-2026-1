# Simulado Integrador - Introdução à Ciência da Computação

**Temas avaliados:** Banco de Dados; Computação Gráfica; Engenharia de Software; Interação Humano-Computador; Segurança da Informação; Sistemas Operacionais; Compiladores e Linguagens de Programação.

**Tempo sugerido:** 120 minutos  
**Valor total:** 70,0 pontos  
**Quantidade de questões:** 70 questões, distribuídas em 7 blocos temáticos.

## Orientações gerais

1. Cada bloco possui 10 questões e vale **10,0 pontos**.
2. As questões **1 a 3** de cada bloco são **dissertativas conceituais**. Responda de forma objetiva, em até **3 linhas**.
3. As questões **4 a 10** de cada bloco são **discursivas de análise e aplicação**. Responda em até **4 linhas**, identificando o conceito envolvido e justificando sua resposta.
4. Nas questões contextualizadas, não basta apenas citar um termo. Explique brevemente por que ele se aplica ao cenário.
5. A prova privilegia análise conceitual de situações simples. Não é necessário escrever código, configurar ferramentas ou detalhar procedimentos técnicos avançados.

---

# Bloco 1 - Banco de Dados

## Questões dissertativas conceituais

**1.** Explique o que é um banco de dados e indique uma contribuição que ele oferece para organizações ou aplicações digitais.

**2.** Diferencie o nível conceitual do nível interno da arquitetura de banco de dados.

**3.** Diferencie, de modo geral, bancos de dados relacionais e não relacionais. Cite uma característica de cada abordagem.

## Questões discursivas de análise e aplicação

**4.** Um aplicativo de biblioteca permite que estudantes visualizem apenas seus próprios empréstimos, enquanto bibliotecários acessam o histórico completo de todos os usuários. Identifique o nível da arquitetura de banco de dados mais relacionado à tela do estudante e explique por que esse nível é importante nesse caso.

**5.** Uma equipe está desenhando as entidades `Aluno`, `Curso`, `Professor` e seus relacionamentos, mas ainda não decidiu como os arquivos serão gravados em disco. Em qual nível da arquitetura esse trabalho se concentra? Justifique.

**6.** Uma loja precisa registrar pedidos, clientes, pagamentos e estoque com dados bem organizados e transações confiáveis. Indique se um banco relacional é uma escolha adequada e justifique com base nas necessidades apresentadas.

**7.** Um sistema de atendimento precisa armazenar relatos de clientes em formatos variados, pois cada tipo de solicitação pode possuir campos diferentes. Entre um banco relacional e um banco não relacional orientado a documentos, indique a alternativa mais flexível para esse caso e justifique.

**8.** Uma universidade utiliza Oracle e deseja implementar uma regra que valide determinadas informações diretamente no servidor de banco de dados. Qual extensão procedural apresentada nos slides pode ser utilizada? Explique sua finalidade.

**9.** Considere o seguinte modelo: `Pedido` possui número, data e valor total; `ItemPedido` possui quantidade e valor parcial, mas só existe quando associado a um pedido. Classifique `ItemPedido` como entidade forte ou fraca e justifique. Indique também um possível atributo derivado de `Pedido`.

**10.** Classifique cada item como dado estruturado, semiestruturado ou não estruturado:  
a) uma tabela com RA, nome e curso;  
b) um arquivo JSON com informações de produtos;  
c) um vídeo de uma aula gravada.  
Justifique brevemente cada classificação.

---

# Bloco 2 - Computação Gráfica

## Questões dissertativas conceituais

**11.** Defina Computação Gráfica e explique seu objetivo em relação à comunicação de informações.

**12.** Cite os dois marcos históricos apresentados nos slides para o surgimento da Computação Gráfica e explique, de forma breve, sua relevância.

**13.** Diferencie jogos 2D e 3D quanto à representação visual e à sensação de profundidade.

## Questões discursivas de análise e aplicação

**14.** Um hospital deseja apresentar imagens de exames de forma que médicos consigam observar estruturas do corpo com maior clareza. Explique como a Computação Gráfica pode contribuir para esse contexto.

**15.** Uma equipe de jogos criou a forma geométrica de um personagem, mas ele ainda parece sem detalhes de pele, roupa e acessórios. Qual tecnologia apresentada nos slides deve ser priorizada nessa etapa? Justifique.

**16.** Em um jogo de corrida, os carros já possuem modelos e texturas, mas todos parecem visualmente planos e sem sombra. Indique a tecnologia que deve ser trabalhada para melhorar esse aspecto e explique sua função.

**17.** Após modelar objetos, aplicar texturas e definir iluminação, uma equipe precisa produzir a imagem final que aparecerá na tela do jogador. Qual etapa ou tecnologia está sendo realizada? Explique.

**18.** Um grupo quer criar um jogo simples de perguntas com ícones, textos e telas planas. Entre uma abordagem 2D e 3D, indique a alternativa inicialmente mais adequada e justifique considerando a proposta do jogo.

**19.** Um estúdio pretende aumentar o realismo de reflexos, sombras e interação da luz em um jogo. Qual técnica citada nos slides está relacionada a esse objetivo? Explique o resultado visual esperado.

**20.** Uma empresa quer desenvolver uma visita virtual a um museu para ser utilizada com óculos imersivos. Indique uma área de aplicação da Computação Gráfica relacionada a esse projeto e explique por que ela é adequada.

---

# Bloco 3 - Engenharia de Software

## Questões dissertativas conceituais

**21.** Defina Engenharia de Software e apresente seu objetivo principal no desenvolvimento de sistemas.

**22.** Explique o que é o Ciclo de Vida do Software (SDLC) e por que ele é utilizado.

**23.** Cite dois atributos de qualidade de software apresentados nos slides e explique brevemente o que cada um representa.

## Questões discursivas de análise e aplicação

**24.** Uma equipe desenvolverá um aplicativo para eventos estudantis. Os organizadores ainda mudam com frequência as funcionalidades desejadas e querem receber versões parciais para avaliar. Entre os modelos Cascata, Iterativo, Espiral e Ágil, indique o mais adequado e justifique.

**25.** Um sistema bancário permite transferências, mas apresenta erros ocasionais que impedem a conclusão de operações importantes. Indique uma prática de Engenharia de Software que pode ajudar a reduzir esse problema e relacione-a a um atributo de qualidade.

**26.** Uma empresa iniciará um sistema inovador, com tecnologia pouco conhecida e riscos relevantes de custo e viabilidade. Qual modelo de processo tende a ser mais apropriado segundo os slides? Justifique.

**27.** Um sistema de matrícula apresenta lentidão quando muitos estudantes acessam o portal simultaneamente. De acordo com a relação entre problemas e soluções apresentada nos slides, qual aspecto deve ser analisado prioritariamente? Explique.

**28.** Duas aplicações de uma instituição precisam trocar informações, mas a integração entre elas é difícil e gera retrabalho. Qual solução mencionada nos slides pode ajudar nesse cenário? Justifique.

**29.** Uma loja virtual tem picos de acesso em períodos promocionais e precisa disponibilizar seu sistema continuamente. Explique como a computação em nuvem pode contribuir para esse cenário.

**30.** Uma escola armazena dados pessoais de estudantes em uma plataforma digital. Explique por que práticas de DevSecOps e atenção à LGPD são relevantes desde o desenvolvimento desse sistema.

---

# Bloco 4 - Interação Humano-Computador

## Questões dissertativas conceituais

**31.** Defina Interação Humano-Computador (IHC) e explique o que significa colocar o foco no humano.

**32.** Diferencie barreiras acidentais de barreiras intencionais em sistemas digitais.

**33.** Explique o que são dark patterns e cite um exemplo apresentado nos slides.

## Questões discursivas de análise e aplicação

**34.** Um serviço de streaming permite assinatura em poucos cliques, mas exige que o usuário passe por diversas telas escondidas para cancelar o plano. Identifique o dark pattern presente e justifique.

**35.** Um site exibe, ao lado de uma oferta, o botão: “Não, eu prefiro pagar mais caro”. Identifique o dark pattern utilizado e explique como ele tenta influenciar a decisão do usuário.

**36.** Em um caixa eletrônico, a opção “Não quero recibo” aparece em verde e a opção “Imprimir recibo” aparece em vermelho, induzindo o usuário a interpretar as cores como recomendação. Explique por que essa escolha visual pode ser considerada uma barreira intencional.

**37.** Um aplicativo bancário destaca empréstimos imediatos, deixa seguros pré-selecionados e esconde funções importantes em menus complexos. Cite duas decisões de design problemáticas presentes no caso e explique seus possíveis efeitos.

**38.** Uma rede social possui rolagem infinita e o usuário perde facilmente a noção de tempo de uso. Identifique o mecanismo envolvido e explique um possível impacto no comportamento do usuário.

**39.** Em uma plataforma de conteúdo, anúncios pagos são exibidos quase da mesma forma que publicações comuns. Explique qual problema de IHC está presente e por que ele prejudica uma decisão informada.

**40.** Uma equipe está redesenhando o aplicativo de uma clínica. Proponha duas decisões de design mais humano e ético para reduzir barreiras aos usuários. Justifique suas escolhas com base em inclusão, clareza ou segurança.

---

# Bloco 5 - Segurança da Informação

## Questões dissertativas conceituais

**41.** Defina Segurança da Informação e indique dois de seus objetivos.

**42.** Explique os três elementos da tríade CIA: confidencialidade, integridade e disponibilidade.

**43.** Diferencie autenticidade, não repúdio e responsabilidade no contexto de um sistema de informação.

## Questões discursivas de análise e aplicação

**44.** Um prontuário eletrônico foi acessado por uma pessoa que não possuía autorização para visualizar os dados de um paciente. Qual princípio da tríade CIA foi violado? Justifique.

**45.** Em um sistema acadêmico, notas foram alteradas sem autorização. Qual princípio da tríade CIA foi afetado principalmente? Explique.

**46.** Um portal de serviços públicos fica inacessível após receber milhares de requisições simultâneas de dispositivos diferentes. Identifique o tipo de ataque e o princípio de segurança mais diretamente prejudicado.

**47.** Um estudante recebe um e-mail supostamente enviado pelo banco, com uma mensagem de urgência e um link para atualizar sua senha. Cite dois sinais de phishing presentes no caso e indique uma atitude segura.

**48.** Classifique os exemplos a seguir:  
a) programa que parece legítimo, mas esconde uma ameaça;  
b) programa que registra tudo o que é digitado;  
c) malware que se replica sozinho pela rede.  
Indique o nome de cada tipo de ameaça.

**49.** Uma empresa teve seus arquivos criptografados e recebeu uma mensagem exigindo pagamento para liberá-los. Identifique a ameaça e apresente duas medidas preventivas ou de redução de impacto.

**50.** Uma universidade deseja que professores visualizem e alterem notas, estudantes apenas visualizem suas próprias notas e técnicos administrem cadastros. Qual modelo de controle de acesso apresentado nos slides se adequa melhor ao cenário? Justifique.

---

# Bloco 6 - Sistemas Operacionais

## Questões dissertativas conceituais

**51.** Defina Sistema Operacional e explique o papel do kernel.

**52.** Explique as perspectivas de “máquina estendida” e “gerenciador de recursos” para compreender um Sistema Operacional.

**53.** Diferencie sistemas em lote, multiprogramação e tempo compartilhado.

## Questões discursivas de análise e aplicação

**54.** Um estudante usa navegador, editor de texto e aplicativo de música ao mesmo tempo. Explique como o Sistema Operacional participa da execução dessas aplicações e de sua relação com o hardware.

**55.** Dois programas exigem grande uso de CPU e memória ao mesmo tempo. Qual perspectiva do Sistema Operacional é mais diretamente aplicada para lidar com esse conflito? Justifique.

**56.** Um programador deseja gravar um arquivo, mas não precisa conhecer detalhes físicos do disco nem controlar diretamente o hardware. Explique como a ideia de máquina estendida ajuda nesse caso.

**57.** Em um computador antigo, vários programas permanecem na memória e, quando um fica aguardando uma operação de entrada e saída, outro aproveita a CPU. Identifique a etapa histórica ou conceito relacionado e explique sua vantagem.

**58.** Uma universidade possuía um grande computador compartilhado por vários usuários conectados por terminais. Cada pessoa tinha a impressão de utilizar a máquina sozinha. Qual conceito histórico explica essa situação? Justifique.

**59.** O kernel do UNIX foi reescrito em C, tornando possível recompilá-lo em diferentes tipos de hardware. Explique o conceito de portabilidade e indique uma consequência que a diversidade de versões pode trazer.

**60.** Uma empresa desenvolve um aplicativo Android e encontra dificuldades porque há muitos modelos de celulares, versões do sistema e interfaces modificadas por fabricantes. Identifique o problema e explique uma consequência para testes ou atualizações.

---

# Bloco 7 - Compiladores e Linguagens de Programação

## Questões dissertativas conceituais

**61.** Defina linguagem de programação.

**62.** Explique a função de um compilador.

**63.** Diferencie, de modo geral, compiladores e interpretadores quanto a desempenho, agilidade e flexibilidade.

## Questões discursivas de análise e aplicação

**64.** Uma equipe precisa criar uma página web com botões, animações e respostas imediatas às ações do usuário no navegador. Qual linguagem apresentada nos slides é especialmente associada a essa finalidade? Justifique.

**65.** Um estudante deseja automatizar tarefas, analisar dados e desenvolver um pequeno protótipo de machine learning. Qual linguagem apresentada nos slides é uma opção adequada? Justifique.

**66.** Uma empresa desenvolverá um componente de jogo que exige alto desempenho e maior controle sobre memória. Entre as linguagens apresentadas, indique uma escolha adequada e justifique.

**67.** Um projeto envolve um sistema corporativo para Windows e também possui uma parte de jogo feita com Unity. Qual linguagem apresentada nos slides pode atender a esses dois contextos? Explique.

**68.** Organize a sequência básica de tradução de um programa: código escrito em linguagem de programação, compilador, binário, execução pelo computador. Explique a finalidade do compilador nessa sequência.

**69.** Uma equipe pretende criar uma rotina muito próxima do hardware e aceita escrever código mais detalhado em troca de maior controle e desempenho. Qual linguagem ou nível de linguagem apresentado nos slides é mais adequado? Cite uma vantagem e uma desvantagem.

**70.** Os slides apontam computação quântica e green coding como desafios futuros. Explique, de forma breve, por que novas formas de computação e a preocupação com eficiência energética podem exigir evolução das linguagens, compiladores ou práticas de programação.
