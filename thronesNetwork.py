import networkx as nx
import pandas as pd

# read csv file into graph
def csvToGraph():
    df = pd.read_csv('thrones-network.csv')
    Graphtype = nx.Graph()
    G = nx.from_pandas_edgelist(df, edge_attr='Weight', create_using=Graphtype)
    print(G)

def main():
    csvToGraph()

main()