import copy

import networkx as nx
from matplotlib import pyplot as plt

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.productList = DAO.getAllProduct()
        self.productMap = {}
        self.salesList = DAO.getAllSales()

        self.colors = set()

        for p in self.productList:
            self.colors.add(p.Product_color)
            self.productMap[p.Product_number] = p

        self.selected_products = None
        self.solBest = []
        self.bestPeso_per_len = []

    def Create_Graph(self, color, year):
        self.grafo.clear()
        self.selected_products = DAO.getAllProduct_byColor(color)
        self.grafo.add_nodes_from(self.selected_products)

        for p1 in self.grafo.nodes:
            for p2 in self.grafo.nodes:
                #if self.check_day(p1, p2, year):
                if p1 != p2:
                    peso = DAO.get_peso(p1.Product_number, p2.Product_number, year)
                    if peso > 0:
                        print(f"{p1.Product_number}-{p2.Product_number} peso: {peso}")
                        self.grafo.add_edge(p1, p2, weight=peso)

    def getTop3(self):
        top3 = []
        setEdge = set()
        for u, v in self.grafo.edges:
            setEdge.add((u, v, self.grafo[u][v]['weight']))
        print(setEdge)
        for i in range(3):
            top = max(setEdge, key=lambda x: x[2])
            top3.append(top)
            setEdge.remove(top)

        return top3

    def check_day(self, p1, p2, year):
        vendite1 = []
        vendite2 = []
        for sale in self.salesList:
            if sale.Product_number == p1.Product_number and sale.Date.year == year:
                vendite1.append(sale)
        for sale in self.salesList:
            if sale.Product_number == p2.Product_number and sale.Date.year == year:
                vendite2.append(sale)

        for s1 in vendite1:
            for s2 in vendite2:
                if s1.Product_number != s2.Product_number and s1.Retailer_code == s2.Retailer_code and s1.Date.day == s2.Date.day:
                    return True

        return False

    def Nnodes(self):
        return len(self.grafo.nodes)

    def Nedges(self):
        return len(self.grafo.edges)

    def find_path(self, product_num):
        self.solBest = []
        self.bestPeso_per_len = [1e16 for i in range(len(self.grafo.edges))]

        product = self.productMap[product_num]

        for nodo in nx.neighbors(self.grafo, product):
            peso = self.grafo[product][nodo]['weight']
            self.ricorsione([(product, nodo, peso)], False, peso)

        '''grafoTemp = nx.Graph(self.grafo.edges(data=True))
        labels = nx.get_edge_attributes(grafoTemp, 'weight')
        pos = nx.spring_layout(grafoTemp)

        nx.draw(grafoTemp, with_labels=True, pos=pos)
        nx.draw_networkx_edge_labels(grafoTemp, pos, edge_labels=labels)
        plt.savefig('Grafo')
        plt.show()

        soluzione = nx.Graph()
        for tuple in self.solBest:
            soluzione.add_edge(tuple[0], tuple[1], weight=tuple[2])
        labels = nx.get_edge_attributes(soluzione, 'weight')
        pos = nx.spring_layout(soluzione)

        nx.draw(soluzione, with_labels=True, pos=pos)
        nx.draw_networkx_edge_labels(soluzione, pos, edge_labels=labels)
        plt.savefig('Soluzione')
        plt.show()'''

    def ricorsione(self, parziale, finito, bestPeso):
        ultimonodo = parziale[-1][1]

        if self.bestPeso_per_len[len(parziale)] < bestPeso:
            return

        if finito:
            if len(parziale) > len(self.solBest):
                self.solBest = copy.deepcopy(parziale)
                print(f"Lunga : {self.solBest.__len__()} {self.solBest}")
        else:
            for nodo in self.grafo.neighbors(ultimonodo):
                peso = self.grafo[ultimonodo][nodo]['weight']
                if peso >= bestPeso and self.check(ultimonodo, nodo, parziale):
                    parziale.append((ultimonodo, nodo, peso))
                    print(peso)
                    if peso < self.bestPeso_per_len[len(parziale)]:
                        self.bestPeso_per_len[len(parziale)] = peso
                    self.ricorsione(parziale, False, peso)
                    parziale.pop()
                else:
                    self.ricorsione(parziale, True, bestPeso)

    def get_maxPeso(self, parziale):
        return max(parziale, key=lambda x: x[2])

    def check(self, ultimonodo, nodo, parizale):
        for tupla in parizale:
            if tupla[:-1] == (ultimonodo, nodo) or tupla[:-1] == (nodo, ultimonodo):
                return False
        return True
