import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from functools import reduce
from networkx.algorithms.community import girvan_newman
import csv

# globals
graph={}

# read csv file into graph
def csvToGraph():
    global graph
    # Data = open('thrones-network.csv', "r")
    # next(Data, None)  # skip the first line in the input file
    # Graphtype = nx.Graph()
    # graph = nx.parse_edgelist(Data, delimiter=',', create_using=Graphtype,data=(('Weight', float),))
    Data=pd.read_csv('thrones-network.csv')
    graph=nx.from_pandas_edgelist(Data,source='Node A', target='Node B', edge_attr='Weight')
    graph=nx.to_undirected(graph)
    graph=nx.Graph(graph)
    print(graph)

# remove edges with weight<5
def removeEdges():
    global graph
    remove = [edge for edge in graph.edges().items() if edge[1]['Weight'] < 5]
    remove_list=[remove[i][0] for i in range(len(remove))]
    graph.remove_edges_from(remove_list)
    # remove nodes with no edge
    graph.remove_nodes_from(list(nx.isolates(graph)))
    nx.draw_spring(graph, with_labels=True)
    plt.show()

def printGraphParams():
    print(nx.info(graph))
    # print average clustering coefficient
    print('average clustring coefficient is:', nx.average_clustering(graph))
    # print density
    print('density is: ', nx.density(graph))
    # print diameter
    print('diameter is: ', nx.diameter(graph))
    # degree distribution
    degrees=[graph.degree(n) for n in graph.nodes()]
    plt.hist(degrees)
    plt.title("Degree Distribution Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    plt.show()
    # average path length
    print('average path length is: ', nx.average_shortest_path_length(graph))

# print DF for each kind of centrality
def printTopTenByCenterality():
    global graph
    topTenDF=[]
    # degree centerality
    result=nx.degree_centrality(graph)
    topTen1 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('degree centrality top ten:')
    df=pd.DataFrame.from_dict(topTen1, orient='index')
    df.columns=['Centrality']
    print(df)
    # eigenvector centrality
    result=nx.eigenvector_centrality(graph)
    topTen2 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('eigenvector centrality top ten:')
    df=pd.DataFrame.from_dict(topTen2, orient='index')
    df.columns=['Centrality']
    print(df)
    # betweenness centrality
    result = nx.betweenness_centrality(graph)
    topTen3 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('betweenness centrality top ten:')
    df=pd.DataFrame.from_dict(topTen3, orient='index')
    df.columns=['Centrality']
    print(df)
    # closeness centrality
    result = nx.closeness_centrality(graph)
    topTen4 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('closeness centrality top ten:')
    df=pd.DataFrame.from_dict(topTen4, orient='index')
    df.columns=['Centrality']
    print(df)

    intersectionTop([topTen1, topTen2, topTen3, topTen4])

# intersection between all types of centraluty
def intersectionTop(dicts):
    ld=dicts
    res = list(reduce(lambda x, y: x & y.keys(), ld))
    print("The most central characters in all centrality types: ",str(res))
    # print the intersection between all top10 lists

# find communities
def findCommunity():
    global graph
    gn_comm=girvan_newman(graph)
    first_iteration_comm=tuple(sorted(c) for c in next(gn_comm))
    print(dict(enumerate(first_iteration_comm)))

    # nx.draw(graph)
    # plt.show()

# top 10 predictions to link - jaccard
def linkPredictionJaccard():
    global graph
    preds_jc = nx.jaccard_coefficient(graph)
    pred_jc_dict = {}
    for u, v, p in preds_jc:
        pred_jc_dict[(u, v)] = p
    print(sorted(pred_jc_dict.items(), key=lambda x: x[1], reverse=True)[:10])

# top 10 predictions to link - adamic
def linkPredictionAdamic():
    global graph
    preds_aa = nx.adamic_adar_index(graph)
    pred_aa_dict = {}
    for u, v, p in preds_aa:
        pred_aa_dict[(u, v)] = p
    print(sorted(pred_aa_dict.items(), key=lambda x: x[1], reverse=True)[:10])



# main
def main():
    csvToGraph()
    removeEdges()
    printGraphParams()
    printTopTenByCenterality()
    # intersectionTop()
    findCommunity()
    linkPredictionAdamic()
    linkPredictionJaccard()


main()