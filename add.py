"""
将json数据解析并加入数据库
"""

import json
from pathlib import Path
from Neo4j.Neo4j import Neo4j

def read_into_json(filename):
    with open(filename,encoding="utf-8") as f:
        return json.load(f)

def add(dirname: str):
    entity_filename = Path(dirname) / "EntityInfo.json" 
    relation_filename = Path(dirname) / "EntityRel.json" 
    entities = read_into_json(entity_filename)
    relations = read_into_json(relation_filename)
    db = Neo4j(ip='localhost',password="knmap2024")
    db.add_graph(entity_info=entities,entity_rel=relations)

if __name__ == "__main__":
    from sys import argv
    print(argv)
    if len(argv) <= 1:
        print(f"usage: {argv[0]} <要导入的目录名>")
        exit()
    add(argv[1])
