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
    Data = open('thrones-network.csv', "r")
    next(Data, None)  # skip the first line in the input file
    Graphtype = nx.Graph()
    graph = nx.parse_edgelist(Data, delimiter=',', create_using=Graphtype,data=(('Weight', float),))

def printGraphParams():
    print(nx.info(graph))
    # print clustering coefficient
    print('clustring coefficient is:', nx.clustering(graph))
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

# TODO-remove edges with weight = 1
def removeEdges():
    global graph
    remove = [edge for edge in graph.edges().items() if edge[1]['Weight'] < 2]
    print(remove)


def printTopTenByCenterality():
    global graph
    topTenDF=[]
    # degree centerality
    result=nx.degree_centrality(graph)
    topTen1 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('degree centerality top ten:')
    df=pd.DataFrame.from_dict(topTen1, orient='index', columns=['Centrality'])
    print(df)
    # eigenvector centrality
    result=nx.eigenvector_centrality(graph)
    topTen2 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('eigenvector centerality top ten:')
    df=pd.DataFrame.from_dict(topTen2, orient='index', columns=['Centrality'])
    print(df)
    # betweenness centrality
    result = nx.betweenness_centrality(graph)
    topTen3 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('betweenness centerality top ten:')
    df=pd.DataFrame.from_dict(topTen3, orient='index', columns=['Centrality'])
    print(df)
    # closeness centrality
    result = nx.closeness_centrality(graph)
    topTen4 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('closeness centerality top ten:')
    df=pd.DataFrame.from_dict(topTen4, orient='index', columns=['Centrality'])
    print(df)

def intersectionTop():
    res = list(reduce(lambda x, y: x & y.keys(), ld))

def findCommunity():
    global graph
    gn_comm=girvan_newman(graph)
    

def main():
    csvToGraph()
    # removeEdges()
    printGraphParams()
    printTopTenByCenterality()
    findCommunity()

main()