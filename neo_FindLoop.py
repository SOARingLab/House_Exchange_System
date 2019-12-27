# 找出有向图中所有的环路
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher, walk

# DFS + Backtracking
def searchCycle(node):
	# 如果当前节点已经在路径中，说明找到一条回路，返回
	if node['name'] in trace:
		idx = trace.index(node['name'])
		global findCycle
		findCycle = True
		ans.append(trace[idx:])
		return

	# 将当前结点加入路径
	trace.append(node['name'])
	# 查找以当前结点为起点的所有relations
	relations = Rmatcher.match([node])
	# 遍历查找到的relations，保存所有的终点结点
	endnodes = []
	for relation in relations:
		for currnode in walk(relation):
			if type(currnode) is Node and currnode != node:
				endnodes.append(currnode)
	# 递归查找
	for nextnode in endnodes:
		searchCycle(nextnode)
	# Backtracking
	trace.pop() 

# 搜索路径
trace = []
# 已搜索到的环路
ans = []
# flag
findCycle = False

graph = Graph("http://127.0.0.1:7474", username="neo4j", password="wsnxdyj")
Rmatcher = RelationshipMatcher(graph)
Nmatcher = NodeMatcher(graph)

# 从任意结点开始查找
node = list(Nmatcher.match('Person', name = 'Jack'))[0]

searchCycle(node)
print(ans)
if findCycle:
	print('Found Cycle!!!')
else:
	print('No Cycle!!!')