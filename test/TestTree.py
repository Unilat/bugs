'''
Created on Sep 8, 2011

@author: calvin
'''

if __name__ == '__main__':
    
    from Tree import Tree
    tree = Tree(1)
    
    tree.add(0, Tree(2))
    tree.add(1, Tree(3))
    tree.add(2, Tree(4))
    
    child1 = tree.child_at(0)
    child1.add(0, Tree(5))
    
    print str(tree)
    print len(tree)
    
    tree.remove(1)
    
    print str(tree)
    print len(tree)
    