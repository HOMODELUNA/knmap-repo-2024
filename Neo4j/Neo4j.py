# coding=utf-8

# 引入外部库
from py2neo import *
from tqdm import tqdm
from typing import TypedDict
from itertools import batched, islice

class Entity(TypedDict):
	type: str
	property: dict[str,str]


# 引入内部库


class Neo4j:
	def __init__ (self, ip: str, password: str, user='neo4j', http_port=7474, bolt_port=7687):
		# Neo4j数据库连接
		self.graph = Graph("bolt://localhost:7687", password=password, user=user)
		self.node_matcher = NodeMatcher(self.graph)

	def crate_graph (self, entity_info: list[Entity], entity_rel: list) -> None:
		"""
		根据所传入的实体信息链表和实体关系三元组链表，构建子图，并存储到Neo4j
		注意：不考虑图谱中已经存在的相同实体
		:param entity_info: element: {type: str, property: dict}
		:param entity_rel: element: (n1_index, {name: str, property: dict}, n2_index)
		:return: None
		"""
		nodes = {}
		index = 0

		print('开始创建实体节点！')
		for info in tqdm(entity_info):
			assert isinstance(info["type"],str)
			assert isinstance(info["property"],dict)
			node = Node(info['type'], name=info['property']['name'])
			node.update(info['property'])
			nodes[index] = node
			self.graph.create(node)
			index += 1

		print('开始创建实体间关系！')
		for rel in tqdm(entity_rel):
			assert isinstance(rel[0],int)
			assert isinstance(rel[1],dict)
			relation = Relationship(nodes[rel[0]], rel[1]['name'], nodes[rel[2]])
			relation.update(rel[1]['property'])
			self.graph.create(relation)

	def add_graph (self, entity_info: list, entity_rel: list) -> None:
		"""
		根据所传入的实体信息链表和实体关系三元组链表，
		在已有实体的基础上，增加新的实体，及实体间关系。
		注意：关系三元组中，实体类型为字符串的实体，在图数据库中可能存在
		:param entity_info: element: {type: str, property: dict}
		:param entity_rel: element: (n1_index/n1_str, {name: str, property: dict}, n2_index/n2_str)
		:return: None
		"""
		nodes = {}
		index = 0

		CHUNK_SIZE = 1024

		print('开始创建新的实体节点！')
		for chunk in tqdm(list(batched(entity_info, CHUNK_SIZE))):
			#print("\n",chunk)
			trans =  self.graph.begin()
			for info in chunk:
				assert isinstance(info["type"],str)
				assert isinstance(info["property"],dict)
				node = Node(info['type'], name=info['property']['name'])
				node.update(info['property'])
				nodes[index] = node
				trans.create(node)
				index += 1
			trans.commit()
		

		print('开始创建已有实体和新实体间关系！')
		if len(entity_rel)> 10000:
			for chunk in tqdm(list(batched(entity_rel, CHUNK_SIZE))):
				trans =  self.graph.begin()
				for rel in chunk:
					# 判断实体1类型
					if isinstance(rel[0], str):
						node1 = self.node_matcher.match(name=rel[0]).first()
					else:
						node1 = nodes[rel[0]]

					# 判断实体2类型
					if isinstance(rel[2], str):
						node2 = self.node_matcher.match(name=rel[2]).first()
					else:
						node2 = nodes[rel[2]]

					# 创建实体关系对象
					if node1 is not None and node2 is not None:
						relation = Relationship(node1, rel[1]['name'], node2)
						relation.update(rel[1]['property'])
						trans.create(relation)
				trans.commit()
		else:
			for rel in tqdm(entity_rel):
				# 判断实体1类型
				if isinstance(rel[0], str):
					node1 = self.node_matcher.match(name=rel[0]).first()
				else:
					node1 = nodes[rel[0]]

				# 判断实体2类型
				if isinstance(rel[2], str):
					node2 = self.node_matcher.match(name=rel[2]).first()
				else:
					node2 = nodes[rel[2]]

				# 创建实体关系对象
				if node1 is not None and node2 is not None:
					relation = Relationship(node1, rel[1]['name'], node2)
					relation.update(rel[1]['property'])
					self.graph.create(relation)
		
	def add_graph_rel_only(self,entity_rel: list) -> None:
		CHUNK_SIZE = 1024
		print('开始创建已有实体和新实体间关系！')
		for chunk in tqdm(islice(entity_rel, CHUNK_SIZE)):
			trans =  self.graph.begin()
			for rel in chunk:
				# 判断实体1类型
				if isinstance(rel[0], str):
					node1 = self.node_matcher.match(name=rel[0]).first()
				else:
					node1 = nodes[rel[0]]

				# 判断实体2类型
				if isinstance(rel[2], str):
					node2 = self.node_matcher.match(name=rel[2]).first()
				else:
					node2 = nodes[rel[2]]

				# 创建实体关系对象
				if node1 is not None and node2 is not None:
					relation = Relationship(node1, rel[1]['name'], node2)
					relation.update(rel[1]['property'])
					trans.create(relation)
			trans.commit()
	def update_graph (self):
		pass
