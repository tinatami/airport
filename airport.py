""" Tina Tami

    This file implements the Airport class with all its
    necessary functions. It takes as input the airplanes
    with their flying time. The programme then checks whether
    the inserted time does not form any conflict. If a
    conflict exists, depending on if the simple flag is True,
    the programme finds the next available spot. Finally,
    the airplane is inserted in the BST. 
"""

import argparse

from bst import BST

class Airport(BST):
    def __init__(self, wait_time=300000, simple=False):
        """ Creates a new Airport instance and sets its basic attributes. """
        BST.__init__(self)
        self.wait_time = wait_time
        self.simple = simple
    
    def find_conflict(self, time):
        """ Return the first node in the tree that conflicts with the specified
            time and wait_time attribute set for the Airport.
           
            Returns None if no such conflict is found. """
        node = self.root
        while (node != None):
            if (time-self.wait_time < node.key < time+self.wait_time):
                return node
            elif (time > node.key):
                node = node.right_child
            elif (time < node.key):
                node = node.left_child
        return None
    
    def bounded_insert(self, time, tailnumber):
        """ Inserts a airplane with a time and tailnumber into the schedule.
            If the difference between the proposed time and an existing node
            in schedule is less then the wait_time, the airplane cannot be
            scheduled at that time.
           
            If the simple flag is set to True, conflict are not inserted
            and otherwise the program will try to insert in the next
            possible timeslot.

            Returns the node if successfully inserted and None otherwise. """
        conflict = self.find_conflict(time)
        if (conflict == None):
            return self.insert(time, tailnumber)
        else:
            if (self.simple != True):
                self.bounded_insert(conflict.key + self.wait_time, tailnumber)
        return None


    def __str__(self):
        """ Return the airplanes in the schedule in sorted order. """
        output = self.in_order_traversal()
        output_string = ''
        for element in output:
            output_string += str(element.key)
            output_string += '/'
            output_string += str(element.value)
            output_string += " "
        output_string = output_string[:-1]
        return output_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sort a list of elements.')
    parser.add_argument('elements', nargs='+',
                        help='The elements of a list')
    parser.add_argument("-t", "--timestep", type=int,
                        help="set the minimum timestep (default=300000)", default=300000)
    parser.add_argument("-s", "--simple", action="store_true",
                        help="either become simple or not")
    args = parser.parse_args()

    cs_airport = Airport(args.timestep, args.simple)
    for elem in args.elements:
        try:
            s = elem.split('/')
            time, tail = int(s[0]), s[1]
            cs_airport.bounded_insert(time, tail)
        except (ValueError, IndexError):
            print("Invalid airplane format: "+elem)
    
    print(cs_airport)

