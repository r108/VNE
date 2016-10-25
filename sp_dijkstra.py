""" Adopted from the below author:
   Copyright 2011 Shao-Chuan Wang <shaochuan.wang AT gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

CGREEN = '\33[32m'
CRED = '\33[31m'
CEND = '\33[0m'

import heapq
import config

def dijkstra(adj, costs, s, t):

    print(config.avoid,"///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    ''' Return predecessors and min distance if there exists a shortest path
        from s to t; Otherwise, return None '''
    Q = []     # priority queue of items; note item is mutable.
    d = {s: 0} # vertex -> minimal distance
    Qd = {}    # vertex -> [d[v], parent_v, v]
    p = {}     # predecessor
    visited_set = set([s])
    for n in config.avoid:
        if n != 0:
            print(n)
            visited_set.add(n)
    for v in adj.get(s, []):
        d[v] = costs[s, v]
        item = [d[v], s, v]
        heapq.heappush(Q, item)
        Qd[v] = item

    print("start at:", s)
    while Q:

        #print("Q is: ",Q)
        cost, parent, u = heapq.heappop(Q)
        if u not in visited_set:
            print ('visit:', u)


            p[u]= parent
            visited_set.add(u)
            if u == t:
                return p, d[u]
            for v in adj.get(u, []):
                if d.get(v):
                    if d[v] > costs[u, v] + d[u]:
                        d[v] =  costs[u, v] + d[u]
                        Qd[v][0] = d[v]    # decrease key
                        Qd[v][1] = u       # update predecessor
                        heapq._siftdown(Q, 0, Q.index(Qd[v]))
                else:
                    d[v] = costs[u, v] + d[u]
                    item = [d[v], u, v]
                    heapq.heappush(Q, item)
                    Qd[v] = item
    print("Empty Q: ",Q)
    return None

def display_shortest_path(path):
    shortest_path = []
    print('Shortest path is ', end="")
    for idx, p in enumerate(path):
        if idx == 0:
            # shortest_path.append((p, p+1))
            print(CGREEN, p, "->", end="")
        elif idx == (len(path) - 1):
            print(p, CEND)
        else:
            print(p, "->", end="")

        if idx != len(path) - 1:
            shortest_path.append((path[idx], path[idx + 1]))
    print("Shortest path links  ", shortest_path,"\n")
    return shortest_path, path


def make_undirected(cost):
    ucost = {}
    for k, w in cost.items():
        ucost[k] = w
        ucost[(k[1],k[0])] = w
    return ucost


def find_sp(graph, weight, frm, to):
    adj=graph
    cost=weight
    cost = make_undirected(cost)

    s = frm
    t = to
    #print("ADJ", adj," and \nWEIGHT ",weight, " for s-t ",s,t)
    predecessors, min_cost = dijkstra(adj, cost, s, t)
    c = t
    path = [c]
    print ('min cost:', min_cost)
    while predecessors.get(c):
        path.insert(0, predecessors[c])
        c = predecessors[c]

    #print ('shortest path:', path)
    return path