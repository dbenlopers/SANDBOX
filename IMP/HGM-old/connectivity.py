'''

'''
#import IMP
#import HGM,HGM.distances

    
#    
#            CONCERNING GRAPHS
#
    #
    # possible connectivity graphs on subunits or particles will be indexed simply by considering
    # the series of observed connexions between objects and consdering then as a bit
    #  for instance, nterconectivity graphs with nodes [p8,p53,p44,p34,p62]    
    #        p8 p53 p44 p34 p62
    #    p8
    #    p53 b1
    #    P44 b2  b3
    #    p34 b4  b5  b6
    #    p62 b7  b8  b9 b10
    #
    #    graph index = sum (bi * pow(2,i) with bi = 1 if the particles are connected
    #
    #    0: 0 1 2 3 4
    #    1: 1
    #    2: 2 3
    #    3: 4 5 6
    #    4: 7 8 9 10
    #
class CountSgraphOccurences:
    
    def __init__(self,sdms,nodes_sublist,threshold=3):
        """ 
        @param sdms:            SubunitPairDistanceMatrixSet
        @param nodes_sublist:   what nodes to consider in the graph (used to restrict the study to a subset of nodes)
        @param threshold:       threshold to consider subunits to be in contact
        """
        self._nb_configs    = sdms.get_number_of_configurations()
        self._graph         = []   # confoguration_index -> graph_index
        
        self._nodes         = nodes_sublist
        self._nb_nodes      = len(nodes_sublist)
        self._nb_edges      = self._nb_nodes*(self._nb_nodes-1)/2
        self._nb_graphs     = pow(2,self._nb_edges)
        self._counter       = [0] * self._nb_graphs # graph_index -> how many configurations 
        self._graphInd2Pairs= []    # map the index of an edge to the pair of linked nodes
        for i in range(1,self._nb_nodes):
            name1=self._nodes[i]
            for j in range(0,i):
                name2=self._nodes[j]
                self._graphInd2Pairs.append( (name1,name2) )
        
        def compute_sgraph_index_from_matrix(sdm,threshold = 5):
            """
            @param sdm:        subunit distance matrix
            @param threshold:  maximum distance to consider subunits to be in contact
            """
            index=0
#            i_index = -1
            for i in range(1,self._nb_nodes):
                name1=self._nodes[i]
#                i_index += i
                for j in range(0,i):
                    name2=self._nodes[j]
                    if sdm.get_value(name1, name2) < threshold:
#                        index += pow(2,i_index + j)
#                        index += (i*(i-1)/2)+j
                        index += pow(2,(i*(i-1)/2)+j) ## FIX 
            return index
        
        for config_index in range(0,sdms.get_number_of_configurations()):
            sdm                          = sdms.get_matrix(config_index)
            graph_index                  = compute_sgraph_index_from_matrix(sdm,threshold)
#            print config_index,"-->",graph_index
            try :
                self._counter[graph_index]  += 1
            except :
                print "access crashed ",len(self._counter),graph_index
                raise
            self._graph.append(graph_index)

    def get_graph_indices_with_count_above(self,threshold=0):
        graph_indices=[]
        for graph_index in range(0,self._nb_graphs) :
            if  self._counter[graph_index] >= threshold :
                graph_indices.append(graph_index)
        return graph_indices

    def show_graphs_with_count_above(self,threshold):
        lines = []
        lines.append("-- CountSgraphOccurences with (nb nodes:"+str(self._nb_nodes)+") (nb graphs:"+str(self._nb_graphs)+") --")
        lines.append("graph index - count - edges")
        graph_indices = self.get_graph_indices_with_count_above(threshold)
        for gi in graph_indices :
            count           = self._counter[gi]
#            edge_list = self._get_graph_edges(gi)
            graph_edges     = self.get_sgraph_edges_as_string(gi)
            lines.append( ":".join( [str(gi),str(count),graph_edges] ) )
        print "\n".join(lines)

    def __repr__(self):
##        return str(self._counter)
#        edges=[]
#        for i in range(0,self._nb_graphs) :
#            if self._counter[i] > 0 :
#                edges.append(":".join([str(i),str(self._counter[i]),self.show_sgraph(i)]))
#        ret_string = "-- graph counter (nb nodes:"+str(self._nb_nodes)+") (nb graphs:"+str(self._nb_graphs)+")\n"+"\n".join(edges)
#        return ret_string 
##        return str([c for c in self._counter if c> 60])
        lines = []
        lines.append("-- CountSgraphOccurences with (nb nodes:"+str(self._nb_nodes)+") (nb graphs:"+str(self._nb_graphs)+") --")
        lines.append("graph index - count - edges")
        graph_indices = self.get_graph_indices_with_count_above(0)
        for gi in graph_indices :
            count           = self._counter[gi]
#            edge_list = self._get_graph_edges(gi)
            graph_edges     = self.get_sgraph_edges_as_string(gi)
            lines.append( ":".join( [str(gi),str(count),graph_edges] ) )
        return "\n".join(lines)

    def _get_edge_index_from_nodes(self,node1,node2):
        try :
            node_indices    = [self._nodes.index(node1),self._nodes.index(node2)]
        except :
            raise KeyError( "keys " + str( (node1,node2) ) + " are not found in nodes list : " + str(self._nodes) )
        node_indices.sort()
        j,i = node_indices
        edge_index      = ( (i)*(i-1) / 2 ) + j
#        print "edge index : ",node1,node2,edge_index
        return edge_index

    def _has_edge(self,edge_index,graph_index):
        return ( ( graph_index / pow(2,edge_index) ) % 2 ) == 1

    def _has_edge_from_nodes(self,node1,node2,graph_index):
        edge_index = self._get_edge_index(self,node1,node2)
        return self._has_edge(edge_index, graph_index) 
    
    def _get_graph_edges(self,graph_index):
        edges=[]
        for i in range(0,self._nb_edges):
            if graph_index%2 == 1:
                edges.append(i)
            graph_index/=2
        return edges
    
    def get_sgraph_edges_as_string(self,graph_index):
        edges           = self._get_graph_edges(graph_index)
        pretty_edges    = ["-".join(self._graphInd2Pairs[e]) for e in edges]
        return "("+ ",".join(pretty_edges) +")"
    
#    def show_sgraph(self,graph_index):
#        node_pairs=[]
##        pow_of_two = 2
##        gis_debug = []
#        for i in range(0,self._nb_edges):
#            if graph_index%2 == 1:
#                node_pairs.append( "-".join(self._graphInd2Pairs[i]) )
#            graph_index/=2
##            gis_debug.append(str(graph_index))
#        return ":".join(node_pairs)
##            "("+"-".join(gis_debug)+")"
    
    def get_count(self,graph_index):
        return self._counter[graph_index]
    
#    def get_sgraph(self,graph_index):
#        pass

    def get_graph_indices_with_all_edges(self,node_pairs_list):
        edge_list=[]
        for p in node_pairs_list :
            edge_list.append( self._get_edge_index_from_nodes(p[0], p[1]) )
        graph_indices=[]
        for graph_index in range(0,self._nb_graphs) :
            all_edge_there = True
            for edge_index in edge_list:
                if not self._has_edge(edge_index, graph_index) :
                    all_edge_there = False
                    break
            if all_edge_there :
                graph_indices.append( graph_index )
        return graph_indices
    
    def get_graph_indices_with_one_edge(self,node_pairs_list):
        edge_list=[]
        for p in node_pairs_list :
            edge_list.append( self._get_edge_index_from_nodes(p[0], p[1]) )
        graph_indices=[]
        for graph_index in range(0,self._nb_graphs) :
            for edge_index in edge_list:
                if self._has_edge(edge_index, graph_index) :
                    graph_indices.append( graph_index )
                    break
        return graph_indices

    def get_graph_indices_with_all_edges_missing(self,node_pairs_list):
        edge_list=[]
        for p in node_pairs_list :
            edge_list.append( self._get_edge_index_from_nodes(p[0], p[1]) )
        graph_indices=[]
        for graph_index in range(0,self._nb_graphs) :
            all_edges_broken = True
            for edge_index in edge_list:
                if self._has_edge(edge_index, graph_index) :
                    all_edge_broken = False
                    break
            if all_edge_broken :
                graph_indices.append( graph_index )
        return graph_indices  

    def get_graph_indices_with_one_edge_missing(self,node_pairs_list):
        edge_list=[]
        for p in node_pairs_list :
            edge_list.append( self._get_edge_index_from_nodes(p[0], p[1]) )
        graph_indices=[]
        for graph_index in range(0,self._nb_graphs) :
            for edge_index in edge_list:
                if not self._has_edge(edge_index, graph_index) :
                    graph_indices.append( graph_index )
        return graph_indices
    
    def get_accumulated_count(self,graph_indices):
        count = 0
        for gi in graph_indices :
            count += self._counter[gi]
        return count
    
    def get_count_with_all_edges(self,node_pairs_list):
        """ how many observed graphs do have the specified list of edges 
        @param node_pairs_list: a list of edges provided as node tags"""
        # first, transform our node pair list in edge indices
        edge_list=[]
        for p in node_pairs_list :
            edge_list.append( self._get_edge_index_from_nodes(p[0], p[1]) )
            
        count = 0
        for graph_index in range(0,self._nb_graphs) :
            nb_occur_graph_index = self.get_count(graph_index)
            if nb_occur_graph_index > 0 : # no need to work if the graph is not observed
                all_edge_there = True
                for edge_index in edge_list:
                    if not self._has_edge(edge_index, graph_index) :
                        all_edge_there = False
                        break
                if all_edge_there :
                    count += nb_occur_graph_index
        return count
    
    def get_count_without_one_of_edges(self,node_pairs_list):
        """ how many observed graphs do not have any of the specified edges 
        @param node_pairs_list: a list of edges provided as node tags"""
        # first, transform our node pair list in edge indices
        edge_list=[]
        for p in node_pairs_list :
            edge_list.append( self._get_edge_index_from_nodes(p[0], p[1]) )
            
        count = 0
        for graph_index in range(0,self._nb_graphs) :
            nb_occur_graph_index = self.get_count(graph_index)
            if nb_occur_graph_index > 0 : # no need to work if the graph is not observed
                all_edges_broken = True
                for edge_index in edge_list:
                    if self._has_edge(edge_index, graph_index) :
                        all_edges_broken = False
                        break
                if all_edges_broken :
                    count += nb_occur_graph_index
        return count
    
    def get_number_of_configurations(self):
        return self._nb_configs
    
    def get_graph(self,configuration_index):
        return self._graph[configuration_index]
    
    def get_configurations(self,graph_index):
        return [ i for i in range(0,self.get_number_of_configurations()) if self._graph[i] == graph_index ]
    
    
