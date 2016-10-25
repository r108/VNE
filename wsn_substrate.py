import networkx as nx

class WSN():

    __WSN_Nodes = nx.Graph()
    __WSN_Links = nx.Graph()
    __links = dict()
    __adj_list = {}
    __interference_list = dict()

    def __init__(self):
        self.init_wsn_substrate(self.get_adjacency_list())
        self.init_interference(self.get_adjacency_list())

    def get_links(self):
        return self.__links

    def get_wsn_links(self):
        return self.__WSN_Links

    def get_wsn_nodes(self):
        return self.__WSN_Nodes

    def get_interferences(self):
        return self.__interference_list

    def init_interference(self, adj_list):
        for n in adj_list:
            items = adj_list.get(n)
            if_list = []
            if_list.extend(items)
            for i in items:
                if_list.extend(adj_list.get(i))
            self.__interference_list[n] = list(set([x for x in if_list if x != n]))
        #print("Interferences ",self.__interference_list)

    def init_wsn_substrate(self, links):
        print
        adj_list = links
        for n in adj_list:
            #print(n)
            self.__WSN_Nodes.add_node(n, {'rank':1, 'load':1, 'degree':len(links[n])})
            #self.__WSN_Nodes.add
            #self.__WSN_Nodes[n]['rank'] = 1
            #self.__WSN_Nodes[n]['load'] = 1
            #self.__WSN_Nodes[n]['degree'] = len(links[n])
            items = adj_list.get(n)
            for i in items:
                str = n,i
                rts = i,n
                if str in self.__links.keys():
                    #print(str," already added")
                    pass
                elif rts in self.__links.keys():
                    #print("already added ",rts)
                    pass
                else:
                    #print(str,rts)
                    self.__links[(n, i)] = 1
                    #self.__WSN_Links.add_edge(n, i)
                    #self.__WSN_Links[n][i]['plr'] = 1
                    #self.__WSN_Links[n][i]['load'] = 1
                    #weighted_link = LinkCost(G[u][v]['plr'], G[u][v]['load'])
                    #self.__WSN_Links[n][i]['weight'] = 1 #weighted_link.get_weight(weighted_link)
                    self.__WSN_Links.add_edge(n,i, {'plr':1, 'load':1, 'weight':1})




    #def get___WSN_Links():
    def get_wsn_substrate(self):
        weight = {(1, 2): 100,
                   (1, 3): 9,
                   (1, 6): 180,
                   (2, 3): 10,
                   (2, 4): 15,
                   (3, 4): 11,
                   (3, 6): 20,
                   (4, 5): 6,
                   (5, 6): 9,
                   (4, 7): 2,
                   (5, 7): 1,
                   (6, 7): 12}

        weight2 = {(1, 2): 1,
                   (1, 4): 1,
                   (1, 5): 1,
                   (2, 3): 1,
                   (3, 4): 1,
                   (4, 5): 1,
                   (5, 6): 1,
                   (6, 7): 1, }

        return weight

    def update_adj_list(self, adj_list):
        self.__adj_list = adj_list

    def get_adjacency_list(self):
        adj_list2 = {1: [2, 4, 5],
                  2: [1, 3],
                  3: [2, 4],
                  4: [3, 5],
                  5: [4, 6],
                  6: [5, 7],
                  7: [6]}

        self.__adj_list2 = {1: [2, 3, 6],
                 2: [1, 3, 4],
                 3: [1, 2, 4, 6],
                 4: [2, 3, 5, 7],
                 5: [4, 6, 7],
                 6: [1, 3, 5, 7],
                 7: [4, 5, 6]}

        self.__adj_list = {1: [2,4,8],
               2: [1, 5, 4, 6],
               3: [7, 6],
               4: [1, 2, 5, 8],
               5: [2, 4, 6, 9],
               6: [2, 3, 5, 7, 9],
               7: [3, 6, 11],
               8: [1, 4, 10],
                9:[5, 6, 10, 11],
                10:[8, 9, 11],
                11:[7, 9, 10, 12],
                12:[11]}

        return self.__adj_list
    def get_nodes_position(self):

        position = {1:(1.2,-1.2),
        2:(1.1,-0.6),
        3:(1.2,1.2),
        4:(0.7,-1),
        5:(0.7,-0.2),
        6:(0.6,0.6),
        7:(0.65,1.35),
        8:(-0.35,-1.3),
        9:(-0.3,-0.2),
        10:(-1.35,-1),
        11:(-1.1,0.35),
        12:(-1.4,1)}

        return position