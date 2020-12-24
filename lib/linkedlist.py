from copy import deepcopy

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return "Node(" + str(self.data) + ") -> " + str(self.next.data)

# https://www.javatpoint.com/python-program-to-create-and-display-a-circular-linked-list
class CircularLinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next
            node.next = self.head

    # This function will add the new node at the end of the list.
    def add(self, data):
        newNode = Node(data)
        # Checks if the list is empty.
        if self.head is None:
            # If list is empty, both head and tail would point to new node.
            self.head = newNode
            newNode.next = self.head
        else:
            node = None
            for n in self:
                node = n
            node.next = newNode
            newNode.next = self.head

    # Displays all the nodes in the list
    def display(self):
        current = self.head
        if not self.head:
            raise Exception("List is empty")
        else:
            print("Nodes of the circular linked list: ")
            #Prints each node by incrementing pointer.
            print(current.data),
            while current.next != self.head:
                current = current.next
                print(current.data),

    def add_after(self, target_node_data, new_node):
        if not self.head:
            raise Exception("List is empty")
        for node in self:
            if node.data == target_node_data:
                new_node.next = node.next
                node.next = new_node
                return
        raise Exception("Node with data '%s' not found" % str(target_node_data))

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
            if node == self.head:
                break

    def __repr__(self):
        nodes = []
        for node in self:
            nodes.append(str(node.data))
        return " -> ".join(nodes)

    def find(self, target_node_data):
        if not self.head:
            raise Exception("List is empty")
        for node in self:
            if node.data == target_node_data:
                return node
        raise Exception("Node with data '%s' not found" % target_node_data)

    def remove_node_with_data(self, target_node_data):
        if not self.head:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            # find whatever was pointing to head :/
            for node in self:
                if node.next == self.head:
                    node.next = self.head.next
                    break
            self.head = self.head.next

        previous_node = self.head
        for node in self:
            if node.data == target_node_data:
                res = deepcopy(node)
                previous_node.next = node.next
                return res
            previous_node = node

        raise Exception("Node with data '%s' not found" % str(target_node_data))

if __name__ == '__main__':
    test = CircularLinkedList([1,2,3])
    test.add(4)
    test.add_after(4,Node(10))
    print(test)
    test.remove_node_with_data(3)
    print(test)
    three = test.find(10)
    print(three)