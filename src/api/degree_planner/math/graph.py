'''
graphs and bfs searching
'''

import copy
import queue

from ..dp.fulfillment_status import Fulfillment_Status

class Edge_Generator():

    def __init__(self):
        pass

    def edge_data(self, node1, node2):
        return '1'
    
    def zero_value(self, value) -> bool:
        return value is None
    
    def print_edge(self, value) -> str:
        return '-' if value is None else str(value)

class Backwards_Overlap(Edge_Generator):

    def __init__(self, all_fulfillment:dict, max_fulfillment:dict):
        self.max_fulfillment = max_fulfillment
        self.all_fulfillment = all_fulfillment

    def edge_data(self, node1:Fulfillment_Status, node2:Fulfillment_Status):
        return self.all_fulfillment.get(node1).get_fulfillment_set().intersection(self.max_fulfillment.get(self.all_fulfillment.get(node2).get_template()).get_fulfillment_set())
    
    def zero_value(self, value):
        return value is None or not len(value)
    
    def print_edge(self, value) -> str:
        return '-' if self.zero_value(value) else ', '.join([str(e) for e in value])
    
class Forwards_Overlap(Edge_Generator):

    def __init__(self, all_fulfillment:dict, max_fulfillment:dict):
        self.max_fulfillment = max_fulfillment
        self.all_fulfillment = all_fulfillment

    def edge_data(self, node1:Fulfillment_Status, node2:Fulfillment_Status):
        return self.all_fulfillment.get(node1).get_fulfillment_set().intersection(self.max_fulfillment.get(self.all_fulfillment.get(node2).get_template()).get_fulfillment_set())
    
    def zero_value(self, value):
        return value is None or not len(value)
    
    def print_edge(self, value) -> str:
        return '-' if self.zero_value(value) else ', '.join([str(e) for e in value])
    
class Edge_Id_Iterator():

    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        for i in range(len(self.graph.grid)):
            for j in range(len(self.graph.grid[i])):
                if self.graph.edge_data_gen.zero_value(self.graph.grid[i][j]):
                    continue
                yield (i, j)

class Edge_Node_Iterator():

    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        for i in range(len(self.graph.grid)):
            for j in range(len(self.graph.grid[i])):
                if self.graph.edge_data_gen.zero_value(self.graph.grid[i][j]):
                    continue
                yield (self.graph._node_object(i), self.graph._node_object(j))

class Edge_Data_Iterator():

    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        for i in range(len(self.graph.grid)):
            for j in range(len(self.graph.grid[i])):
                if self.graph.edge_data_gen.zero_value(self.graph.grid[i][j]):
                    continue
                yield self.graph.grid[i][j]

class Edge_Items_Iterator():
    '''
    returns (n1, n2, value)
    '''

    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        for i in range(len(self.graph.grid)):
            for j in range(len(self.graph.grid[i])):
                if self.graph.edge_data_gen.zero_value(self.graph.grid[i][j]):
                    continue
                yield (self.graph._node_object(i), self.graph._node_object(j), self.graph.grid[i][j])

class BFS_data():
    '''
    stores shortest paths that traces from any root to that node

    if node isn't found, that means it isn't connected to any roots
    '''

    def __init__(self, start_nodes:set):
        self.paths = dict()
        self.bfs_queue = queue.SimpleQueue()

        for node in start_nodes:
            self.add_path(node, [node])

    def add_path(self, node, path:list):
        self.paths.update({node:path})
        self.bfs_queue.put(node)

    def remove_path(self, node):
        self.paths.pop(node, None)

    def get_path(self, node):
        return self.paths.get(node, None)
    
    def contains_node(self, node):
        return self.paths.get(node, None) is not None
    
    def contains_child(self, node):
        if not self.contains_node(node):
            return False
        return len(self.paths.get(node)) > 1
    
    def next(self):
        return self.bfs_queue.get()
    
    def has_next(self):
        return not self.bfs_queue.empty()
    
    def __len__(self):
        return len(self.paths)
    
    def __repr__(self):
        rstr = f'\nbfs paths:\n'
        for node, path in self.paths.items():
            rstr += f"  {str(node).ljust(10)}: {' -> '.join([str(e) for e in path])}\n"
        return rstr


class Graph():
    '''
    adjacency graph that can store sets as edge data
    '''

    def __init__(self, nodes:set=None, edge_data_gen:Edge_Generator=None):
        if nodes is None:
            nodes = set()

        if edge_data_gen is None:
            self.edge_data_gen = Edge_Generator()
        else:
            self.edge_data_gen = edge_data_gen
        
        self.grid = [[None for j in range(len(nodes))] for i in range(len(nodes))]
        self.nodes_obj_to_id = dict()
        self.nodes_id_to_obj = dict()
        self.roots = set()
        count = 0
        for node in nodes:
            self.nodes_obj_to_id.update({node:count})
            self.nodes_id_to_obj.update({count:node})
            count += 1

    
    def compute_overlap(self, node1, node2):
        return self.edge_data_gen.edge_data(node1, node2)
    

    def add_node(self, node, compute_overlap=True, data_set=None):
        if node in self:
            return False
        
        for row in self.grid:
            row.append(None)
        self.grid.append([None for j in range(len(self.grid) + 1)])
        self.nodes_obj_to_id.update({node:len(self.grid) - 1})
        self.nodes_id_to_obj.update({len(self.grid) - 1:node})

        if compute_overlap:
            for target_node in self.nodes_obj_to_id.keys():
                self.update_connection(node, target_node, data_set)
                self.update_connection(target_node, node, data_set)

        return True

    
    def remove_node(self, node):
        if node not in self:
            return False
        
        id = self.nodes_obj_to_id.get(node)

        # if it's the last one:
        if id == len(self.grid) - 1:
            self.grid.pop(-1)
            for row in self.grid:
                row.pop(-1)
            self.nodes_obj_to_id.pop(node)
            self.nodes_id_to_obj.pop(id)
            return True
        
        last_pos = len(self.grid) - 1
        moved_node = self.nodes_id_to_obj.get(last_pos)
        
        # bring the last element's info to the deleted element's place
        self.grid[id] = self.grid[-1]
        self.grid.pop(-1)

        # bring every element's last element to the deleted element's place
        for row in self.grid:
            row[id] = row[-1]
            row.pop(-1)

        self.nodes_obj_to_id.pop(node)
        self.nodes_obj_to_id.update({moved_node:id})
        self.nodes_id_to_obj.pop(last_pos)
        self.nodes_id_to_obj.update({id:moved_node})

        return True


    def update_all_connections(self, data=None):
        for node_origin in self.nodes_obj_to_id.keys():
            for node_to in self.nodes_obj_to_id.keys():
                self.update_connection(node_origin, node_to, data)


    def update_connection(self, node_origin, node_to, data_set:set=None):
        '''
        add a connection from node_origin to node_to
        '''
        if node_origin == node_to:
            return
        if data_set is None:
            data_set = self.compute_overlap(node_origin, node_to)
        self.grid[self._node_id(node_origin)][self._node_id(node_to)] = data_set


    def remove_connection(self, node_origin, node_to):
        '''
        remove a connection from node_origin to node_to
        '''
        if node_origin == node_to:
            return
        self.grid[self._node_id(node_origin)][self._node_id(node_to)] = None


    def outbound_connections(self, node) -> set:
        '''
        returns set of nodes this node connects to
        '''
        id = self._node_id(node)
        connected_nodes = set()
        for i in range(0, len(self.grid)):
            if not self.edge_data_gen.zero_value(self.grid[id][i]):
                connected_nodes.add(self._node_object(i))
        return connected_nodes


    def inbound_connections(self, node) -> set:
        '''
        returns set of nodes that connect to this node
        '''
        id = self._node_id(node)
        connected_nodes = set()
        for i in range(0, len(self.grid)):
            if not self.edge_data_gen.zero_value(self.grid[i][id]):
                connected_nodes.add(self._node_object(i))
        return connected_nodes
    
    
    def edge_data(self, node1, node2, first_element_of_set:bool=False):
        elements = self.grid[self._node_id(node1)][self._node_id(node2)]
        if first_element_of_set and len(elements):
            for e in elements:
                return e
        return elements


    def _node_id(self, node) -> int:
        '''
        return node id from node obj
        '''
        return self.nodes_obj_to_id.get(node, None)


    def _node_object(self, id):
        '''
        return node obj from node id
        '''
        return self.nodes_id_to_obj.get(id, None)


    def bfs(self, start_nodes:set=None) -> BFS_data:
        '''
        find BFS paths from links
        '''
        if start_nodes is None:
            start_nodes = set()

        start_nodes.update(self.roots)
            
        bfs = BFS_data(start_nodes)
        while bfs.has_next():
            node_current = bfs.next()
            for node_next in self.outbound_connections(node_current):
                if bfs.contains_node(node_next):
                    continue
                trace = copy.deepcopy(bfs.get_path(node_current))
                trace.append(node_next)
                bfs.add_path(node_next, trace)

        return bfs
    

    def _edge_endpoints_id(self):
        '''
        INTERNAL USE: gets the internal node ids of each connection
        '''
        return Edge_Id_Iterator(self)
    

    def edge_endpoints(self):
        '''
        returns an iterator containing (node1, node2) representing the endpoints of every edge
        '''
        return Edge_Node_Iterator(self)
    

    def edge_values(self):
        '''
        iterators through every edge's value
        '''
        return Edge_Data_Iterator(self)
    

    def edge_items(self):
        '''
        returns an iterator containing (node1, node2, value) representing the two endpoints and
        the value of every edge
        '''
        return Edge_Items_Iterator(self)


    def __repr__(self):
        WIDTH = 12
        STAGGERED = False
        if not STAGGERED:
            rstr = f"\n{'links'.ljust(WIDTH)}{''.join([str(self._node_object(i)).ljust(WIDTH) for i in range(0, len(self))])}\n"
            for i in range(0, len(self.grid)):
                rstr += str(self._node_object(i)).ljust(WIDTH)
                for j in range(0, len(self.grid)):
                    data_set = self.grid[i][j]
                    value = self.edge_data_gen.print_edge(data_set)
                    if len(value) > 8:
                        value = value[:8]
                    rstr += value.ljust(WIDTH)
                rstr += '\n'
            return rstr
        
        WIDTH += 12
        rstr = ''
        for i in range(0, len(self.grid)):
            rstr += f"\n\n{'links of'.ljust(WIDTH)}{(self._node_object(i))}\n"
            for j in range(0, len(self.grid)):
                data_set = self.grid[i][j]
                value = self.edge_data_gen.print_edge(data_set)
                if len(value) > 8:
                    value = value[:8]
                rstr += f'{str(self._node_object(j)).ljust(WIDTH)} {value.ljust(WIDTH)}'
                rstr += '\n'
        return rstr
    

    def __iter__(self):
        '''
        iterates through every node in the graph
        '''
        for key in self.nodes_obj_to_id.keys():
            yield(key)
    

    def __contains__(self, element):
        '''
        returns whether a node is inside this graph
        '''
        return self.nodes_obj_to_id.get(element, None) is not None
    

    def __eq__(self, other):
        return self.grid == other.grid and self.nodes_obj_to_id == other.nodes_name_to_id
   

    def __len__(self):
        return len(self.grid)
