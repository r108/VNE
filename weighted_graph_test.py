'''Create nodes and edges and set their attributes'''
try:
    import matplotlib.pyplot as plt
except:
    raise

from wsn_substrate import WSN
import networkx as nx
from link_weight import LinkCost
import sp_dijkstra as sp
import config

CVIOLETBG = '\33[45m'
CBLUEBG = '\33[44m'
CGREYBG = '\33[100m'
CGREEN = '\33[32m'
CRED = '\33[31m'
CEND = '\33[0m'


#G = nx.Graph()
GW = nx.Graph()

#WSN_Nodes = nx.Graph()
#WSN_Links = nx.Graph()
vwsn_list  = []



wsn = WSN()

exit_flag = True

def update_all_links_attributes(plr, load):
    for u,v,d  in WSN_Links.edges_iter(data=True):
        WSN_Links[u][v]['plr'] = plr
        WSN_Links[u][v]['load'] = load
        link_weight = LinkCost(WSN_Links[u][v]['plr'], WSN_Links[u][v]['load'])
        WSN_Links[u][v]['weight'] = link_weight.get_weight(link_weight)
        links[(u, v)] = link_weight.get_weight(link_weight)
        print(link_weight.get_weight(link_weight))
    print("")

def update_link_attributes(u, v, plr, load):

    if plr is -1:
        WSN_Links[u][v]['plr'] = WSN_Links[u][v]['plr']
    else:
        WSN_Links[u][v]['plr'] += plr
    if load is -1:
        WSN_Links[u][v]['load'] = WSN_Links[u][v]['load']
    else:
        WSN_Links[u][v]['load'] += load

    link_weight = LinkCost(WSN_Links[u][v]['plr'], WSN_Links[u][v]['load'])
    WSN_Links[u][v]['weight'] = link_weight.get_weight(link_weight)
    links[(u, v)] = link_weight.get_weight(link_weight)


def difference(Nodes, R):
    DIF = nx.create_empty_copy(R)

    if set(Nodes != set(R)):
        raise nx.NetworkXError("Graphs are not equal!!")

    r_edges = set(R.edges_iter())
    s_edges = set(Nodes.edges_iter())

    diff_edges = r_edges.symmetric_difference(s_edges)

    #in case edges are in r but not in s
    diff_edges = r_edges - s_edges

    DIF.add_edges_from(diff_edges)

    return DIF


'''
def initialize_nodes(G):
    for n in G.nodes():
        G.add_node(n, centrality=1, load=1)
    print("")
'''

def display_node_attr(G):
    print("")
    for n, d in G.nodes_iter(data=True):
        if 'rank' in d:
            if 'load' in d:
                print("Node",CGREEN,n,CEND,"has",CBLUEBG,"rank",d['rank'],CEND,CGREYBG,"load",d['load'],CEND,"and degree of",d['degree'])
            else:
                print(CRED,"Missing",CGREYBG,"load",CRED,"attribute in",CEND,CGREEN,n,CEND)
        else:
            print(CRED,"Missing",CBLUEBG,"rank",CRED,"attribute in",CEND,CGREEN,n,CEND)
    print("")

def display_edge_attr(G):
    #print("Edge attributes - ", G.edge)
    for u,v,d in G.edges_iter(data=True):

        if 'weight' in d:
            if 'plr' in d:
                if 'load' in d:
                    print("Edge", CGREEN, u, "<->", v, CEND, "has",
                          CBLUEBG, "weight", d['weight'], CEND,
                          CVIOLETBG, "plr", format(G[u][v]['plr']), CEND,
                          CGREYBG, "load", format(G[u][v]['load']), CEND)
                else:
                    print(CRED,"Missing",CGREYBG,"load",CEND,CRED,"attribute in",CEND,CGREEN,u,"<->",v,CEND)
            else:
                print(CRED,"Missing",CVIOLETBG,"plr",CEND,CRED,"attribute in",CEND,CGREEN,u,"<->",v,CEND)
        else:
            print(CRED,"Missing",CBLUEBG,"weight",CEND,CRED,"attribute in",CEND,CGREEN,u,"<->",v,CEND)
    #print(G[u][v].keys())
    print("")


def show_graph_plot(G,shortest_path, path):

    embeding_positions = list(map(int,path))
    colors=[]

    for n in G.nodes():
        if n in embeding_positions:
            colors.append('r')
        else:
            colors.append('g')

    fixed_positions = wsn.get_nodes_position()
    fixed_nodes = fixed_positions.keys()

    #elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >1200]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True)]# if d['weight'] <=1200]

    edge_labels = dict([((u,v),d['weight']) for u,v,d in G.edges(data=True)])
    eembed=shortest_path
    #eembed.append((1,2))
    pos=nx.spring_layout(G,pos=fixed_positions, fixed=fixed_nodes) # positions for all nodes
    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=300, node_color=colors)
    # edges
    #nx.draw_networkx_edges(G,pos,edgelist=elarge,width=2)
    nx.draw_networkx_edges(G,pos,edgelist=eembed,width=10, edge_color='r')

    nx.draw_networkx_edges(G,pos,edgelist=esmall,
                        width=4,alpha=0.5,edge_color='b',style='dashed')
    # labels
    nx.draw_networkx_labels(G,pos,font_size=15,font_family='sans-serif')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,font_size=12)


    plt.axis('on')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display

def update_all_nodes_attributes(load):

    for n, d in WSN_Nodes.nodes(data=True):
        WSN_Nodes[n]['load'] = load
        WSN_Nodes[n]['rank'] = WSN_Nodes.neighbors(n)

def update_node_attributes(Nodes, node, load):
    for n, d in Nodes.nodes_iter(data=True):
        #print("n is",type(n),"and node is",type(node))
        if n == int(node):
            d['load'] = d['load']+int(load)
            print("d['load'] = ",(d['load']+int(load)))
            d['rank'] = len(adj[n])


def get_shortest_path_tree(adj, links, nodes_to_em):
    print(adj,"adj====")
    print(links,"links---------")
    print(nodes_to_em,"nodes_to_em==============")
    edge_list = dict()
    i = 0
    for n in nodes_to_em:
        print("Nodes to em: ",n,"in  ",nodes_to_em)
        if i < len(nodes_to_em) - 1:
            k = (int((nodes_to_em[i])), int(nodes_to_em[i + 1]))
            l = 0
            if k in links:
                edge_list[(int((nodes_to_em[i])), int(nodes_to_em[i + 1]))] = sp.find_sp(adj, links, int((nodes_to_em[i])),int((nodes_to_em[i+1])))
            else:
                edge_list[(int((nodes_to_em[i])), int(nodes_to_em[i + 1]))] = l
            print("--------------------------================================ww ", 1)
            #paths_list[(nodes_to_em[i], nodes_to_em[i + 1])] = sp.find_sp(adj, links, nodes_to_em[i],nodes_to_em[i + 1])
            print("paths_list", edge_list)
            #sp.display_shortest_path(edge_list[(int((nodes_to_em[i])), int(nodes_to_em[i + 1]))])
            shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj,links,int(nodes_to_em[i]), int(nodes_to_em[i + 1])))
            show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)
            i = i + 1



def get_shortest_path(adj, links, frm, to):
    return sp.find_sp(adj, links, frm, to)

def embed_nodes(nodes_to_em, quota):
    nodes_list =[]
    vn = []
    vn_links = nx.Graph()
    vn_nodes = nx.Graph()
    frm = nodes_to_em[0]
    to = nodes_to_em[1]
    for n in nodes_to_em:
        nodes_list.append(n)
        update_node_attributes(WSN_Nodes, int(n), int(quota))
        vn_nodes.add_node(int(n), load = int(quota))
        #vnr.add_node(n, load=int(quota))
        #vn_nodes[n]['load'] = int(quota)
    vn.append(vn_nodes)
    #print('nodes to em', nodes_list)
    shortest_path, path_nodes = sp.display_shortest_path(
        get_shortest_path(adj, links, int(frm), int(to)))


    for l in shortest_path:



       WSN_Links[l[0]][l[1]]['load'] = WSN_Links[l[0]][l[1]]['load'] + int(quota)
       update_link_attributes(l[0], l[1], WSN_Links[l[0]][l[1]]['plr'], WSN_Links[l[0]][l[1]]['load'])
       vn_links.add_edge(l[0],l[1], load=int(quota))
       #vnr.add_edge(l[0],l[1], load=int(quota))

       #vn_links[l[0]][l[1]] ['load']= int(quota)
    vn.append(vn_links)
    vwsn_list.append(vn)
 #   for i,vn in enumerate(vwsn_list):
 #       for j,val in enumerate(vn):
 #           for vnode,d in vn_nodes.nodes_iter(data=True):
 #             #  print("it a type ", type(vnode))
 #               print("node in embedded list is - ",vnode)
 #               print("data is ",vn_nodes.__getitem__(vnode))

    display_vn_nodes(vn_nodes)
    display_vn_links(vn_links)
    display_node_attr(WSN_Nodes)
    display_edge_attr(WSN_Links)
#    print("shp", shortest_path)
#   print("pn", path_nodes)
#    print("n2e--", nodes_to_em)
#    print("n2e", list(map(int,nodes_to_em)))
    show_graph_plot(wsn.get_wsn_links(), shortest_path, nodes_to_em)

def display_vn_nodes(vn_nodes):

    for n,d in vn_nodes.nodes_iter(data=True):
            print("Node ",n," load",d['load'])

def display_vn_links(vn_links):
    for u,v,d in vn_links.edges_iter(data=True):
        #print("edgedata for ",u,v, vn_links.get_edge_data(u,v))
        print("edgedata for ", u,"<->", v, "is",d['load'])

def display_data_structs():
    print("Nodes - ", WSN_Nodes.nodes(data=True))
    print("Edges - ", WSN_Links.edges(data=True))
    print("Adjacency list - ", WSN_Links.adjacency_list())
    print("adj_list - ", wsn.get_adjacency_list())
    print("Interference list - ", interferences)
    print("Links - ", links)

def print_conflicting_lnks(cn_frm, cn_to):

    e_list = []

    shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, cn_frm, cn_to))
    all_path_nodes = path_nodes
    print("path nodes pop last node", path_nodes.pop())
    print("path nodes", path_nodes)
    print("all path nodes", all_path_nodes)
    for pn in path_nodes:
        interferes = []
        interferes.extend(interferences.__getitem__(pn))
        interferes.append(pn)
        print(pn,"peers are: ",interferes)
        #for i in interferes:
        for fr,t in links:
            if (fr in interferes) and (t in interferes):
                if (fr in wsn.get_adjacency_list().__getitem__(pn)) or (t in wsn.get_adjacency_list().__getitem__(pn)):
                    e_list.append((fr,t))
 #                   print(fr,t," are in links")
                else:
                    print("NOT IN LINKS - ",wsn.get_adjacency_list().__getitem__(pn))
        e_list2 = list(set(e_list))
#        print("e_list: ",e_list)
#m        print("e_list2: ", e_list2)

    map_nodes(all_path_nodes)

    map_links(e_list, e_list2)

    show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)
    display_edge_attr(WSN_Links)
    display_node_attr(WSN_Nodes)
        #print(interferences.keys())
    #print(interferences.__getitem__(int(cn)))

def get_conflicting_links(path_nodes):
    counter1 = 0
    counter2 = 0
    e_list = []
    elist = []
    all_path_nodes = []
#    shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, cn_frm, cn_to))
    all_path_nodes.extend(path_nodes)
    print("path nodes pop last node", path_nodes.pop())
    print("path nodes", path_nodes)
    print("all path nodes", all_path_nodes)
    for pn in path_nodes:
        counter1 = counter1 + 1
        counter2 = counter2 + 1
        print(pn)
        interferes = []
        print(pn,"interferences.__getitem__(pn)",interferences.__getitem__(pn))
        interferes.extend(interferences.__getitem__(pn))
        interferes.append(pn)
        print("interferes",interferes)
#        print(pn, "peers are: ", interferes)
        # for i in interferes:
        print()
        print("links",links)
        print("wsn.get_adjacency_list().__getitem__(pn)",wsn.get_adjacency_list().__getitem__(pn))
        remove_list = []
        for n in wsn.get_adjacency_list().__getitem__(pn):

            inner_neighbor_list = []
            inner_neighbor_list = wsn.get_adjacency_list().__getitem__(n)
            remove_list.append(pn)

            print("n is",n)
            counter1 = counter1 + 1
            if (pn in interferes) and (n in interferes):
                if pn < n:
                    print("append pn n",pn,n)
                    elist.append((pn, n))
                else:
                    print("append n pn",n,pn)
                    elist.append((n, pn))



            print(n," 's inner neighbor list - ", inner_neighbor_list )
            if pn in inner_neighbor_list:
                print(pn, "pn is in  inner_neighbor_list",inner_neighbor_list)
            print("remove list-",remove_list,"from inner neighbor list-",inner_neighbor_list)
            inner_neighbor_list = [x for x in inner_neighbor_list if x not in remove_list]
            print("remove list-",remove_list,"from inner neighbor list-",inner_neighbor_list," results")

            print("######################################################################")
            print(pn, "pn is removed from inner_neighbor_list", inner_neighbor_list)
            print(pn, "original list remains",wsn.get_adjacency_list().__getitem__(n))
            for nn in inner_neighbor_list:
                print(nn,"nn-",n,"n")
                counter1 = counter1 + 1
                flag = False
                #if (n,nn) not in inner_list:
                #flag = True
                if nn < n:
                    print("append nn n",nn,n)
                    elist.append((nn, n))
                else:
                    print("append n nn",n,nn)
                    elist.append((n, nn))
            remove_list.append(n)

        elist2 = list(set(elist))
        print("counter1", counter1)
        print("get conflict elist: ", elist)
        print("get conflict elist2: ", elist2)

        for u, v in links:
            counter2 = counter2 + 1

            if (u in interferes) and (v in interferes):
                if (u in wsn.get_adjacency_list().__getitem__(pn)) or (v in wsn.get_adjacency_list().__getitem__(pn)):
                    e_list.append((u, v))
#                    print(fr, t, " are in links")
                else:
                    print("NOT IN LINKS ",wsn.get_adjacency_list().__getitem__(pn))
        e_list2 = list(set(e_list))
        print("counter2", counter2)
        print("get conflict e_list: ", e_list)
        print("get conflict e_list2: ", e_list2)

    for u, v in elist2:
        print(u, v, "elist2 times", elist.count((u, v)))
    print()
    for u, v in e_list2:
        print(u, v, "elist2 times", e_list.count((u, v)))
    return e_list, e_list2

def map_links(e_list, e_list2):
    for e_fr,e_to in e_list2:
        update_link_attributes(int(e_fr), int(e_to), -1, (e_list.count((e_fr,e_to)) * 10))
        print(e_fr,e_to,"occur ", e_list.count((e_fr,e_to)),"times")

def map_nodes(all_path_nodes):

    for idx,pn in enumerate(all_path_nodes):
        if idx == 0:
            update_node_attributes(WSN_Nodes, pn, 20)
        elif idx == (len(all_path_nodes) - 1):
            update_node_attributes(WSN_Nodes, pn, 20)
        else:
            update_node_attributes(WSN_Nodes, pn, 10)

def embed_vn(VN):
    print("VN embedding: ",VN)

    vwsn_nodes = VN[1]
    vr_links = VN[2]

    frm = list(vwsn_nodes)[0]
    to = list(vwsn_nodes)[1]

    required_load = vwsn_nodes[frm]['load']
    config.avoid = [0]
    verify(vr_links, frm, to, required_load)


def verify(vr_links, frm, to, required_load):
    config.counter_value = config.counter_value +1
    print(config.counter_value,"counter ")
    user_input = input('continue?: ')
    if user_input is '0':
        shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, frm, to))
        show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)
    else:
        shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, frm, to))
        show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)

        #exit(0)
    e_list, e_list2 = [], []
    e_l, e_l2 = get_conflicting_links(path_nodes)
    e_list.extend(e_l)
    e_list2.extend(e_l2)

    nodes_in_path = []
    for e1, e2 in e_list2:
        if e1 not in e_list2:
            nodes_in_path.append(e1)
        if e2 not in e_list2:
            nodes_in_path.append(e2)

    nodes_in_path = list(set(nodes_in_path))
    print("nodes in path --", nodes_in_path)

    node_check = check_node_constraints(nodes_in_path, required_load)

    if node_check != 0:
        print("node ", node_check, "does not have enough resource\nEMBEDDING FAILED!")
    else:
        print("nodes have enough resource")

    link_check_u, v = check_link_constraints(e_list, e_list2, vr_links['load'], vr_links['plr'])

    if link_check_u != 0:
        print(link_check_u, v, "do not have enough resource")
        if config.counter_value < 20:
            config.avoid.append(v)
            verify(vr_links, frm, to, required_load )   ##recalculate path
    else:
        print("edges have enough resource")


def check_link_constraints(e_list, e_list2, required_load, required_plr):
    print("checking links ---- ",e_list,"\ne_list2 -- ",e_list2)
    for u,v in e_list2:
        if WSN_Links[u][v]['load'] + (required_load * e_list.count((u,v))) > 100:
            print(WSN_Links[u][v]['load']," + ",(required_load * e_list.count((u, v))), "is required")
            print(u, v, "have not got enough resource")
            return u,v
        else:
            print((required_load * e_list.count((u, v))), "is required")
            print(u, v, "have enough resource")

    return 0,0


def check_node_constraints(nodes_in_path, required_load):
    print("checking nodes -----",nodes_in_path)
    for idx,n in enumerate(nodes_in_path):
        if idx == 0:
            if WSN_Nodes.node[n]['load'] + required_load > 100:
                #print("Source node - ",WSN_Nodes.node[n]['load'])
                return n
        elif idx == (len(nodes_in_path) - 1):
            if WSN_Nodes.node[n]['load'] + required_load > 100:
                #print("Sink node - ",WSN_Nodes.node[n]['load'])
                return n
        else:
            if WSN_Nodes.node[n]['load']  + required_load > 100:
                #print("Relay node - ",WSN_Nodes.node[n]['load'])
                return n
    return 0

if __name__ == '__main__':

    VWSN_nodes = {3: {'load':30},
                  8:{'load':30}}

    VR_links = {'load':30, 'plr':40}
    VN = (1000,VWSN_nodes,VR_links)





    links = wsn.get_links()
    adj = wsn.get_adjacency_list()
    WSN_Nodes = wsn.get_wsn_nodes()
    WSN_Links = wsn.get_wsn_links()
    interferences = wsn.get_interferences()
    update_all_links_attributes(1, 1)
    print("...................", WSN_Nodes)
    shortest_path, path_nodes = [],[] #sp.display_shortest_path(get_shortest_path(adj,links,1,6))
    #print("SP:", shortest_path, "P", path_nodes)
    #print('path nodes',path_nodes)
    display_edge_attr(WSN_Links)
    display_node_attr(WSN_Nodes)

    #display_data_structs()


    #update_link_attributes(4, 8, 30, 30)
    WSN_Links[4][8]['load'] =20
    WSN_Links[5][9]['load'] = 20
    display_data_structs()
    embed_vn(VN)

    while exit_flag is True:
        print("\n---->\n0 - Exit\n1 - update all links\n2 - shortest path\n"
              "3 - change link args\n4 - change node arg\n5 - embed nodes\n6 - show\n7 - Interferences\n")
        user_input = input(': ')
        if user_input is '0':
            #shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, 1, 6))

            exit_flag = False
            #exit()
            #show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)
        elif user_input is '1':
            plr = input('plr: ')
            load = input('load: ')
            display_edge_attr(WSN_Links)
            display_data_structs()
            update_all_links_attributes( int(plr), int(load) )
            display_edge_attr(WSN_Links)
            shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, 1, 6))
        elif user_input is '2':
            frm = input('frm: ')
            to = input('to: ')
            display_edge_attr(WSN_Links)
            shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, int(frm), int(to)))
            show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)
        elif user_input is '3':
            link_nodes = input('link: ')
            link_nodes = link_nodes.split(',')
            print(link_nodes[0],link_nodes[1])
            plr = input('plr: ')
            load = input('load: ')
            update_link_attributes(int(link_nodes[0]),int(link_nodes[1]),int(plr),int(load))
            print("Links", links)
            display_edge_attr(WSN_Links)
        elif user_input is '4':
            node = input('node: ')
            load = input('load: ')
            display_node_attr(WSN_Nodes)
            update_node_attributes(WSN_Nodes, int(node),int(load))
            display_node_attr(WSN_Nodes)
        elif user_input is '5':
            nodes_to_embed = input("nodes to embed: ")
            nodes_to_embed = nodes_to_embed.split(",")
            quota = input("quota: ")

            #get_shortest_path_tree(adj, links, nodes_to_embed)

            embed_nodes(nodes_to_embed,quota)

        elif user_input is '6':
            show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)

        elif user_input is '7':
            conflict_node1 = input("conflict source node: ")
            conflict_node2 = input("conflict end node: ")

            print_conflicting_lnks(int(conflict_node1),int(conflict_node2))
