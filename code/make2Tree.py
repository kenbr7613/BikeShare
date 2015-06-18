



class make2Tree():

    def __init__(self, br, args):
	if(br):
	    self.isLeaf = True
	    self.initLeaf(args)
	else:
	    self.isLeaf = False
	    self.initBranch(args)


    def initBranch(self,args):
	self.val = args[0] 
	self.feature = args[1] 

    def initLeaf(self, args):
	self.val = args[0]
	self.feature = None

    def insertLeft(self, node):
	self.left = node

    def insertRightt(self, node):
	self.right = node

    def getLeft(self):
	return self.left

    def getRight(self):
	return self.right

    def getVal(self):
	return self.val

    def getFeature(self):
	return self.feature

    def isLeaf(self):
	return self.isLeaf
   
