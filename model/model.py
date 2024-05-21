import networkx as nx

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

    def Create_Graph(self, color, year):
        self.selected_products = DAO.getAllProduct_byColor(color)
        self.grafo.add_nodes_from(self.selected_products)

        for p1 in self.grafo.nodes:
            for p2 in self.grafo.nodes:
                if self.check_day(p1, p2, year):
                    peso = DAO.get_peso(p1.Product_number, p2.Product_number, year)[0][0]
                    print(peso)
                    self.grafo.add_edge(p1, p2, weight=peso)




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
                if s1.Product_number == s2.Product_number and s1.Retailer_code != s2.Retailer_code and s1.Date.day == s2.Date.day:
                    return True

        return False

    def Nnodes(self):
        return len(self.grafo.nodes)

    def Nedges(self):
        return len(self.grafo.edges)

