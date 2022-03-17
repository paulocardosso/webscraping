"""
Projeto Web Scraping Usando Python/Selenium
Desenvolvidor por: Paulo Cardoso
Supermercados testados: Gbarbosa e Bigbompreço
"""

#usado para tempo de espera
import time
#usado para simular o navegador, neste caso o chrome
from selenium import webdriver
#usado para simular ações das teclas do teclado
from selenium.webdriver.common.keys import Keys

class Webscraping:
    #construtor que defini os atributos para realização do sistema
    def __init__(self):
        self.driver = []
        self.mercado = []
        self.site = []
        self.cep = ''
        self.produto = {
            "nome":"",
            "tipo":"",
            "marca":"",
            "tamanho":""
        }

    #fazerBusca método que vai pegar informações do usuário, como: a quantidade de mercados, nomes dos mercados, cep e produto
    def fazerBusca(self):
        #variavel para armazenar a quantidade de mercados
        qtd = ''
        #tratamento da variavel qtd, caso ela seja uma string e não um numero
        while type(qtd) is str:
            try:
                qtd = int(input('Informe a quantidade de supermercados que deseja fazer webscraping:\n'))
            except:
                print('Quantidade invalida! Informe uma quantidade numerica!')
        #vai pegar as informações do supermercado ao usuario, mediante a quantidade informada anteriormente
        for i in range(qtd):
            supermercado = str(input('Informe o nome do {}º Supermercado:\n'.format(i+1))).strip()
            #tratamento do supermercado bigbompreço, devido as suas variações de nomes
            if supermercado == 'bompreço' or supermercado == 'bompreco' or supermercado == 'bigbompreco':
                supermercado = 'bigbompreço'
            #armazena o nome do supermercado no array mercado da classe
            self.mercado.append(supermercado)
            #tratamento dos sites do supermercado
            if supermercado.upper() == 'GBARBOSA':
                site = 'https://www.delivery.gbarbosa.com.br/'
            elif supermercado.upper() == 'BIGBOMPREÇO':
                site = 'https://www.bompreco.com.br/'
            elif supermercado.upper() == 'OUTRO':
                # se tiver outro mercado disponivel, faça isso:
                    # coloca o nome do supermercado em caixa alta, no lugar da palavra OUTRO
                    # site = 'url do site do supermercado'
                    # remover o pass abaixo
                pass
            else:
                print('Supermercado inexistente! tente novamente')
            #armazena o site do supermercado no array site da classe
            self.site.append(site)
        #chama o metodo de informeCep, para pegar o cep do usuário e ao mesmo tempo validar o cep (sem caracteres)
        self.informeCep()
        # chama o metodo de informeProduto, para pegar informações do produto a ser pesquisado (nome, tipo, marca e tamanho)
        self.informeProduto()
        # chama o metodo para abrirNavegador, apos pegar todos os dados precisos para fazer a busca
        self.abrirNavegador()

    def informeCep(self):
        #armazena o cep informado pelo usuário
        cep = str(input('Informe o seu CEP: (Somente numeros, ex.: 99999999)\n')).strip()
        #trata o cep informado com base na quantidade de numeros (8 numeros) e na composição do cep (sem caracteres)
        while len(cep) != 8 or not cep.isnumeric():
            print('CEP INVALIDO! Tente Novamente')
            cep = str(input('Informe o seu CEP: (Somente numeros, ex.: 99999999)\n')).strip()
        #apos o tratamento, armazena o cep na variavel cep da classe
        self.cep = cep

    def informeProduto(self):
        #armazena todas as informações do produto, no dicionario produto da classe
        produtonome = str(input('Informe o produto que deseja procurar:\n')).strip()
        self.produto["nome"] = produtonome
        tipo = str(input('Informe o tipo do produto (Ex.: Tradicional, Forte, Fraco, etc):\n')).strip()
        self.produto["tipo"] = tipo
        marca = str(input('Informe a marca do produto (Ex.: Garoto, Nestlê):\n')).strip()
        self.produto["marca"] = marca
        tamanho = str(input('Informe o tamanho do produto (Ex.: 100g ou 1L):\n')).strip()
        self.produto["tamanho"] = tamanho

    def abrirNavegador(self):
        #vai abrir o navegador com base na quantidade de supermercados informados
        for i in range(len(self.site)):
            self.driver.append(webdriver.Chrome(executable_path="driver/chromedriver.exe"))
            self.driver[i].get(self.site[i])
        #apos aberto, vai registrar o Cep informado pelo usuário anteriormente
        self.registrarCep()

    #esse metodo vai verificar se o cep informado, existe no banco de dados de cada supermercado
    def verificaCep(self,i,mercado):
        #cada mercado tem uma forma diferente de analisar o cep
        if mercado == 'GBARBOSA':
            #a div vai capturar o texto, logo apos informa o cep que nao existe no sistema
            try:
                div = self.driver[i].find_element_by_css_selector('div.text-center.text-danger.ng-star-inserted')
            except:
                #se nao consegui armazenar a div, é pq existe o cep no sistema
                print('O CEP {} existe no banco de dados do {}'.format(self.cep,mercado))
            else:
                #se conseguiu armazenar a div, significa que o cep nao existe no sistema, informa isso ao usuário
                print('O CEP {} NÃO EXISTE NO BANCO DE DADOS DO SUPERMERCADO {}'.format(self.cep,mercado))
                #pede um novo cep ao usuário
                self.informeCep()
                #realiza todo o processo de inserção e verificação do novo cep
                input_cep = self.driver[i].find_element_by_id('cep')
                #realiza a limpeza do input, já que consta o cep antigo
                input_cep.clear()
                input_cep.send_keys(self.cep)
                time.sleep(6)  # Tempo de 6seg para carregar as opções de entrega
                #chama a verificação do cep, para analisar o novo cep
                self.verificaCep(i,mercado)
        elif mercado == 'BIGBOMPREÇO':
            #verifica se o cep existe no bd do bigbompreco
            try:
                texto = self.driver[i].find_element_by_id('stepText')
            except:
                #se existir entra no except
                print('O CEP {} existe no banco de dados do {}'.format(self.cep,mercado))
            else:
                #senao, entra aqui
                if 'não' in str(texto.text):
                    #exibi a mensagem de cep invalido
                    print('O CEP {} NÃO EXISTE NO BANCO DE DADOS DO SUPERMERCADO {}'.format(self.cep,mercado))
                    #fecha o modal
                    self.driver[i].find_element_by_css_selector('button.btn-close').click()
                    #pede o novo cep
                    self.informeCep()
                    #se o modal estiver fechado, abre o modal
                    try:
                        self.driver[i].find_element_by_css_selector('div.vtex-whitelabelCollapse').click()
                    except:
                        #se estiver já aberto, apenas informe o cep, dê enter e verifica o novo cep informado
                        input_cep = self.driver[i].find_element_by_css_selector('input.vtex-cep')
                        input_cep.send_keys(self.cep)
                        input_cep.send_keys(Keys.ENTER)
                        time.sleep(10)
                        self.verificaCep(i, mercado)
                    else:
                        #apos aberto o modal, limpa o input, informe o novo cep, dê enter e verifica o novo cep informado
                        time.sleep(3)
                        input_cep = self.driver[i].find_element_by_css_selector('input.vtex-cep')
                        input_cep.clear()
                        input_cep.send_keys(self.cep)
                        input_cep.send_keys(Keys.ENTER)
                        time.sleep(10)
                        self.verificaCep(i, mercado)
        elif mercado == 'OUTRO':
            #caso exista outro mercado, apague a palavra OUTRO e informe o nome em caixa alta do novo mercado
            #coloca todo o tratamento do cep aqui e removar o comando pass ao final
            pass
        else:
            print('ESTE MERCADO NÃO EXISTE EM NOSSO SISTEMA')

    #vai registrar o cep informado pelo usuário em cada supermercado informado
    def registrarCep(self):
        time.sleep(5) #tempo para carregar a pagina do supermercado
        for i in range(len(self.mercado)):
            #trata cada mercado informado, pois cada um tem um metodo diferente de registrar o cep
            if self.mercado[i].upper() == 'GBARBOSA':
                # click no botao de localização para abrir o modal e assim informar o cep
                self.driver[i].find_element_by_css_selector('button.btn.btn-warning.ng-star-inserted').click()
                #apos aberto o modal, captura o input que possui o id cep
                input_cep = self.driver[i].find_element_by_id('cep')
                #digita no input anterior, o cep informado pelo usuário
                input_cep.send_keys(self.cep)
                time.sleep(6)  # Tempo de 6seg para carregar as opções de entrega
                # chama o metodo para verificar se o cep existe no sistema do mercado, passando a posicao e o mercado como parametros
                self.verificaCep(i,self.mercado[i].upper())
                # se existe o cep, seleciona a opcao para entrega em domicilio
                input_cep.send_keys(Keys.TAB + Keys.ENTER)
                # confirma essa opção de entrega, clicando em confirmar
                self.driver[i].find_element_by_css_selector('button.btn.btn-success.ng-star-inserted').click()
            elif self.mercado[i].upper() == 'BIGBOMPREÇO':
                #o modal ja abre ao acessa o site, logo pegamos o input de cara
                input_cep = self.driver[i].find_element_by_css_selector('input.vtex-cep')
                #ao pegar input, digita o cep informado
                input_cep.send_keys(self.cep)
                #dê enter para confirmar o cep
                input_cep.send_keys(Keys.ENTER)
                time.sleep(10) #espera 10segundos para carregar a resposta do site
                #verifica se o cep existe, passando a posição e o nome do mercado
                self.verificaCep(i, self.mercado[i].upper())
            elif self.mercado[i].upper() == 'OUTRO':
                #Se ter outro mercado add informações de registro de cep neste campo, remover o pass ao final
                #Troca a palavra OUTRO pelo nome do mercado em caixa alta
                pass
            else:
                print('Supermercado inexistente em nosso sistema! Tente novamente!')
        time.sleep(3)
        self.verificarItensBuscados()

    #esse metodo vai buscarItem em cada supermercado informado, passando o produto como parametro
    def buscarItem(self,produto,tipo,marca,tamanho):
        for i in range(len(self.mercado)):
            #cada mercado tem uma forma diferente de fazer a busca
            if self.mercado[i].upper() == 'GBARBOSA':
                #captura o input de busca
                input_busca = self.driver[i].find_element_by_id('inputBuscaRapida')
            elif self.mercado[i].upper() == 'BIGBOMPREÇO':
                # tempo de 10seg para carrega a pagina por completo
                time.sleep(10)
                #encontrar o input do site bigbompreço, nao sendo pelo id, pois o id é mutavel
                div = self.driver[i].find_element_by_css_selector('div.vtex-store-components-3-x-autoCompleteOuterContainer--search-header')
                #captura o input de busca
                input_busca = div.find_element_by_tag_name('input')
            elif self.mercado[i].upper() == 'OUTRO':
                # Se ter outro mercado add funcionalidades de busca aqui
                pass
            else:
                print('Supermercado inexistente em nosso sistema! Tente novamente!')
            # chama o metodo criarPalavraPBusca, para cria a frase de busca
            frasebusca = self.criarPalavraPBusca(produto, tipo, marca, tamanho)
            # inserir a palavra criada anteriormente, no input
            input_busca.send_keys(frasebusca)
            # de enter para realizar a busca
            input_busca.send_keys(Keys.ENTER)

    #metodo vai criar a palavra de busca, mediante os parametros informados
    def criarPalavraPBusca(self,produto,tipo,marca,tamanho):
        frasebusca = ''
        if produto:
            frasebusca += '{}'.format(produto)
        if tipo:
            frasebusca += ' {}'.format(tipo)
        if marca:
            frasebusca += ' {}'.format(marca)
        if tamanho:
            frasebusca += ' {}'.format(tamanho)
        #retorna a palavra de busca criada
        return frasebusca.strip()

    #metodo que vai simular uma descida e uma subida na pagina informada, mediante o body passado como parametro
    def carregarPaginaDescidaSubida(self,body):
        #Descida rápida
        for c in range(20):
            #pressionando a tecla page down (20 vezes)
            body.send_keys(Keys.PAGE_DOWN)
        #Subida rápida
        for c in range(20):
            # pressionando a tecla page up (20 vezes)
            body.send_keys(Keys.PAGE_UP)

    def verificarItensBuscados(self):
        #cria uma lista para armazenar os dicionarios de itens encontrados
        listamercados = []
        #passa as informações do produto, para realizar a busca no metodo seguinte
        produto = self.produto["nome"]
        tipo = self.produto["tipo"]
        marca = self.produto["marca"]
        tamanho = self.produto["tamanho"]
        #chama o metodo de buscarItem, passando as informações do produto como parametro
        self.buscarItem(produto, tipo, marca, tamanho)
        #espera 3seg para carrega a respota da busca
        time.sleep(3)
        for i in range(len(self.mercado)):
            #para cada mercado cria um novo dicionario com itens encontrados
            itens = {
                "mercado": self.mercado[i],
                "nome": [],
                "valor": [],
                "valornum": []
            }
            #cada mercado tem um metodo diferente para capturar os itens encontrados
            if self.mercado[i].upper() == 'GBARBOSA':
                #captura todos os produtos encontrados apos ter feito a busca
                produtos = self.driver[i].find_elements_by_class_name('product')
                #percorre todos os produtos encontrados, para verificar o nome, o valor do mesmo e se está disponivel no mercado
                for x in produtos:
                    #armazena o nome do produto
                    nomeproduto = x.find_element_by_class_name('caption')
                    #variavel para verificar se o produto existe ou nao, se existe é pq tem a opção de comprar
                    verificaproduto = str(nomeproduto.text).split('\n')[1]
                    #realiza a verificacao, se existir realizar todas as etapas seguintes
                    if 'COMPRAR' in verificaproduto:
                        #capturar a valor do produto, existe produtos em promoção, logo possui class diferente, portanto, foi criada a excessão
                        try:
                            #se o produto estiver de promocao, vai capturar o valor promocional e executar o else
                            valor = x.find_element_by_css_selector('div.drill-price-md.text-success')
                        except:
                            #senao estiver de promocao vai capturar o valor nominal, sem executar o else a seguir
                            valor = x.find_element_by_css_selector('div.drill-price-md.text-danger')
                            valor1 = valor.find_element_by_css_selector('div.info-price')
                        else:
                            #executa somente se o produto estiver de promoção
                            valor1 = valor.find_element_by_css_selector('div.info-price.ng-star-inserted')
                        #variavel para compara com as informações do produto passada pelo usuário
                        nomecomp = str(nomeproduto.text).upper()
                        #verifica se todas as informações passada, consta no nome do produto, se sim executa todo o processo abaixo
                        if produto.upper() in nomecomp and tipo.upper() in nomecomp and marca.upper() in nomecomp and tamanho.upper() in nomecomp:
                            #add um novo produto, o valor em string e o valor float para realiza calculo do menor valor
                            itens["nome"].append(str(nomeproduto.text).split('\n')[0].strip())
                            itens["valor"].append(str(valor1.text).split('un.')[0].strip())
                            itens["valornum"].append(float(str(valor1.text).split('un.')[0].strip().split(' ')[1].replace(',','.')))
                # armazena o dicionario itens no array listamercados criado no inicio deste metodo
                listamercados.append(itens)
                #fecha o driver já que realizou todo o processo de busca e verificação
                self.driver[i].close()
            elif self.mercado[i].upper() == 'BIGBOMPREÇO':
                #pausa de 5seg para carregar o site
                time.sleep(5)
                # precisa carregar todos os produtos para isso, precisa descer a página e voltar
                body = self.driver[i].find_element_by_tag_name('body')
                self.carregarPaginaDescidaSubida(body)
                # apos carrega toda a pagina, capturar todos os produtos encontrados
                produtos = self.driver[i].find_elements_by_class_name('vtex-search-result-3-x-galleryItem')
                for x in produtos:
                    # capturar o nome de cada produto encontrado
                    nomeproduto = x.find_element_by_css_selector('span.vtex-product-summary-2-x-productBrand')
                    # variavel para compara com as informações do produto passada pelo usuário
                    nomecomp = str(nomeproduto.text).upper()
                    # verifica se o produto existe, se sim vai capturar o preço do mesmo
                    if nomecomp:
                        preco = x.find_element_by_css_selector('span.vtex-productShowCasePrice')
                    # verifica se todas as informações passada, consta no nome do produto, se sim executa todo o processo abaixo
                    if produto.upper() in nomecomp and tipo.upper() in nomecomp and marca.upper() in nomecomp and tamanho.upper() in nomecomp:
                        # add um novo produto, o valor em string e o valor float para realiza calculo do menor valor
                        itens["nome"].append(str(nomeproduto.text).strip())
                        itens["valor"].append(str(preco.text).strip())
                        itens["valornum"].append(float(str(preco.text).strip().split(' ')[1].replace(',', '.')))
                # armazena o dicionario itens no array listamercados criado no inicio deste metodo
                listamercados.append(itens)
                # fecha o driver já que realizou todo o processo de busca e verificação
                self.driver[i].close()
            elif self.mercado[i].upper() == 'OUTRO':
                # Se ter outro mercado add funcionalidades de verificacao aqui
                pass
            else:
                print('Supermercado inexistente em nosso sistema! Tente novamente!')
        #chama o metodo de exibir os resultados encontrados
        self.exibirResultados(listamercados)

    #esse metodo apenas atribui informações do menor valor, tais como: mercado, produto, valor
    def atribuirMenorValor(self,valorbarato,valormaisbarato,mercado,produto,valor):
        valorbarato[0] = mercado
        valorbarato[1] = valormaisbarato
        valorbarato[2] = produto
        valorbarato[3] = valor

    #exibi o supermercado com o valor do produto buscado mais economico
    def mostrarMaisBarato(self,valorbarato):
        print('=======SUPERMERCADO COM O PRODUTO MAIS BARATO:========')
        print(valorbarato[0].upper())
        print('Produto: ' + valorbarato[2])
        print('Valor: ' + valorbarato[3])
        print('======================================================\n')

    #mostra todos os possiveis resultados
    def exibirResultados(self,listam):
        #armazena a frase buscada
        frasebusca = self.criarPalavraPBusca(self.produto["nome"],self.produto["tipo"],self.produto["marca"],self.produto["tamanho"])
        # um array para armazena informações do produto mais barato
        valorbarato = ["", 0.0, "", ""]
        #uma variavel para saber se é para mostrar o supermercado mais barato ou nao
        mostrarbarato = False
        #percorre todos os resultados encontrados, na lista de dict
        for i in range(len(listam)):
            print('===========SUPERMERCADO:================')
            #exibi o nome de cada supermercado pesquisado
            print(listam[i]["mercado"].upper())
            print('========RESULTADO DA BUSCA:=============')
            #exibi o que foi buscado e quantos resultado foram encontrados
            print('Buscar por: {}'.format(frasebusca))
            # se existe resultados mostrar a quantidade de produtos pesquisados e verificados
            if len(listam[i]["nome"]) > 0:
                print('Foram encontrados: {} produtos'.format(len(listam[i]["nome"])))
                print('=======PRODUTO MAIS BARATO:=============')
                #captura o valor mais barato
                valormaisbarato = min(listam[i]["valornum"])
                #captura a posição do valor mais barato
                pos = listam[i]["valornum"].index(valormaisbarato)
                #mostra o produto e o valor mais barato no mercado informado
                print('Produto: ' + listam[i]["nome"][pos])
                print('Valor: ' + listam[i]["valor"][pos])
                print('========================================\n')
                #se for pesquisado em mais de um mercado, vai mostrar o mercado mais barato
                if len(listam) > 1:
                    #atribui a variavel true para mostrar o mercado mais barato
                    mostrarbarato = True
                    #realiza a verificação e atribuição do menor valor encontrado
                    if i == 0:
                        self.atribuirMenorValor(valorbarato,valormaisbarato,listam[i]["mercado"],listam[i]["nome"][pos],listam[i]["valor"][pos])
                    elif valormaisbarato < valorbarato[1]:
                        self.atribuirMenorValor(valorbarato,valormaisbarato,listam[i]["mercado"],listam[i]["nome"][pos],listam[i]["valor"][pos])
            else:
                #senao existe resultado, mostra as possiveis causas que nao foi encontrado
                mostrarbarato = False
                print('NÃO FORAM ENCONTRADOS RESULTADOS')
                print('===========POSSIVEIS CAUSAS:============')
                if self.produto["nome"]:
                    print('O produto {} não existe ou\nestá escrito de maneira diferente no\nsupermercado {}.'.format(
                        self.produto["nome"], listam[i]["mercado"]))
                if self.produto["tipo"]:
                    print('O tipo {} não existe ou\nestá escrito de maneira diferente no\nsupermercado {}.'.format(
                        self.produto["tipo"], listam[i]["mercado"]))
                if self.produto["marca"]:
                    print('A marca {} não existe ou\nestá escrito de maneira diferente no\nsupermercado {}.'.format(
                        self.produto["marca"], listam[i]["mercado"]))
                if self.produto["tamanho"]:
                    print('O tamanho {} não existe ou\nestá escrito de maneira diferente no\nsupermercado {}.'.format(
                        self.produto["tamanho"], listam[i]["mercado"]))
                print('========================================\n')
        if mostrarbarato:
            #chama o metodo para exibir o mercado mais barato
            self.mostrarMaisBarato(valorbarato)

if __name__ == '__main__':

    webscraping = Webscraping()
    webscraping.fazerBusca()