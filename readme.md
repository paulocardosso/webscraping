# Projeto Web Scraping Usando Python/Selenium

## Introdução

Com a alta inflação que estamos vivenciando nos dias atuais, 
uma economia a mais no final do mês, sempre é bem-vinda.
Portanto, o presente projeto têm por objetivo principal gerar 
essa economia extra ao realizar compras nos supermercados, 
fazendo comparações de preços em cada supermercado informado, 
chegando assim a uma solução mais economica para o usuário final. 

## Objetivo do Projeto

1. Verificar preços de um determinado produto em sites de supermercados 
da região, que são informados pelo URL
    1. Pedir ao usuário a quantidade de supermercados que deseja buscar
        1. Exemplo de resposta numerica: `1`
    1. Informar o nome de cada supermercado
        1. Exemplo de resposta: `gbarbosa`
    1. Pedir ao usuário o CEP do seu endereço:
        1. Exemplo de CEP (sem hifen): `99999999`
    1. Pedir ao usuário qual produto deseja procurar
        1. Além do produto, o usuário deve informar o tipo, a marca e o 
        tamanho para uma busca mais precisa
    1. Registrar o CEP informado no site do supermercado através da automação
        1. Click no button da localização no site do supermercado
        1. Click no input para digitar o cep
        1. Digitar o cep no input selecionado
        1. Confirmar o cep e a forma de entrega (caso exista essa opção)
    1. Verificar o resultado da busca
        1. Verificar se o resultado possui informações coerentes com o produto buscado
        1. Todo resultado coerente com a busca, será armazena em um dicionario, 
        com o nome do produto e o valor do mesmo    
1. Informar o menor preço do produto pesquisado em cada supermercado informado, 
para o usuário ter uma economia ao realizar a compra de determinado produto 

## Metodologia

O projeto será baseado em uma programação orientada a objetos (POO), usando a 
linguagem Python juntamente com a biblioteca Selenium. Inicialmente, será criada 
a classe: **Webscraping**. Essa classe possui os seguintes atributos: **Driver** (um array para
armazenar cada objeto criado para simulação do navegador), **mercado** (um array para armazenar os
nomes do supermercados informado pelo usuário), **site** (um array para armazenar os sites de
cada supermercado informado), **cep** (uma string para armazenar o cep do usuário) e o **produto**
(um dicionario, para armazenar todas as informações do produto: nome, tipo, marca e tamanho). 
A classe **Webscraping** possui os métodos: **fazerBusca()** (método de partida, onde será
realizado um questionário ao usuário a respeito da busca: quantidade de mercados, nomes do
mercados, cep do usuário e o produto que deseja procurar), **informeCep()** (método para o 
usuario informar o cep e ao mesmo tempo tratar essa variavel (validação)), **informeProduto()**
(método para armazenar as informações do produto), **abrirNavegador()** (método realiza a 
abertura do(s) navegador(es)), **registraCep()** (método vai inserir o cep do usuário nos sites
dos supermercados informado pelo usuário), **verificaCep()** (método vai verificar/validar se 
o cep do usuário existe no sistema do supermercado), **buscarItem()** (método vai realizar a 
busca do produto informado nos sites dos supermercado informado), **criarPalavraPBusca()**
(método vai gerar uma palavra a ser buscada no método buscarItem), **verificarItensBuscados()**
(método vai gerar uma lista de dicionario, contendo todos os produtos encontrado
de cada supermercado referente ao termo buscado), **carregarSubidaDescida()** (método para
carregar a pagina, realizando a descida e a subida da página), **atribuirMenorValor()**
(método para fazer atribuiçao do menor valor), **mostrarMaisBarato()** (método vai 
exibir o supermercado que possui o produto buscado com o menor valor),
**exibirResultado()** (método vai mostrar todos os possiveis resultados, independente
se o produto buscado foi encontrado ou não, caso não encontre sera informado as possiveis
causas) e o **construtor()** (método que associa os tipos a cada atributo informado).
Este projeto foi baseado em dois supermercados da região de Vitória da Conquista(BA)
Gbarbosa e o Bigbompreço, mas foi deixado espaços para novos supermercados. Os 
tempos de espera é somente para carregamento da pagina, que vai depender da velocidade
de acesso aos sites.

## Resultados

Foram realizado vários testes, exibidos logo abaixo:

> 1º Teste: Ao executar o arquivo "webscraping.py", carregamos as variaveis de entrada
e o obtemos a seguinte saída, com apenas um supermercado
>>**Entradas:**\
>>`qtd = 1`\
>>`supermercado = gbarbosa`\
>>`cep = 45028742`\
>>`produto = café`\
>>`tipo = `\
>>`marca = `\
>>`tamanho = 250g`
>
>>**Saída:**\
>>`===========SUPERMERCADO:===========`\
>>`GBARBOSA`\
>>`========RESULTADO DA BUSCA:========`\
>>`Buscar por: café 250g`\
>>`Foram encontrados: 32 produtos`\
>>`=======PRODUTO MAIS BARATO:========`\
>>`Produto: Café Moído Losango 250g`\
>>`Valor: R$ 6,99`\
>>`===================================`

> 2º Teste: Ao executar o arquivo "webscraping.py", carregamos as variaveis de entrada
e o obtemos a seguinte saída, agora com dois supermercados
>>**Entradas:**\
>>`qtd = 2`\
>>`supermercado 1 = gbarbosa`\
>>`supermercado 2 = bigbompreço`\
>>`cep = 45028742`\
>>`produto = café`\
>>`tipo = `\
>>`marca = `\
>>`tamanho = 250g`
>
>>**Saída:**\
>>`===========SUPERMERCADO:===========`\
>>`GBARBOSA`\
>>`========RESULTADO DA BUSCA:========`\
>>`Buscar por: café 250g`\
>>`Foram encontrados: 32 produtos`\
>>`=======PRODUTO MAIS BARATO:========`\
>>`Produto: Café Moído Losango 250g`\
>>`Valor: R$ 6,99`\
>>`===================================`
>>
>>`===========SUPERMERCADO:===========`\
>>`BIGBOMPREÇO`\
>>`========RESULTADO DA BUSCA:========`\
>>`Buscar por: café 250g`\
>>`Foram encontrados: 27 produtos`\
>>`=======PRODUTO MAIS BARATO:========`\
>>`Produto: Café Torrado e Moído Tradicional Confiare Pacote 250g`\
>>`Valor: R$ 6,29`\
>>`===================================`
>>
>>`=====SUPERMERCADO MAIS BARATO:=====`\
>>`BIGBOMPREÇO`\
>>`Produto: Café Torrado e Moído Tradicional Confiare Pacote 250g`\
>>`Valor: R$ 6,29`\
>>`===================================`

> 3º Teste: Ao executar o arquivo "webscraping.py", carregamos as variaveis de entrada
e o obtemos a seguinte saída, agora com cep invalido pelo sistema do supermercado
>>**Entradas:**\
>>`qtd = 1`\
>>`supermercado 1 = gbarbosa`\
>>`cep = 99999999`\
>>`produto = café`\
>>`tipo = `\
>>`marca = `\
>>`tamanho = 250g`
>
>>**Saída:**\
>>`O CEP 99999999 NÃO EXISTE NO BANCO DE DADOS DO SUPERMERCADO GBARBOSA`\
>>`Informe o seu CEP: (Somente numeros, ex.: 99999999)`\

> 4º Teste: Ao executar o arquivo "webscraping.py", carregamos as variaveis de entrada
e o obtemos a seguinte saída, agora com um produto inexistente no supermercado informado
>>**Entradas:**\
>>`qtd = 1`\
>>`supermercado 1 = gbarbosa`\
>>`cep = 45028742`\
>>`produto = revolver`\
>>`tipo = `\
>>`marca = `\
>>`tamanho = `
>
>>**Saída:**\
>>`===========SUPERMERCADO:===========`\
>>`GBARBOSA`\
>>`========RESULTADO DA BUSCA:========`\
>>`Buscar por: revolver`\
>>`NÃO FORAM ENCONTRADOS RESULTADOS`\
>>`=======POSSSIVEIS CAUSAS:========`\
>>`O produto revolver não existe ou`\
>>`está escrito de maneira diferente`\
>>`no supermercado gbarbosa.`\
>>`===================================`

## Discussão

O presente trabalho apresentou um resultado satisfatório. Entretanto, várias melhorias
podem ser implementadas para a questão de perfomance do sistema e também versões mais 
complexas, onde o sistema poderá realizar uma feira completa em varios supermercados
e por fim chegar a um resultado mais economico, incluindo o valor do frete dos supermercados 
informados.

## Anexo

Todas as informações referente ao sistema, estarão nos comentários antes de cada linha de código.
Para maiores informações, entre em contato

## Referências

1. Python
    1. https://www.python.org/
1. Selenium-python
    1. https://selenium-python.readthedocs.io/