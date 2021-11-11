# There are no restrictions on how you must store
# class or instance variables for this project.
# Use whatever makes the most sense for your 
# design and implementation.


class node:
    def __init__(self, label):
        """
        Parameter: a string indicating the label of the new node
        """
        self.label = label # Get the label of node
        self.neighbors = [] # Store adjacent nodes
        self.in_degree_n = 0 # Initialize in degree
        self.out_degree_n = 0 # Initialize out degree

    def __str__(self):
        # Return label as string
        return str(self.label)

    def in_degree(self):
        """
        Parameter: none
        Return value: integer representing the in-degree of 
        this node
        """
        return self.in_degree_n
        
    def out_degree(self):
        """
        Parameter: none
        Return value: integer representing the out-degree of 
        this node
        """
        return self.out_degree_n
        
class Graph:
    def __init__(self, directed):
        """
        Parameter: a boolean indicating whether the new instance 
        of Graph will be directed (True) or undirected (False)
        Post condition: new instance of an empty graph is 
        created
        """
        self.directed = directed # Get value of whether graph is directed or not
        self.graph = {} # Complete graph contain all information of nodes
        self.node_list = [] # List that hold nodes only
        self.weight = 1 # Initialize graph's weight 
        self.edge_num = 0 # Initialize number of edges

    def num_vertices(self):
        """
        Parameters: none
        Return value: integer corresponding to the total number
        of vertices in the graph
        """
        return len(self.node_list)

    def num_edges(self):
        """
        Parameters: none
        Return value: integer corresponding to the total number
        of edges in the graph
        """
        return self.edge_num
    
    def is_directed(self):
        """
        Parameters: none
        Return value: boolean - True if this instance of the 
        Graph class is a directed graph, False otherwise
        """
        return self.directed

    def is_weighted(self):
        """
        Parameters: none
        Return value: boolean - True if any edge in the Graph
        has a weight other than 1, False otherwise
        """
        if self.weight != 1:
            return True
        else:
            return False

    def add_node(self, label):
        """
        Parameter: a string indicating the label of a new node
        in the Graph
        Return value: none
        Assumptions: labels of nodes in the Graph must be unique
        """      
        node_label = node(label)

        # Don't add duplicate node
        if label not in self.node_list:
            self.node_list.append(label)
            self.graph[node_label.label] = {'out_degree' : node_label.out_degree(), 'in_degree' : node_label.in_degree(), 'neighbors' : node_label.neighbors}
        else:
            raise DuplicateNode
    
    def remove_node(self, label):
        """
        Parameter: a string indicating the label of an existing
        node in the Graph
        Return value: none
        Post conditions: the node with the given label, as well 
        as any edges to/from that node, are removed from the 
        graph
        """
        if label not in self.node_list:
            raise NodeNotFound
        
        # Delete node from node that have it has neighbor
        for i in self.node_list:
            for neighbor in self.graph[i]['neighbors']:
                if neighbor == label:
                    self.graph[i]['neighbors'].remove(label)
        # Delete node from graph
        del self.graph[label]
        # Delte node from node list
        self.node_list.remove(label)

        # Recalculate in degree and out degree
        for i in self.graph:
            self.graph[i]['out_degree'] = len(self.graph[i]['neighbors'])
        
        for i in self.graph:
            in_degree = 0
            for j in self.graph:
                for n in self.graph[j]['neighbors']:
                    if i == n:
                        in_degree += 1          
                self.graph[i]['in_degree'] = in_degree
    
    def add_edge(self, n1, n2, weight = 1):
        """
        Parameters: 
            two strings, indicating the labels of the 
            nodes connected by the new edge. If this is a directed 
            Graph, then the edge will be FROM n1 TO n2.

            a numeric value (int/float) for a weight of the edge
        Return value: none
        Assumptions: the combination of (n1, n2, weight) must 
        be unique in the Graph
        Post conditions: one new edge is added to the Graph
        """
        l1 = node(n1)

        # No duplicate edge
        if n1 not in self.node_list or n2 not in self.node_list:
            raise NodeNotFound
        if n1 in self.graph[n2]['neighbors'] or n2 in self.graph[n1]['neighbors']:
            raise DuplicateEdge

        # Update edge number
        self.edge_num += 1

        # Update weight
        if (weight != 1):
            self.weight += weight

        if self.is_directed():
            # Prevent making graph from directed to non-directed  
            self.graph[n1]['neighbors'].append(n2)
        else: 
            self.graph[n1]['neighbors'].append(n2)
            self.graph[n2]['neighbors'].append(n1)
        
        # Count in degree and out degree by nodes' neighbors
        for i in self.graph:
            for j in self.graph[i]['neighbors']:
                if j == n2:
                    l1.in_degree_n +=1

        # Assign in degree and out degree
        self.graph[n2]['in_degree'] = l1.in_degree_n
        l1.out_degree_n = len(self.graph[n1]['neighbors'])
        self.graph[n1]['out_degree'] = l1.out_degree_n 
        
    
    def remove_edge(self, n1, n2, weight = 1):
        """
        Parameters: 
            two strings, indicating the labels of the 
            nodes connected by the edge. If this is a directed 
            Graph, then the edge will be FROM n1 TO n2.

            a numeric value (int/float) for a weight of the edge
        Return value: none
        Post conditions: the edge with the given nodes and weight
        is removed from the graph
        """
        # Make sure edge exist before delete
        if self.has_edge(n1, n2) == False:
            raise EdgeNotFound
        if self.is_directed:
            self.graph[n1]['neighbors'].remove(n2)
        else:
            self.graph[n2]['neighbors'].remove(n1)
            self.graph[n1]['neighbors'].remove(n2)

        # Update weight
        if (weight != 1):
            self.weight - weight

        # Update number of edges
        self.edge_num -= 1

        # Recalculate in degree and out degree
        for i in self.graph:
            self.graph[i]['out_degree'] = len(self.graph[i]['neighbors'])
        
        for i in self.graph:
            in_degree = 0
            for j in self.graph:
                for n in self.graph[j]['neighbors']:
                    if i == n:
                        in_degree += 1          
                self.graph[i]['in_degree'] = in_degree
    
    def BFS(self, source):
        """
        Parameter: a string indicating the label of an existing 
        node in the Graph
        Return value: a list of node objects, which is the 
        Breadth First Search starting at source
        """
        visited = [False]*(int(max(self.node_list)) + 1) # Create list for visited node
        list = [] # Create list to hold the node
        queue = [] # Create queue getting the first node
        queue.append(source) # Add root node first
        visited[int(source)] = True # Mark root node as visited
        while queue:
            source = queue.pop(0)
            list.append(source)
            for i in self.graph[source]['neighbors']:
                if visited[int(i)] == False:
                    queue.append(i)
                    visited[int(i)] = True
                    
        return list
    
    def DFS(self, source):
        """
        Parameter: a string indicating the label of an existing 
        node in the Graph
        Return value: a list of node objects, which is the 
        Depth First Search starting at source
        """
        visited = set() # Create set for visited node
        list = [] # Create empty list to hold the node
        # Create separate function for recursive sake
        list = self.depth_first_search(source, visited, list)
        return list

    def depth_first_search(self, source, visited, list):
        visited.add(source)
        list.append(source)
        
        # Recursively check if node has been visited
        for neighbor in self.graph[source]['neighbors']:
            if neighbor not in visited:
                self.depth_first_search(neighbor, visited, list)
        return list
          
    def has_edge(self, n1, n2):
        """
        Parameters: 
            two strings, indicating the labels of the 
            nodes connected by the new edge. If this is a directed 
            Graph, then the edge will be FROM n1 TO n2.
        Return value: a boolean - True if there is an edge in the 
            Graph from n1 to n2, False otherwise
        """
        # Make sure node exists
        if n1 not in self.node_list or n2 not in self.node_list:
            raise NodeNotFound
        if self.is_directed():
            if n2 in self.graph[n1]['neighbors']:
                return True
            else:
                return False
        else:
            if n2 in self.graph[n1]['neighbors'] or n1 in  self.graph[n2]['neighbors']:
                return True
            else:
                return False
    
    def get_path(self, n1, n2):
        """
        Parameters: 
            two strings, indicating the labels of the 
            nodes you wish to find a path between. The path will be
            FROM n1 TO n2.
        Return value: a list L of node objects such that L[0] has 
            label n1, L[-1] has label n2, and for 1 <= i <= len(L) - 1,
            the Graph has an edge from L[i-1] to L[i]
        """
        # Make sure node exists
        if n1 not in self.node_list or n2 not in self.node_list:
            raise NodeNotFound
        queue = [] # Create empty queue to get first node
        queue.append(n1) # Add root node
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == n2:
                return path
            for i in self.graph[node]['neighbors']:
                new_path = list(path)
                new_path.append(i)
                queue.append(new_path)
    
    def get_adjacent_nodes(self, label):
        """
        Parameter: a string indicating the label of an existing 
        node in the Graph
        Return value: a list of node objects containing all nodes
        adjacent to the node with the given label
        """
        if label not in self.node_list:
            raise NodeNotFound
        # Return neighbors of that node
        return self.graph[label]['neighbors']

# Exceptions
class DuplicateNode(Exception):
    pass
class NodeNotFound(Exception):
    pass
class DuplicateEdge(Exception):
    pass
class EdgeNotFound(Exception):
    pass


"""
If a label is provided that is supposed to exist in the Graph
and a node with that label does not exist, the method should raise 
a "NodeNotFound" exception.

If the remove_edge method is called for an edge that does not 
exist in the Graph, the method should raise an "EdgeNotFound"
exception.

If a method call would result in a duplicate label or duplicate 
edge being added to the Graph, a "DuplicateNode" or "DuplicateEdge"
exception should be raised.

If you are not familiar with defining custom exceptions in Python3,
it's not too complicated. Check out this source for explanation and
examples:
https://www.askpython.com/python/python-custom-exceptions
"""