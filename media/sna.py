README = '''
author: Chet Weger (chetweger@gmail.com)
Social Network Analysis Final Project
Filetypes:
    AList:
    1
    0
    abc:
    1 0
    0 1
    edges:
    0 1
    Above all describe the same graph.

To view a paper describing my project for Social Network Analysis visit:
http://chet-weger.herokuapp.com/Social_Network_Analysis/

structure and size.
To make an Erdos-Renyi file, type:
makeErAList([fileName], edges, nodes)
To convert from dimacs filetype type:
fromDimacs(filename)
To test the stability of a fileName, type:
run(fileName, [iterations])
Results can take quite long depending on the graph.

Dependencies: you must have python-igraph, and mcl (see man mcl).
'''



import random
import subprocess
import copy
import re
import os
import igraph
from igraph import *

CURRENT_DIR = os.getcwd()
FILE_OFFSET = 0

'''
Loads a file into a list of lists representation.
This can be either adjacency or abc/edges format
'''
def loadGraph(filename, fileType):
    fBuf = open(CURRENT_DIR + '/' + filename)
    lines = fBuf.readlines()
    lines = lines[FILE_OFFSET:len(lines)]
    digits = []
    for line in lines:
        lineDigits = re.findall('[\w]+', line)
        lineDigits = map(int, lineDigits)
        if fileType == "dimacs":
            lineDigits = map( (lambda x: x-1), lineDigits)
        digits = digits + [lineDigits]
    for i in range(len(digits)):
        for digit in digits[i]:
            #abc format is similar to edges format
            if (not fileType == "abc"):
                assert (i) in digits[digit]
    print "Graph loaded succesfully.  Assertions passed."
    fBuf.close()
    return digits

'''
The copy model with p = 0
since p=0, edge distribution will follow the power law
'''
def addEdgeCopyModel(graph):
    possibleNodes = range(FILE_OFFSET, len(graph))
    copyMeNode = random.choice(possibleNodes)
    possibleNodes.remove(copyMeNode)
    randNode = random.choice(possibleNodes)
    possibleAdditions = copy.deepcopy(graph[copyMeNode])
    addition = random.choice(possibleAdditions)
    graph[randNode] += [addition]
    graph[addition] += [randNode]
    return graph

'''
Changes format from AList to what Dongen calls abc format
(both both list of lists)
'''
def changeFormatToABC(adjacency_list_graph):
    abcFormat = []
    for current_node in range(len(adjacency_list_graph)):
        for adjacent_node in adjacency_list_graph[current_node]:
            abcFormat += [(current_node, adjacent_node)]
    return abcFormat

'''
Changes format from abc format to AList
(booth list of lists).
This function is sloooooooow.
'''
def changeFormatToAList(abcGraph):
    adjacencyList = []
    listAll = reduce( (lambda pair1, pair2: list(pair1) + list(pair2)), abcGraph)
    maxEl = max(listAll)
    size = maxEl + 1

    AList = [[] for x in range(size)]
    for pair in abcGraph:
        '''
        IMPORTANT: edgelist (igraph) and abc (mcl) are
        slightly different fileformats so we must check to
        avoid adding duplicates...
        '''
        if(not pair[1] in AList[pair[0]]):
            AList[pair[0]] += [pair[1]]
        if (not pair[0] in AList[pair[1]]):
            AList[pair[1]] += [pair[0]]

    for list_nodes in AList:
        # nodes should always be connnected to something...
        # cluster are not size 1
        assert list_nodes != -1
    return AList

'''
Used to prune graph to remove edges that don't
belong for a given clustering.
'''
def containsEdge(edge, clustering):
    for cluster in clustering:
        if (edge[0] in cluster) and (edge[1] in cluster):
            return True
    return False

'''
Takes a clustering and an abcGraph,
and trims the edges for the nodes that
are not in the same cluster.
'''
def pruneABCGraph(abcGraph, clustering):
    clusterGraph = []
    for edge in abcGraph:
        if containsEdge(edge, clustering):
            clusterGraph += [edge]
    return clusterGraph

'''
Writes list of lists to file.
'''
def writeToFile(graph, newFileName):
    # create a file to write to
    writeTo = open(CURRENT_DIR + '/' + newFileName, 'w+')
    for line in graph:
        stringLine = map(str, line)
        stringLine = reduce( (lambda x, y: x + ' ' + y), stringLine) + " \n"
        writeTo.write(stringLine)
    writeTo.close()
    print newFileName, "created."

'''
Takes a file and adds edge using copy model
[number] of times.
'''
def makeManyMods(number, fromFile, newFilesName):
    for i in range(number):
        oldGraph = loadGraph(fromFile, False)
        newGraph = addEdgeCopyModel(oldGraph)
        writeToFile(newGraph, 'mod_' + str(i) + '_' + newFilesName)


'''
Computes both split-join (normalized) and nmi distance measure
between two file graphs in adjacency form using the mcl alg.
'''
def computeDistanceMCL(fileName1, fileName2):
    graph1 = loadGraph(fileName1, "adjacency")
    graph2 = loadGraph(fileName2, "adjacency")
    assert len(graph1) == len(graph2)
    numNodes = len(graph1)

    graph1 = changeFormatToABC(graph1)
    graph2 = changeFormatToABC(graph2)
    intoMClF1 = "into_mcl_" + fileName1
    intoMClF2 = "into_mcl_" + fileName2
    assert intoMClF1 != intoMClF2
    writeToFile(graph1, intoMClF1)
    writeToFile(graph2, intoMClF2)

    c1 = "intermediate_" + fileName1
    c2 = "intermediate_" + fileName2
    subprocess.call(["mcl", intoMClF1, "--abc", "-o", c1])
    subprocess.call(["mcl", intoMClF2, "--abc", "-o", c2])

    clustering1 = loadGraph(c1, "abc")
    clustering2 = loadGraph(c2, "abc")

    prunedGraph1 = pruneABCGraph(graph1, clustering1)
    prunedGraph2 = pruneABCGraph(graph2, clustering2)

    clusterFile1 = "clustering_" + fileName1
    clusterFile2 = "clustering_" + fileName2
    writeToFile(prunedGraph1, clusterFile1)
    writeToFile(prunedGraph2, clusterFile2)
    clusterGraph1 = Graph.Read(clusterFile1, "edges")
    clusterGraph2 = Graph.Read(clusterFile2, "edges")

    cluster1 = Graph.clusters(clusterGraph1) # this is completely broken lol. Thats why it didn't work...
    cluster2 = Graph.clusters(clusterGraph2)

    mcl_dist = 1 - compare_communities(cluster1, cluster2, "nmi")
    sj_dist = compare_communities(cluster1, cluster2, "split-join")
    #normalizes split-join distance measure:
    sj_dist_norm = float(sj_dist)/(numNodes*2)

    return mcl_dist, sj_dist_norm


'''
Computes both split-join (normalized) and nmi distance measure between
two file graphs in adjacency form using the Fast modular alg.
'''
def computeDistanceFMod(fileName1, fileName2):
    graph1 = loadGraph(fileName1, "adjacency")
    graph2 = loadGraph(fileName2, "adjacency")
    num_nodes = len(graph1)
    assert len(graph1) == len(graph2)

    graph1 = changeFormatToABC(graph1)
    graph2 = changeFormatToABC(graph2)
    intoFModF1 = "into_FMod1_" + fileName1
    intoFModF2 = "into_FMod2_" + fileName2
    writeToFile(graph1, intoFModF1)
    writeToFile(graph2, intoFModF2)

    graph1 = Graph.Read(intoFModF1, 'edges')
    graph2 = Graph.Read(intoFModF2, 'edges')

    graph1 = graph1.as_undirected()
    graph2 = graph2.as_undirected()

    vertexDendrogram1 = graph1.community_fastgreedy()
    vertexDendrogram2 = graph2.community_fastgreedy()

    cluster1 = vertexDendrogram1.as_clustering()
    cluster2 = vertexDendrogram2.as_clustering()

    nmi_dist = 1 - compare_communities(cluster1, cluster2, "nmi")
    sj_dist = compare_communities(cluster1, cluster2, "split-join")

    #normalizes split-join distance measure:
    sj_dist_norm = float(sj_dist)/(num_nodes*2)
    return nmi_dist, sj_dist_norm

'''
Converts from the dimacs fileformat at
ccc.gatech.edu/dimacs10 to standard AList
compatible with mcl implementation
'''
def fromDimacs(fileName, newName):
    graph = loadGraph(fileName, 'dimacs')
    writeToFile(graph, newName)

'''
Creates a file for Erdos-Renyi graph
in AList or mcl-compatible file format.
'''
def makeErAList(filename, vertices, edges):
    er_graph = Graph.Erdos_Renyi(n=vertices, m=edges)
    er_graph = er_graph.as_undirected()
    er_graph.write_edgelist(filename)
    '''
    This is a bit wacky but it works... i need file
    format in AList to be compatible with my computeDistance
    functions.
    '''
    er_graph = loadGraph(filename, 'abc')
    er_graph = changeFormatToAList(er_graph)
    writeToFile(er_graph, filename)

'''
Uses the copy model to add an edge to fileName for [iterations]
number of times, and then computes the stability/distance between
fileName and the mods of all iterations.
'''
def run(fileName, iterations):
    makeManyMods(iterations, fileName, fileName)
    nmi_mcl = []
    sj_mcl = []
    nmi_FMod = []
    sj_FMod = []
    for i in range(iterations):
        otherFilename = "mod_" + str(i) + '_' + fileName

        result_mcl = computeDistanceMCL(fileName, otherFilename)
        print result_mcl, "iteration: ", i
        nmi_mcl += [result_mcl[0]]
        sj_mcl += [result_mcl[1]]

        result_fmod = computeDistanceFMod(fileName, otherFilename)
        nmi_FMod += [result_fmod[0]]
        sj_FMod += [result_fmod[1]]

    return {'nmi_mcl': nmi_mcl, 'sj_mcl': sj_mcl, 'nmi_FMod': nmi_FMod, 'sj_FMod': sj_FMod}

print README
