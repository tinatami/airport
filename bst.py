""" Tina Tami

    This file implements the BST class with all its
    necessary functions. Helper functions are added as well. 
"""

from node import Node

class BST(object):
    def __init__(self, key_list=[]):
        """ Create a new BST, set its attributes, and insert all the keys in
            the key_list into the BST. """
        self.root = None
        if (len(key_list) > 0):
            for key in key_list:
                self.insert(key, value=None)
    
    def get_root(self):
        """ Return the root of the BST. """
        return self.root
    
    def is_empty(self):
        """ Return True if the BST is empty. """
        if (self.root == None):
            return True
        return False
    
    def find_max(self):
        """ Return the node with the maximum key in the BST. """
        if (self.root == None):
            return None
        root = self.root
        while (root != None):
            if (root.right_child == None):
                return root
            root = root.right_child
        return None
    
    def find_min(self):
        """ Return the node with the minimum key in the BST. """
        if (self.root == None):
            return None
        root = self.root
        while (root != None):
            if (root.left_child == None):
                return root
            root = root.left_child
        return None

    def search_min(self, node):
        """ Return the node with the minimum key in the subtree. """
        root = node
        if (root == None):
            return None
        while (root != None):
            if (root.left_child == None):
                return root
            root = root.left_child
        return None
    
    def search(self, key):
        """ Return the Node object containing the key if the key exists in
            the BST, else return None. """
        if (self.root == None):
            return None
        root = self.root
        while (root != None):
            if (root.key == key):
                return root
            elif (key > root.key):
                root = root.right_child
            elif (key < root.key):
                root = root.left_child
        return None
    
    def contains(self, key):
        """ Return True if the key exists in the BST, else return False. """
        if (self.root == None):
            return False
        root = self.root
        while (root != None):
            if (root.key == key):
                return True
            elif (key > root.key):
                root = root.right_child
            elif (key < root.key):
                root = root.left_child
        return False

    def two_kids(self, node):
        """ Returns True if node has two children, else returns False. """
        if (self.root == None):
            return False
        left = node.left_child
        right = node.right_child
        if (left and right):
            return True
        return False

    def count_key(self, key):
        """ Counts the ammount of steps that need to be taken
            to reach the specified key in the tree. """
        counter_key = 0
        root = self.root
        while (root != None):
            if (root.key == key):
                return counter_key
            elif (key > root.key):
                root = root.right_child
                counter_key += 1
            elif (key < root.key):
                root = root.left_child
                counter_key += 1
        return counter_key

    def insert_height_fix(self, parent, new_node_key):
        """ Makes sure the height of the relevant nodes are
            updated when inserting a new node. The final if-statement
            checks if the root height has to be adjusted as well. """
        if (not self.two_kids(parent)):
            node = parent
            while (node != self.root):
                node.height += 1
                node = node.parent 
        counter_key = self.count_key(new_node_key)
        if (counter_key > self.root.height):
            self.root.height = counter_key
        pass

    def insert(self, key, value=None):
        """ Create a new node for this key and value, and insert it into the BST.
            Return the new inserted node, or None if the key and value could not
            be inserted. """
        new_node = Node(key, value)
        if (self.root == None):
            self.root = new_node
            self.root.height = 0
            return new_node
        root = self.root
        parent = None

        # Find the  spot where the new node will be placed
        while (root != None):
            parent = root
            if (key > root.key):
                root = root.right_child
            elif (key < root.key):
                root = root.left_child
            elif (key == root.key):
                return None

        # Place the new node at the left or right side
        if (key > parent):
            parent.right_child = new_node
            new_node.parent = parent
            self.insert_height_fix(parent, new_node.key)
            return new_node

        if (key < parent):
            parent.left_child = new_node
            new_node.parent = parent
            self.insert_height_fix(parent, new_node.key)
            return new_node
        return None

    def fix_height_down(self, parent):
        """ Makes the height of the relevant nodes one less
            whenever a node is deleted. """
        node = parent
        while (node != self.root):
            node.height -= 1
            node = node.parent 
        pass

    def delete_height_fix(self, root):
        """ Makes the height of the root node one less
            when this is necessary. """
        root.height -= 1
        tree = self.in_order_traversal()
        for element in tree:
            if (element.height >= root.height and element.key != root.key):
                root.height += 1
                break

    def delete_no_kids(self, delete, root):
        """ Handles the delete-function when the node
            we want to delete has no children. """
        parent = delete.parent
        if (not self.two_kids(parent)):
            self.fix_height_down(parent)
        if (delete == parent.right_child):
            parent.right_child = None
        elif (delete == parent.left_child):
            parent.left_child = None
        temp = delete
        delete = None
        self.delete_height_fix(root)
        return temp

    def delete_right_kid(self, delete, root):
        """ Handles the delete-function when the node
            we want to delete only has a right child. """
        parent = delete.parent
        if (not self.two_kids(delete)):
            self.fix_height_down(delete)
        child = delete.right_child

        # Handles case if the node to delete is a right child
        if (delete == parent.right_child):
            parent.right_child = child
            temp = delete
            delete = None
            child.parent = parent
            self.delete_height_fix(root)
            return temp

        # Handles case if the node to delete is a left child
        elif (delete == parent.left_child):
            parent.left_child = child
            temp = delete
            delete = None
            child.parent = parent
            self.delete_height_fix(root)
            return temp

    def delete_left_kid(self, delete, root):
        """ Handles the delete-function when the node
            we want to delete only has a right child. """
        parent = delete.parent
        if (not self.two_kids(delete)):
            self.fix_height_down(delete)
            child = delete.left_child

        # Handles case if the node to delete is a right child
        if (delete == parent.right_child):
            parent.right_child = child
            temp = delete
            delete = None
            child.parent = parent
            self.delete_height_fix(root)
            return temp

        # Handles case if the node to delete is a left child
        elif (delete == parent.left_child):
            parent.left_child = child
            temp = delete
            delete = None
            child.parent = parent
            self.delete_height_fix(root)
            return temp

    def delete(self, key):
        """ Remove the Node object containing the key if the key exists in
            the BST and return the removed node, else return None.
           
            The returned node is the actual Node object that got removed
            from the BST, and so might be successor of the removed key. """
        root = self.root
        delete = self.search(key)
        if (delete == None or root == None):
            return None

        # Handles case if node to delete has no children
        if (not delete.right_child and not delete.left_child):
            temp = self.delete_no_kids(delete, root)
            return temp

        # Handles case if node to delete only has a right child
        elif (delete.right_child and not delete.left_child):
            temp = self.delete_right_kid(delete, root)
            return temp

        # Handles case if node to delete only has a left child
        elif (not delete.right_child and delete.left_child):
            temp = self.delete_left_kid(delete, root)
            return temp

        # Handles case if node to delete has two children
        elif (self.two_kids(delete)):
            right_tree = delete.right_child
            successor = self.search_min(right_tree)
            temp = successor
            delete.key = successor.key
            delete.value = successor.value
            if (not successor.right_child):
                temp = self.delete_no_kids(successor, root)
            elif (successor.right_child):
                temp = self.delete_right_kid(successor, root)
            return temp
        return None
    
    def in_order_traversal(self):
        """ Return a list of the Nodes in the tree in sorted order. """
        if (self.root == None):
            return []
        temp = self.root
        return self.in_order(temp, [])

    def in_order(self, root, node_list):
        """ This is a helper function to call in_order recursively. """
        if (root != None):
            self.in_order(root.left_child, node_list)
            node_list.append(root)
            self.in_order(root.right_child, node_list)
        return node_list
    
    def breadth_first_traversal(self):
        """ Return a list of lists, where each inner lists contains the elements
            of one layer in the tree. Layers are filled in breadth-first-order,
            and contain contain all elements linked in the BST, including the
            None elements.
            >> BST([5, 8]).breadth_first_traversal()
            [[Node(5)], [None, Node(8)], [None, None]] """
        if (self.root == None):
            return []
        output = []
        parents = [self.root]
        output.append(parents)

        # Loop to put parents in one list and its children in one list
        while (parents):
            children = []
            for node in parents:
                if (node != None):
                    if (node.left_child):
                        children.append(node.left_child)
                    elif (not node.left_child):
                        children.append(None)
                    if (node.right_child):
                        children.append(node.right_child)
                    elif (not node.right_child):
                        children.append(None)
            output.append(children)
            parents = children
        return output
        

    def __str__(self):
        """ Return a string containing the elements of the tree in breadth-first
            order, with each on a new line, and None elements as `_`, and
            finally a single line containing all the nodes in sorted order.
            >> print(BST([5, 8, 3]))
            5
            3 8
            _ _ _ _
            3 5 8 """
        output_list = self.breadth_first_traversal()
        output = ''

        # Convert the output of breadth_first_traversal to a string
        for lists in output_list:
            for element in lists:
                if (element == None):
                    element = "_"
                output += str(element)
                output += " "
            output += '\n'
        output = output[:-1]
        in_order_list = self.in_order_traversal()
        in_order_string = ''

        # Convert the output of in_order_traversal to a string
        for element in in_order_list:
            in_order_string += str(element)
            in_order_string += " "
        output += in_order_string
        return output
    



