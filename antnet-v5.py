# -*- coding: utf-8 -*-
"""
@autor: Antonio Russoniello
"""

import networkx as nx
import matplotlib.pyplot as plt
import random


############ VARIAVEIS GLOBAIS ################
#cenarios bem-sucedidos: 500 formigas e 10 nos, 700 formigas e 20 nos
#num_formigas = 100 #recomendado por Dorigo num_formigas = n^50 n=comprimento do percurso
num_formigas = 700
nodo_origem = 1
alfa = 2 # importancia de feromonios
beta = 3 # peso das distancias (maior distancia = maior custo = pior caso))
# ciclo_execucao = 100
ciclo_execucao = 200
tau_inicial = 0.01
tau_incr = 0.10
#num_nodos = 10 # numero de Nos
num_nodos = 20
nodo_destino = num_nodos - 1


############ CLASSE FORMIGAS ################
class Formigas:

    def __init__(self, grafo, indice_formiga, nodo_atual):
        self.indice = indice_formiga
        self.grafo = grafo
        self.nodo_atual = nodo_atual
        self.ttl = num_formigas * ciclo_execucao
        self.nodos_visitados = []
        self.nodos_visitados.append(nodo_atual)
        self.laco = False
        
    def quem_sou(self):
        if(self.nodo_atual != nodo_destino):   
            print('sou formiga: ', self.indice)
            print('estou no no: ', self.nodo_atual)
            print('vizinhos do no atual: ', self.grafo.edges(self.nodo_atual))
        else:
            print('sou formiga: ', self.indice)
            print('cheguei ao destino: ', self.nodo_atual)
            #print('sou uma formiga morta :-)')
            print('meus nos visitados sao: ', self.nodos_visitados)
            self.ttl = 1
        if (self.laco):
            print('estou presa em um laco')
            
        
    def proximo_nodo(self):
        while (self.nodo_atual != nodo_destino):
            self.lista_prob = []
            self.lista_prob2 = []
            self.rango_prob = []
            self.sumatoria = 0
            self.arestas = self.grafo[self.nodo_atual]
            #print('no atual ', self.nodo_atual)
            self.nodos_vizinhos = self.arestas.keys() 
            #print(len(self.arestas))
            print('vizinhos ', self.nodos_vizinhos)
            self.nodos_vizinhos = self.eliminar_repeticoes(self.nodos_vizinhos, self.nodos_visitados)
            if (len(self.nodos_vizinhos) == 0):
                self.laco = True
                print('estou presa em um laco')                
                break            
            for i in range(len(self.nodos_vizinhos)):
                self.feromonio = self.grafo[self.nodo_atual][self.nodos_vizinhos[i]]['tau']
                self.distancia = self.grafo[self.nodo_atual][self.nodos_vizinhos[i]]['distancia']
                print('++++++++++  no %i  ++++++++++++' % self.nodos_vizinhos[i])
                print('++      feromonio %f '      % self.feromonio)
                print('++      distancia %f '     % self.distancia)
                #self.prob = ((self.feromonio)**alfa)*((self.distancia)**beta) # para favorecer distancias grandes
                self.prob = ((self.feromonio)**alfa)*((1-self.distancia)**beta) #para favorecer distancias pequenas
                if (self.prob == 0):
                    self.prob = 0.01 
                print('++      probabilidade %f '  % self.prob)
                
                self.sumatoria = self.sumatoria + self.prob
                #print(self.grafo.edges(self.indice))
                #print('somatoria; ', self.sumatoria)
                self.lista_prob.append(self.prob)
            for i in range(0, len(self.nodos_vizinhos)):
                #print(lista_prob[i])
                self.lista_prob2.append(round((self.lista_prob[i]/self.sumatoria),5))
                if (i == 0):
                    self.rango_prob.append([0,self.lista_prob2[i]])
                    self.rango_inf = self.lista_prob2[i]
                else:
                    self.rango_sup = self.rango_inf + self.lista_prob2[i]
                    self.rango_prob.append([self.rango_inf, self.rango_inf + self.lista_prob2[i]])
                    self.rango_inf = self.rango_inf + self.lista_prob2[i]
            print('+++++++++++++++++++++++++++++++++')
            print('probabilidade por aresta: ', self.lista_prob2)
            print('faixa de probabilidades: ', self.rango_prob)
            self.valor_aleatorio = random.uniform(0,1)
            print('valor aleatorio: ', self.valor_aleatorio)
        
            for j in range(len(self.nodos_vizinhos)):
                self.nodo_atual = j
                if ((self.valor_aleatorio >= self.rango_prob[j][0]) & (self.valor_aleatorio <= self.rango_prob[j][1])):
                    break               

            print('proximo no a visitar: ', self.nodos_vizinhos[self.nodo_atual])
            
            self.nodos_visitados.append(self.nodos_vizinhos[self.nodo_atual])
            print('nos visitados: ', self.nodos_visitados)
            self.nodo_atual = self.nodos_vizinhos[self.nodo_atual]
            return            
    
    def atualizar_feromonios(self):
        soma_distancias = 0
        for i in range(0, len(self.nodos_visitados)-1):
            print('aresta %s <-> %s: ' % (self.nodos_visitados[i], self.nodos_visitados[i+1]))
            print('tau: ', self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['tau'])
            # somar todos os custos da rota e o inverso sera o tau incremental aplicado a cada aresta
            print('distancia: ',  self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['distancia'])
            soma_distancias = soma_distancias + self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['distancia']          
        # atualizacao de feromonios para a rota    
        #print(soma_distancias)
        delta_tau = 1/soma_distancias
        for i in range(0, len(self.nodos_visitados)-1):
            tau_atual = self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['tau']
            self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['tau'] = round((tau_atual + delta_tau), 2)
        print('tau atualizado: ', self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['tau'])
        return
        
    def eliminar_repeticoes(self, nodos_ve, nodos_vi):
        self.vizinho = set(nodos_ve)
        self.visitado = set(nodos_vi)
        self.conjunto = self.vizinho - self.visitado
        print('lista de nos sem repeticoes ', list(self.conjunto))
        return list(self.conjunto)
        
    def tempo_vida(self):
        if (self.ttl > 1):        
            self.ttl = self.ttl - 1
            #print('tempo restante de vida: ', self.ttl)
        return self.ttl
    
    def formiga_volta():
        return

############ GRAFICAR GRAFO ################
def graficar_grafo(grafo, etiquetas, layout_grafo, cor_nodo, cor_aresta):
    tamanho_nodo = 350
    alfa_nodo = .8
    tamanho_texto_nodo = 12
    alfa_aresta = .5
    espessura_aresta = 3
    #pos_texto_aresta = 0.3
    fonte_texto = 'sans-serif'
    # estes sao diferentes layouts para a rede que voce pode tentar
    # shell parece funcionar melhor
    if layout_grafo == 'spring':
        pos_grafo = nx.spring_layout(G)
    elif layout_grafo == 'spectral':
        pos_grafo = nx.spectral_layout(G)
    elif layout_grafo == 'random':
        pos_grafo = nx.random_layout(G)
    else:
        pos_grafo = nx.shell_layout(G)    
    # desenhar grafo
    nx.draw_networkx_nodes(grafo, pos_grafo, node_size=tamanho_nodo, alpha=alfa_nodo, node_color=cor_nodo)
    nx.draw_networkx_edges(grafo, pos_grafo, width=espessura_aresta, alpha=alfa_aresta, edge_color=cor_aresta)
    nx.draw_networkx_labels(grafo, pos_grafo, font_size=tamanho_texto_nodo, font_family=fonte_texto)
    for aresta in grafo.edges():
        dici = {aresta: grafo.edge[aresta[0]][aresta[1]]['distancia']}
        nx.draw_networkx_edge_labels(grafo, pos_grafo, dici, label_pos=0.3)
    plt.axis('off')    
    plt.show()

           
########################## INICIO ############################################
# criar grafo com atributo etiqueta
G = nx.Graph(etiqueta="grafo")
G.add_nodes_from(range(1,num_nodos+1))

# Gerar Grafo com distancias conhecidas para DEBUG
#for i in range(1,num_nodos+1):
#    for s in range(1,3):    
#        G.add_edge(i,random.randint(1,num_nodos), distancia=0.1, tau=round(tau_inicial, 2))
#        etiquetas = (chr, range(1,num_nodos))


# Gerar Grafo com valores aleatorios de distancia
for i in range(1,num_nodos+1):
    for s in range(1,3):       # garante de dois a tres nos conectados
        G.add_edge(i,random.randint(1,num_nodos), distancia=round(random.uniform(0,1),2), tau=tau_inicial)
        etiquetas = (chr, range(1,num_nodos))

print('Componentes conectados:')
print(sorted(nx.connected_components(G), key = len, reverse=True))
#print('grau do ultimo no:', G.degree(num_nodos)) # mostrar grau do ultimo elemento
#print('arestas do ultimo no:', G.edges(num_nodos)) # mostrar arestas do ultimo no


# Graficar grafo
#graficar_grafo(G,etiquetas=True, layout_grafo='shell', cor_nodo='red', cor_aresta='green')

# Definir Rota a otimizar
#nodo_origem = raw_input('No origem: ')
#nodo_destino= raw_input('No destino: ')
#rota_corta = nx.shortest_path(G, source=int(nodo_origem), target=int(nodo_destino))
#print('rota mais curta: ', rota_corta, '\n')
for i in range(1, len(G)+1):
    print('No:', i)
    print('Nos Adjacentes: ', G[i])
    
print('\nInicio de Colonia de Formigas')
print('Quantidade de Formigas: ', num_formigas)
# criar lista de formigas
formigas_lista = [Formigas(G, i, nodo_origem) for i in range(num_formigas)]

ciclos = 0
while (ciclos < ciclo_execucao):
    for i in range(len(formigas_lista)):
        print('================================================')    
        formigas_lista[i].quem_sou()    
        formigas_lista[i].proximo_nodo()
        formigas_lista[i].tempo_vida()
    print('\n* Resultados Parciais:')
    for i in range(1, len(formigas_lista)):
        if (formigas_lista[i].laco == False):
            print('\nformiga %i atualizando feromonio para nos visitados: %s' % (i, formigas_lista[i].nodos_visitados))
            formigas_lista[i].atualizar_feromonios()
       
    ciclos += 1

print('\n* Resultados Finais:')

lista_rotas = []
lista_rotas_unicas = []
contar_rota = 0
for i in range(1, len(formigas_lista)):
    if (formigas_lista[i].laco == False):
        print('\nformiga %i rota: %s' % (i, formigas_lista[i].nodos_visitados))
        contar_rota = lista_rotas.count(formigas_lista[i].nodos_visitados)
        lista_rotas.append(formigas_lista[i].nodos_visitados)    
        if ( contar_rota > 0):
            rota_existe_bandeira = True
        else:
            rota_existe_bandeira = False
            lista_rotas_unicas.append(formigas_lista[i].nodos_visitados)
print('\n')
custo_rota = 0
lista_custos = []
for rota in lista_rotas_unicas:
    print('rota %s selecionada %s vezes' % (rota, lista_rotas.count(rota)))
    for i in range(0, len(rota)-1):
        custo_rota = custo_rota + G[rota[i]][rota[i+1]]['distancia']
    lista_custos.append(round(custo_rota,2))
    print('custo rota %s igual a %s ' % (rota, custo_rota))
    indice = lista_custos.index(min(lista_custos))

print('\na rota %s tem o menor custo (%s) ' % (lista_rotas_unicas[indice], min(lista_custos)))
       
#   lista_rotas.count(lista_rotas_unicas[0])

#        if (lista_rotas.count(formigas_lista[i].nodos_visitados) == 0):
#            continue
#        else:
#            lista_rotas.append(formigas_lista[i].nodos_visitados)
