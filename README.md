# PyMJC: Python MiniJava Compiler

Este repositório tem como objetivo fazer as entregas do projeto da disciplina de [CK0202 - Construção de Compiladores](https://cc.ufc.br/curso/matriz-curricular/?cod=CK0202) (Semestre 2022.1) do [Departamento de Computação](https://dc.ufc.br/pt/) da [Universidade Federal](https://www.ufc.br/). Professor responsável: [Lincoln Souza Rocha](https://cc.ufc.br/curso/corpo-docente/lincoln).

# Equipe Responável

Os seguintes alunos (equipe XXXXX) são responsáveis pelo projeto: 

-  Mátricula: XXXX | Aluno: XXXXX 
-  Mátricula: XXXX | Aluno: XXXXX
-  Mátricula: XXXX | Aluno: XXXXX

# Método de Avaliação

Os alunos serão avaliados em função de um projeto de implementação de um compilador para a [MiniJava](https://www.cambridge.org/resources/052182060X/) tendo como alvo a arquitetura [MIPS](https://pt.wikibooks.org/wiki/Introdu%C3%A7%C3%A3o_%C3%A0_Arquitetura_de_Computadores/O_que_%C3%A9_o_MIPS%3F?fbclid=IwAR1nOV06c9RILTviaaAtvo2GTdYlLHcmlpUozUYJNKRKud4Ed4jNXCIVgWU). Através do projeto do compilador, os alunos terão a oportunidade de praticar toda a teoria apresentada nas aulas teóricas presenciais. A avaliação da implementação (**AI**) do compilador será realizada de forma iterativa e incremental por meio de entregas parciais, onde uma nota será atribuída ao aluno a cada entrega:

- **AI-a**: Analisador léxico e sintático, com peso de `20%`;
- **AI-b**: Árvores sintática abstrata e análise semântica, com peso de `15%`;
- **AI-c**: Tradução para o código intermediário, com peso de `25%`;
- **AI-d**: Seleção de Instruções, com peso de `15%`;
- **AI-e**: Alocação de registradores, com peso de `15%`;
- **AI-f**: Integração e geração do código final, com peso de `10%`.
 
O prazo de entrega de cada etapa do projeto está especificado no cronograma de aulas apresentado no primeiro dia de aula e disponível no sistema acadêmico oficial, o [SI3 - SGAA](http://si3.ufc.br/sigaa). Para cada entrega, a equipe responsável deverá apresentar um relatório para o professor, seguindo as seguintes regras:

- O ralatório compreende um relato por escrito sucinto sobre o status do projeto referente à etapa atual (veja [aqui](REPORTS.md));
- O relatório será apresentado por um **único aluno** do time, chamado *aluno relator*.

O relato deve responder às seguintes perguntas e incluir os seguintes itens: 

- A etapa foi completamente ou parcialmente concluída?
- No caso de parcialmente concluída, o que não foi concluído?
- O programa passa nos testes automatizados?
- Algum erro de execução foi encontrado para alguma das entradas? Quais?
- Quais as dificuldades encontradas para realização da etapa do projeto?
- Qual a participação de cada membro da equipe na etapa de execução?

Os alunos devem revezar-se na relatoria do projeto, ou seja, o próximo aluno a ser o relator deve ser um dentre os que ainda não foram relatores anteriormente ou, caso todos já tenham sido relatores, aquele que foi o relator mais antigo. A penalidade para o caso de não atendimento ao requisito de revezamento dos alunos na relatoria do projeto é um fator de `0,9` aplicado à nota coletiva, definida adiante.

A avaliação da etapa **AI-i**, onde **i ∊ {a,b,c,d,e,f}**, será computada após a **reunião de avaliação**. Nessa reunião, será apresentado o relatório previamente enviado pela equipe. Após a exposição do relatório, o professor fará perguntas que deverão ser respondidas por alunos diferentes, escolhidos pelo professor. A nota **AI-i** será individual, ou seja, para cada aluno. Será calculada a partir de uma nota atribuída à equipe, chamada **nota coletiva**, não podendo ser superior a essa nota.

- A nota coletiva refere-se à qualidade e organização da apresentação, com peso de `30%`, e ao status da implementação da etapa correspondente do compilador MiniJava (qualidade, organização e corretude do código), com peso de `70%`.
- O cálculo da nota **AI-i** levará em consideração a participação do membro da equipe na execução da etapa, descrita pelo relator, bem como a qualidade das respostas às questões individuais, podendo ser igual ou menor à nota coletiva.
  - Para cada membro da equipe, sua participação na etapa do projeto será avaliada segundo um dos três conceitos abaixo, com o respectivo fator a ser multiplicado à nota coletiva: **Satisfatório** (`1,0`), **Regular** (`0,80`) e **Insatisfatório** (`0,50`);
  - Para a questão oral, o professor atribuirá um dos três conceitos abaixo, com o respectivo fator a ser multiplicado à nota coletiva: **Satisfatório** (`1,0`), **Regular** (`0,9`) e **Insatisfatório** (`0,8`).
 
 # A Linguagem MiniJava
 
O linguagem de programação [MiniJava](https://www.cambridge.org/resources/052182060X/) é um subconjunto da linguagem Java, usado para ensino de projeto e implementação de compiladores. Como é um subconjunto, todo programa MiniJava é um programa Java válido que pode ser executado pela JVM, fornecendo um meio simples dos alunos testarem a saída dos seus compiladores sem ter um compilador MiniJava disponível.

MiniJava restringe a linguagem Java para ter apenas inteiros, booleanos, vetores de inteiros e classes, removendo interfaces, números de ponto flutuante, classes abstratas, strings, vetores de outros tipos etc. Também não há sobrecarga de métodos, ou métodos estáticos, exceto pelo método main da classe principal do programa. Um programa MiniJava está restrito a um único arquivo fonte, com extensão `.java`, não existe o conceito de pacote. Existem vários programas exemplo na página de [MiniJava](https://www.cambridge.org/resources/052182060X/).

Note que MiniJava trata ``System.out.println`` como uma palavra reservada (``PRINT``), não como uma chamada do método ``println``. Isso facilita o restante do compilador. Também não há um operador de divisão.
- Espaços em branco: ``[ \n\t\r\f]``;
- Comentários: dois tipos de comentário, um começando com ``//`` e indo até o final da linha, o outro começando com ``/*`` e terminando com ``*/``, sem aninhamento;
- Palavras reservadas: ``'boolean' (BOOLEN)``, ``'class' (CLASS)``, ``'extends' (EXTENDS)``, ``'public' (PUBLIC)``, ``'static' (STATIC)``, ``'void' (VOID)``, ``'main' (MAIN)``, ``'String' (STRING)``, ``'return' (RETURN)``, ``'int' (INT)``, ``'if' (IF)``, ``'else' (ELSE)``, ``'while' (WHILE)``, ``'System.out.println' (PRINT)``, ``'length' (LENGTH)``, ``'true' (TRUE)``, ``'false' (FALSE)``, ``'this' (THIS)`` e ``'new' (NEW)``;
- Identificadores (``ID``): uma letra, seguido de zero ou mais letras, dígitos ou ``'_'``;
- Numerais (``NUM``): apenas números inteiros;
- Operadores e pontuação: ``'(' LEFTPARENT``, ``')' RIGHTPARENT``, ``'[' LEFTSQRBRACKET``, ``']' RIGHTSQRBRACKET``, ``'{' LEFTBRACE``, ``'}' RIGHTBRACE``, ``';' SEMICOLON``, ``'.' DOT``, ``',' COMMA``, ``'=' EQUALS``, ``'<' LESS``, ``'+' PLUS``, ``'-' MINUS``, ``'*' TIMES``,``'&&' AND``  e ``'!' NOT``.

# A Biblioteca Python SLY
 
 O compilador a ser desenvolvido para a linguagem MiniJava, de agora em diante denominado `PyMJC` (*Python MiniJava Compiler*), deverá ser desenvolvido usando a linguagem Python. Assim, para facilitar o desenvolvimento os alunos deverão usar a biblioteca [SLY](https://sly.readthedocs.io/en/latest/). SLY é uma biblioteca de [código aberto](https://github.com/dabeaz/sly) que provê a implementação do Lex e do Yacc, ferramentas úteis para a construção de **scanners** (analiasadores léxicos) e **parsers** (analisadores sintáticos). A documentação oficial da SLY pode ser encontrada [aqui](https://sly.readthedocs.io/en/latest/sly.html). Além disso, a palestra [Reinventing the Parser Generator @ PyCon 2018](https://youtu.be/zJ9z6Ge-vXs) do autor da SLY pode ser útil.   
 
 # Estrutura do Projeto
 
 O projeto do compilador segue a estrutura organizacional inicial abaixo que deve ser evoluída ao longo das entregas:

```
PyMJCG00
├── .github/workflows
│   └── ci.yml
├── doc
│   └── SemanticCheckings.pdf
├── pymjc
│   ├── back
│   ├── front
|   |   ├── ast.py
|   |   ├── lexer.py
|   |   ├── paser.py
|   |   ├── symbol.py
|   |   └── visitor.py 
│   ├── log.py
│   └── run.py
├── tests
|   ├── testdata
|   |   ├── correct
|   |   |   ├── BinarySearch.java
|   |   |   ├── BinaryTree.java
|   |   |   ├── BubbleSort.java
|   |   |   ├── Factorial.java
|   |   |   ├── LinearSearch.java
|   |   |   ├── LinkedList.java
|   |   |   ├── QuickSort.java
|   |   |   └── TreeVisitor.java
|   |   └── faulty
|   |       ├── semantic
|   |       |   ├── SemanticFaultyAlreadyDeclared.java
|   |       |   ├── SemanticFaultyArrayUsage.java
|   |       |   ├── SemanticFaultyBinaryTypeMismatch.java
|   |       |   ├── SemanticFaultyIfAndWhileUsage.java
|   |       |   ├── SemanticFaultyInvalid.java
|   |       |   ├── SemanticFaultyNotTypeMismatch.java
|   |       |   ├── SemanticFaultyReturnTypeAndArgUsage.java
|   |       |   └── SemanticFaultyUndeclared.java
|   |       ├── syntax
|   |       |   ├── SyntaxBinarySearch.java
|   |       |   ├── SyntaxBinaryTree.java
|   |       |   ├── SyntaxBubbleSort.java
|   |       |   ├── SyntaxFactorial.java
|   |       |   ├── SyntaxLinearSearch.java
|   |       |   ├── SyntaxLinkedList.java
|   |       |   ├── SyntaxQuickSort.java
|   |       |   └── SyntaxTreeVisitor.java
|   |       └── tokens
|   |           ├── TokenBinarySearch.java
|   |           ├── TokenBinaryTree.java
|   |           ├── TokenBubbleSort.java
|   |           ├── TokenFactorial.java
|   |           ├── TokenLinearSearch.java
|   |           ├── TokenLinkedList.java
|   |           ├── TokenQuickSort.java
|   |           └── TokenTreeVisitor.java
|   ├── testoracle
|   |   ├── lexer_test_suite_oracles.json
|   |   ├── parser_test_suite_oracles.json
|   |   └── semantic_test_suite_oracles.json
|   ├── test_lexer.py
|   ├── test_paser.py
|   ├── test_semantic.py
│   └── util.py
├── .gitignore
├── README.md
├── REPORTS.md
├── poetry.lock
└── pyproject.toml
```

O arquivo `ci.yml` descreve o workflow de integração contínua que é executado toda vez que um commit é feito no branch `main`. O diretório `pymjc` contém a estrutura básica do compilador, que se divide em `back` (**back end**), `front` (**front end**) e o ponto de entrada do compilador em si `run.py`. O arquivo `run.py` apresenta uma implementação inicial de como exeutar o compilador, veja a classe `MJCompiler` dentro dele. Dentro do diretório `front` deve fica a implementação dos módulos relacionados com o front end do compilador. Lá já se incontram implementações parciais do analisador léxico (veja a classe `MJLexer` dentro de `lexer.py`) e do analisador sinático (veja a classe `MJParser` dentro de `parser.py`). Além disso, os elementos para construção da árvore de sintaxe abstrata encontram-se no arquivo `ast.py`. Os módulos úteis para criação da tabela de símbolos encontram-se em `symbol.py` e os módulos úteis para o preenchimento da tabela de símblos e verificação semântica de tipos encontram-se em `visitor.py` (OBS. leia as instruções do arquivo `SemanticCheckings.pdf` dentro de `doc`).   

Toda parte de automação de testes está definido no diretório `tests`. Dentro do diretório `testdata` encontram-se programas escritos em MiniJava de forma correta (diretório `correct`) e incorreta (diretório `faulty`). Esses arquivos são utilizados para testar, de forma automática, o compilador em desenvolvimento. Os arquivos `lexer_test_suite_oracles.json`, `parser_test_suite_oracles.json` e `semantic_test_suite_oracles.json` dentro do diretório `testoracle` contém os oráculos de teste a serem confrontados com os resultados gerados pelo compilador em desenvolvimento. Os arquivos `test_lexer.py`, `test_paser.py` e `test_semantic.py` contém, respectivamente, testes unitários para testar os analizadores léxico, sintático e semântico. O arquivo `util.py` disponibiliza algumas funções utilitárias para os testes.

Por fim, os arquivos `poetry.lock` e `pyproject.toml` do [Poetry](https://python-poetry.org/) estão relacionados com build automatizado e gerenciamento de depenências do projeto. 

# Executando o Compilador
 
 O compilador pode ser executado via linha de comando usando o comando abaixo:

```
$ python -m pymjc.run <path-completo-do-arquivo-fonte>.java
```

ou via [Poetry](https://python-poetry.org/) (por questões de resolução de dependências):

```
$ poetry run python -m pymjc.run <path-completo-do-arquivo-fonte>.java
```

# Executando os Testes Automatizados
 
 Os testes automatizados podem ser executados via linha de comando usando o comando abaixo:

```
$ python -u -m unittest discover tests
```

ou via [Poetry](https://python-poetry.org/) (por questões de resolução de dependências):

```
$ poetry run python -u -m unittest discover tests
```
