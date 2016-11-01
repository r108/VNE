import networkx as nx

class WSN():

    __WSN_Nodes = nx.Graph()
    __WSN_Links = nx.Graph()
    __links = dict()
    __adj_list = {}
    __two_hops_list = dict()

    def __init__(self):
        self.init_wsn_substrate(self.get_adjacency_list())
        self.init_two_hop_neighborhood(self.get_adjacency_list())

    def get_links(self):
        return self.__links

    def get_wsn_links(self):
        return self.__WSN_Links

    def get_wsn_nodes(self):
        return self.__WSN_Nodes

    def get_two_hops_list(self):
        return self.__two_hops_list

    def init_two_hop_neighborhood(self, adj_list):
        for n in adj_list:
            items = adj_list.get(n)
            if_list = []
            if_list.extend(items)
            for i in items:
                if_list.extend(adj_list.get(i))
            self.__two_hops_list[n] = list(set([x for x in if_list if x != n]))
        #print("Interferences ",self.__two_hops_list)

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

        self.__adj_list = {1: [2, 9],
                 2: [1, 3, 10],
                 3: [2, 4, 11],
                 4: [3, 5, 12],
                 5: [4, 6, 13],
                 6: [5, 7, 14],
                 7: [6, 8, 15],
                 8:[7, 16],
                 9:[1, 10, 17],
        10:[2, 9, 11, 18],
        11:[3, 10, 12, 19],
        12:[4, 11, 13, 20],
        13:[5, 12, 14, 21],
        14:[6, 13, 15, 22],
        15:[7, 14, 16, 23],
        16:[8, 15, 24],
        17:[9, 18, 25],
        18:[10, 17, 19, 26],
        19:[11, 18, 20, 27],
        20:[12, 19, 21, 28],
        21:[13, 20, 22, 29],
        22:[14, 21, 23, 30],
        23:[15, 22, 24, 31],
        24:[16, 23, 32],
        25:[17, 26, 33],
        26:[18, 25, 27, 34],
        27:[19, 26, 28, 35],
        28:[20, 27, 29, 36],
        29:[21, 28, 30, 37],
        30:[22, 29, 31, 38],
        31:[23, 30, 32, 39],
        32:[24, 31, 40],
        33:[25, 34, 41],
        34:[26, 33, 35, 42],
        35:[27, 34, 36, 43],
        36:[28, 35, 37, 44],
        37:[29, 36, 38, 45],
        38:[30, 37, 39, 46],
        39:[31, 38, 39, 47],
        40:[32, 39, 48],
        41:[33, 42, 49],
        42:[34, 41, 43, 50],
        43:[35, 42, 44, 51],
        44:[36, 43, 45, 52],
        45:[37, 44, 46, 53],
        46:[38, 45, 47, 54],
        47:[39, 46, 48, 55],
        48:[40, 47, 56],
        49:[41, 50],
        50:[42, 49, 51],
        51:[43, 50, 52],
        52:[44, 51, 53],
        53:[45, 52, 54],
        54:[46, 53, 55],
        55:[47, 54, 56],
        56:[48, 55],}

        self.__adj_list4 = {1: [2,4,8],
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

        position = {1:(1.5,-1.6),
        2:(1.5,-1.2),
        3:(1.5,-0.8),
        4:(1.5,-0.4),
        5:(1.5,0.4),
        6:(1.5,0.8),
        7:(1.5,1.2),
        8:(1.5,1.6),
        9:(1,-1.6),
        10:(1,-1.2),
        11:(1,-0.8),
        12:(1,-0.4),
        13:(1,0.4),
        14:(1,.8),
        15:(1,1.2),
        16:(1,1.6),
        17:(0.5,-1.6),
        18:(0.5,-1.2),
        19:(0.5,-0.8),
        20:(0.5,-0.4),
        21:(0.5,0.4),
        22:(0.5,0.8),
        23:(0.5,1.2),
        24:(0.5,1.6),
        25:(0,-1.6),
        26:(0,-1.2),
        27:(0,-0.8),
        28:(0,-0.4),
        29:(0,0.4),
        30:(0,0.8),
        31:(0,1.2),
        32:(0,1.6),
        33:(-0.5,-1.6),
        34:(-0.5,-1.2),
        35:(-0.5,-0.8),
        36:(-0.5,-0.4),
        37:(-0.5,0.4),
        38:(-0.5,0.8),
        39:(-0.5,1.2),
        40:(-0.5,1.6),
        41:(-1,-1.6),
        42:(-1,-1.2),
        43:(-1,-0.8),
        44:(-1,-0.4),
        45:(-1,0.4),
        46:(-1,0.8),
        47:(-1,1.2),
        48:(-1,1.6),
        49:(-1.5,-1.6),
        50:(-1.5,-1.2),
        51:(-1.5,-0.8),
        52:(-1.5,-0.4),
        53:(-1.5,0.4),
        54:(-1.5,0.8),
        55:(-1.5,1.2),
        56:(-1.5,1.6)}

        return position