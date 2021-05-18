class Node:
    def __init__(depth,data):
        self.data = data
        self.depth = depth
        self.child = []

root = Node(0,[0 for _ in range(12)])

def Tree(root):
    for i in range(100):
        
