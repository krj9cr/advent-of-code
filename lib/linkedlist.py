from copy import deepcopy

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data

class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    def add_first(self, node):
        node.next = self.head
        self.head = node

    def add_last(self, node):
        if not self.head:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.next = node

    def find(self, target_node_data):
        if not self.head:
            raise Exception("List is empty")
        for node in self:
            if node.data == target_node_data:
                return node
        raise Exception("Node with data '%s' not found" % target_node_data)

    def add_after(self, target_node_data, new_node):
        if not self.head:
            raise Exception("List is empty")
        for node in self:
            if node.data == target_node_data:
                new_node.next = node.next
                node.next = new_node
                return
        raise Exception("Node with data '%s' not found" % str(target_node_data))

    def remove_node_with_data(self, target_node_data):
        if not self.head:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            res = deepcopy(self.head)
            self.head = self.head.next
            return res

        previous_node = self.head
        for node in self:
            if node.data == target_node_data:
                res = deepcopy(node)
                previous_node.next = node.next
                return res
            previous_node = node

        raise Exception("Node with data '%s' not found" % str(target_node_data))

    def remove_node(self, target_node):
        if not self.head:
            raise Exception("List is empty")

        if self.head.data == target_node.data:
            self.head = self.head.next

        previous_node = self.head
        for node in self:
            if node.data == target_node.data:
                previous_node.next = node.next
            previous_node = node

        raise Exception("Node with data '%s' not found" % str(target_node.data))

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.data))
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)