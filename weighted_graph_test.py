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
import copy

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
     #   print(link_weight.get_weight(link_weight))
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

def display_vn_node_allocation(G):
    print("")
    for n, d in G.nodes_iter(data=True):
        if 'load' in d:
            print("Node",CGREEN,n,CEND,"has",CGREYBG,"load",d['load'],CEND,"allocated")
        else:
            print(CRED, "Missing", CGREYBG, "load", CRED, "attribute in", CEND, CGREEN, n, CEND)
    print("")

def display_vn_edge_allocation(G):
    for u,v,d in G.edges_iter(data=True):
        if 'load' in d:
            print("Edge", CGREEN, u, "<->", v, CEND, "has",
                  CGREYBG, "load", format(G[u][v]['load']), CEND,"allocated")
        else:
            print(CRED,"Missing",CGREYBG,"load",CEND,CRED,"attribute in",CEND,CGREEN,u,"<->",v,CEND)
    print("")

def display_edge_attr(G):
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

    config.plot_counter += 1
    embeding_positions = list(map(int,path))
    colors=[]

    for n in G.nodes():
        if n in embeding_positions:
            colors.append('r')
        else:
            colors.append('g')

    positions = wsn.get_nodes_position()
    fixed_positions = dict()
    for n in G.nodes(data=False):
        fixed_positions.update({n:positions[n]})
    #fixed_positions = dict(x,d for x,d in fixed_positions if x  in G.nodes(data=False))

    fixed_nodes = fixed_positions.keys()

    #elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >1200]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True)]# if d['weight'] <=1200]

    edge_labels = dict([((u,v),d['load']) for u,v,d in G.edges(data=True)])
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
    plt.savefig("weighted_graph"+str(config.plot_counter)+".png") # save as png
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
            d['rank'] = len(adj[n])


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
    shortest_path, path_nodes = sp.get_shortest_path(adj, links, int(frm), int(to))


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
    print("Interference list - ", two_hops_list)
    print("Links - ", links)


def get_conflicting_links(path_nodes):
    p_nodes = []
    p_nodes.extend(path_nodes)
    counter1 = 0
    counter2 = 0
#    e_list = []
    elist = []
    all_path_nodes = []
#    shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, cn_frm, cn_to))
    all_path_nodes.extend(p_nodes)
    p_nodes.pop()

    for pn in p_nodes:
        counter1 = counter1 + 1
        counter2 = counter2 + 1
        interferes = []
        interferes.extend(config.two_hops.__getitem__(pn))
        interferes.append(pn)

        remove_list = []
        for n in config.reduced_adj.get(pn):
            counter1 = counter1 + 1
 #           inner_neighbor_list = []
            inner_neighbor_list = config.reduced_adj.get(n)
            remove_list.append(pn)

            if (pn in interferes) and (n in interferes):
                if pn < n:
                    #print("append pn n",pn,n)
                    elist.append((pn, n))
                else:
                    #print("append n pn",n,pn)
                    elist.append((n, pn))

            inner_neighbor_list = [x for x in inner_neighbor_list if x not in remove_list]

            for nn in inner_neighbor_list:
                counter1 = counter1 + 1
                if nn < n:
                    #print("append nn n",nn,n)
                    elist.append((nn, n))
                else:
                    #print("append n nn",n,nn)
                    elist.append((n, nn))
            remove_list.append(n)

        elist2 = list(set(elist))
        print("counter1", counter1)
        print("get conflict elist: ", elist)
        print("get conflict elist2: ", elist2)

#    for u, v in elist2:
#        print(u, v, "elist2 times", elist.count((u, v)))
    print()

    return elist, elist2

'''
        for u, v in links:
            counter2 = counter2 + 1
            if (u in interferes) and (v in interferes):
                if (u in adj.__getitem__(pn)) or (v in adj.__getitem__(pn)):
                    e_list.append((u, v))
                else:
                    print("NOT IN LINKS ",adj.__getitem__(pn))

        e_list2 = list(set(e_list))
        print("counter2", counter2)
        print("get conflict e_list: ", e_list)
        print("get conflict e_list2: ", e_list2)

     for u, v in e_list2:
        print(u, v, "e_list2 times", e_list.count((u, v)))
'''



def map_links(e_list, e_list2, required_load):
    for e_fr,e_to in e_list2:
        update_link_attributes(int(e_fr), int(e_to), -1, (e_list.count((e_fr,e_to)) * required_load))
        #if (e_fr,e_to) not in config.allocated_links_weight:
        config.allocated_links_weight.update({(e_fr,e_to): WSN_Links[e_fr][e_to]['weight']})
        config.allocated_links_load.update({(e_fr, e_to): WSN_Links[e_fr][e_to]['load']})
#        print(e_fr,e_to,"occur ", e_list.count((e_fr,e_to)),"times")
    print("config.allocated_links_weight.",config.allocated_links_weight)
    print("config.allocated_links_load.", config.allocated_links_load)
    #print("get reduced adj",type(config.allocated_links_weight)


def map_nodes(all_path_nodes, required_load):

    for idx,pn in enumerate(all_path_nodes):
        if idx == 0:
            update_node_attributes(WSN_Nodes, pn, required_load)
        elif idx == (len(all_path_nodes) - 1):
            update_node_attributes(WSN_Nodes, pn, required_load)
        else:
            update_node_attributes(WSN_Nodes, pn, required_load)

def embed_vn(VN):

    config.reduced_adj = copy.deepcopy(adj)
    config.link_weights = copy.deepcopy(links)
    config.two_hops = copy.deepcopy(two_hops_list)

    print("@",config.link_weights)
    print("VN embedding: ",VN)

    vwsn_nodes = VN[1]
    link_reqiurement = VN[2]

    frm = list(vwsn_nodes)[0]
    to = list(vwsn_nodes)[1]

    node_requirement = vwsn_nodes[frm]['load']
    config.avoid = [(0,0)]
    verify(link_reqiurement, frm, to, node_requirement)


def verify(link_reqiurement, frm, to, node_requirement):
    config.counter_value = config.counter_value +1
    print(config.counter_value,"counter ")

    node_check, VN_nodes = check_node_constraints([frm,to], node_requirement)
    if node_check != 0:
        print("node ", node_check, "does not have enough resource\nEMBEDDING FAILED!")
        exit()
    else:
        print("source and sink nodes have enough resource")

    if config.has_embedding == True:
        print("config.has_embedding is",config.has_embedding)
        if (0,0) in config.avoid: config.avoid.remove((0,0))
        print("ccconfig.avoid",config.avoid)
        for u,v in config.avoid:
            config.avoid.remove((u, v))
            print("ccconfig.avoid after", config.avoid)

            print("u,v",u,v)
            print(config.reduced_adj.get(u), "forrr", v)
            print(config.reduced_adj.get(v), "forrr", u)
            config.reduced_adj.get(u).remove(v)
            config.reduced_adj.get(v).remove(u)
            config.two_hops.get(v).remove(u)
            config.two_hops.get(u).remove(v)

            print("config.avoid before",config.avoid)

            print("config.avoid after", config.avoid)
            print(config.reduced_adj.__getitem__(u),"for",v)
            print(config.reduced_adj.__getitem__(v),"for",u)
            print("adj",adj.get(u),"reduced_ad",config.reduced_adj.__getitem__(u))
            print("adj", adj.get(v), "reduced_ad", config.reduced_adj.__getitem__(v))
            config.link_weights[(u,v)] = 1000000
            print("config.link_weights[(u,v)]",config.link_weights[(int(u),int(v))],"\nlinks[(u,v)]",links[(int(u),int(v))])

        shortest_path, path_nodes = sp.get_shortest_path(config.reduced_adj, config.link_weights, frm, to)
        if shortest_path is None:
            print("EMBEDDING HAS FAILED!")
            return
    else:
        print("config.has_embedding is",config.has_embedding)
        shortest_path, path_nodes = sp.get_shortest_path(adj, links, frm, to)

    print("??path nodes",path_nodes)

    e_list, e_list2 = get_conflicting_links(path_nodes)

    # get list of unique nodes from conflicting link list
    nodes_in_path = []
    for e1, e2 in e_list2:
        if e1 not in nodes_in_path:
            nodes_in_path.append(e1)
        if e2 not in nodes_in_path:
            nodes_in_path.append(e2)

    node_check, VN_nodes = check_node_constraints(nodes_in_path, node_requirement)

    if node_check != 0:
        print("node ", node_check, "does not have enough resource\nEMBEDDING FAILED!")
        return
    else:
        print("all nodes in path have enough resource")

    print("shortest_path", shortest_path)
    print("path nodes", path_nodes)
    link_check, VN_links = check_link_constraints(e_list, e_list2, link_reqiurement['load'], link_reqiurement['plr'],shortest_path)
    print("link_check",link_check)
    if link_check != (0,0):
        print("link_check is", link_check)
        if config.counter_value > 100:
            print(link_check, "do not have enough resource")
            print("EMBEDDING HAS FAILED!!")
            return
        if link_check not in config.avoid:
            config.avoid.append(link_check)
        verify(link_reqiurement, frm, to, node_requirement)

 #       reduce_feasible_edges(link_reqiurement, link_check_u, link_check_v, node_requirement)
    else:
        print("edges have enough resource")
        print("++SUCCESSFUL EMBEDDING++")
        config.feasible = True
        config.has_embedding = True
        commit_vn(VN_nodes,VN_links,node_requirement,e_list, e_list2, path_nodes, shortest_path)
        print("shortest_path",shortest_path)
        print("path nodes",path_nodes)



##    show_graph_plot(wsn.get_wsn_links(), shortest_path, [frm,to])

def reduce_feasible_edges(link_reqiurement, u, v, node_requirement):

    #reduced_adj = dict()
    reduced_links = dict()
    print(type(adj),"adj",adj)
    print(type(links),"links",links)
    ab = nx.Graph()

    for node in adj:
        for neighbor in wsn.get_adjacency_list().__getitem__(node):
            print(node,neighbor,"dont match", u, v)
            if (node == u) and (neighbor == v):
                print("match",u,v)

    print(adj)
    #print(reduced_adj)


    verify(link_reqiurement, u, v, node_requirement)  ##recalculate path

    #shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, frm, to))

def commit_vn(VN_nodes, VN_links, required_load,e_list, e_list2, path_nodes, shortest_path):
    map_nodes(VN_nodes.nodes(), required_load)
    map_links(e_list, e_list2, required_load)

    print("path_nodes", path_nodes, "\nrequired_load", required_load)

    print("VN Nodes - ", VN_nodes.nodes(data=True))
    print("VN Links - ", VN_links.edges(data=True))
    vn = (VN_nodes, VN_links, shortest_path, path_nodes)
    print("here wsn.get_wsn_links()", VN_links.edges(data=True), "\n shortest_path", shortest_path,
          "\n path_nodes", path_nodes)
    config.VWSNs.append(vn)





def check_link_constraints(e_list, e_list2, required_load, required_plr, shortest_path):
    VN_links = nx.Graph()
    print("checking links ---- ",e_list,"\ne_list2 -- ",e_list2,"shortest_path",shortest_path)
    for u,v in shortest_path:

        if WSN_Links[u][v]['load'] + (required_load * e_list.count((u, v))) > 100:
            print("PATH FAILS AT",u,v)
            return (u,v),VN_links
    for u,v in e_list2:
        if WSN_Links[u][v]['load'] + (required_load * e_list.count((u,v))) > 100:
            print("Link",u, v,"requires",WSN_Links[u][v]['load']," + ",(required_load * e_list.count((u, v))), "but have not got enough")
            return (u,v),VN_links
        else:
            allocated_load = (required_load * e_list.count((u, v)))
            VN_links.add_edge(u,v, {'load':allocated_load})
            print(u, v, "can supply",allocated_load)
            return_value = (0,0)
    print("RETURN ",return_value)
    return return_value,VN_links


def check_node_constraints(nodes_in_path, required_load):
    VN_nodes = nx.Graph()
    print("checking nodes -----",nodes_in_path)
    for idx,n in enumerate(nodes_in_path):
        VN_nodes.add_node(n, {'load': required_load})
        if idx == 0:
            if WSN_Nodes.node[n]['load'] + required_load > 100:
                print("Source node",n," has - ",WSN_Nodes.node[n]['load'],"and require",+ required_load )
                return n, VN_nodes
        elif idx == (len(nodes_in_path) - 1):
            if WSN_Nodes.node[n]['load'] + (required_load) > 100:
                print("Sink node",n,"has - ",WSN_Nodes.node[n]['load'],"and require",+ required_load )
                return n, VN_nodes
        else:
            if WSN_Nodes.node[n]['load']  + required_load > 100:
                print("Relay node",n,"has - ",WSN_Nodes.node[n]['load'],"and require",+ required_load )
                return n, VN_nodes
    return 0, VN_nodes

def draw_graph():
    N = 10
    G = nx.grid_2d_graph(N, N)
    print("G nodes --", G.node)
    pos = dict((n, n) for n in G.nodes())
    labels = dict(((i, j), i + (N - 1 - j) * 10) for i, j in G.nodes())
    nx.draw_networkx(G, pos=pos, labels=labels)

    print("G adj",G.edges())
    print("G nodes", G.node)
    print("G nodes", G.adjacency_list())
    #plt.axis('off')
    plt.show()

if __name__ == '__main__':

    links = wsn.get_links()
    adj = wsn.get_adjacency_list()
    print("adj is type ",type(adj)," and links is type",type(links))

    WSN_Nodes = wsn.get_wsn_nodes()
    print("WSN_Nodes is type",type(WSN_Nodes))
    WSN_Links = wsn.get_wsn_links()
    two_hops_list = wsn.get_two_hops_list()
    update_all_links_attributes(1, 1)
    print("...................", WSN_Nodes)
    shortest_path, path_nodes = [],[] #sp.display_shortest_path(get_shortest_path(adj,links,1,6))
    #print("SP:", shortest_path, "P", path_nodes)
    #print('path nodes',path_nodes)
    display_edge_attr(WSN_Links)
    display_node_attr(WSN_Nodes)

    #display_data_structs()


    #update_link_attributes(4, 8, 30, 30)
#    WSN_Links[1][2]['load'] =20
#    WSN_Links[28][36]['load'] = 20
    display_data_structs()


    while exit_flag is True:
        print("\n---->\n0 - Exit\n1 - update all links\n2 - shortest path\n"
              "3 - change link args\n4 - change node arg\n5 - embed nodes\n6 - show\n7 - Embed\n"
              "\n8 - draw")
        user_input = input(': ')
        if user_input is '0':
            #shortest_path, path_nodes = sp.display_shortest_path(get_shortest_path(adj, links, 1, 6))
            display_edge_attr(WSN_Links)
            display_node_attr(WSN_Nodes)

            for idx,vwsn in enumerate(config.VWSNs):
                print("vwsn",idx,"nodes",vwsn[0].nodes(data=True))
                print("vwsn",idx,"links", vwsn[1].edges(data=True))
                print("VWSN ",idx,"allocations:")
                display_vn_edge_allocation(vwsn[1])
                display_vn_node_allocation(vwsn[0])
            #exit_flag = False
            #exit()
            show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)
        elif user_input is '1':
            plr = input('plr: ')
            load = input('load: ')
            display_edge_attr(WSN_Links)
            display_data_structs()
            update_all_links_attributes( int(plr), int(load) )
            display_edge_attr(WSN_Links)
            shortest_path, path_nodes = sp.get_shortest_path(adj, links, 1, 6)
        elif user_input is '2':
            frm = input('frm: ')
            to = input('to: ')
            display_edge_attr(WSN_Links)
            shortest_path, path_nodes = sp.get_shortest_path(adj, links, int(frm), int(to))
            show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)
            print("wsn.get_wsn_links()",wsn.get_wsn_links().edges(data=True),"\n shortest_path", shortest_path,"\n path_nodes", path_nodes)
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

            embed_nodes(nodes_to_embed,quota)

        elif user_input is '6':
            show_graph_plot(wsn.get_wsn_links(), shortest_path, path_nodes)
            display_edge_attr(WSN_Links)
            display_node_attr(WSN_Nodes)

        elif user_input is '7':
            node1 = input(" source node: ")
            if node1 != "":
                node2 = input(" sink node: ")
            else:
                continue
            if node2 != "":
                quota = input(" quota: ")
            else:
                continue



            VWSN_nodes = {int(node1): {'load': int(quota)},
                          int(node2): {'load': int(quota)}}

            link_reqiurement = {'load': int(quota), 'plr': 40}
            VN = (1000, VWSN_nodes, link_reqiurement)

            embed_vn(VN)
            #print_conflicting_lnks(int(conflict_node1),int(conflict_node2))
        elif user_input is '8':
            #draw_graph()
            display_edge_attr(WSN_Links)
            display_node_attr(WSN_Nodes)

            for idx, vwsn in enumerate(config.VWSNs):
                print("vwsn", idx, "nodes", vwsn[0].nodes(data=True))
                print("vwsn", idx, "links", vwsn[1].edges(data=True))
                print("VWSN ", idx, "allocations:")
                display_vn_edge_allocation(vwsn[1])
                display_vn_node_allocation(vwsn[0])
                show_graph_plot(vwsn[1], vwsn[2], vwsn[3])
                print("wsn.get_wsn_links()", vwsn[1].edges(data=True), "\n shortest_path", vwsn[2],
                      "\n path_nodes", vwsn[3])
                print("VN nodes",vwsn[1].nodes(data=False))
