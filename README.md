# 24秋知识图谱系统演示

## 环境布置
docker 部署 neo4j
```bash
docker run -it -p7687:7687 -p7474:7474 --rm neo4j:latest
```

然后你在本电脑的7474端口可以看到neo4j的http web ui

neo4j 用户名: neofj , 密码: knmap2024

## 将数据导入系统

分别有机场,火车站,城市的数据,它们放在data目录,结构如下:

```bash
$ tree data
data
├── Airport
│   ├── EntityInfo.json # 注意,文件名和内容格式是固定的
│   └── EntityRel.json
├── City
│   ├── EntityInfo.json
│   └── EntityRel.json
└── TrainStation
    ├── EntityInfo.json
    └── EntityRel.json
```

使用add脚本添加数据到数据库:
```
python .\add.py .\data\city\ # 注意,这个执行时间很长(45min)
python .\add.py .\data\Airport\
python .\add.py .\data\TrainStation\
```

要是不想自己执行一遍,用我导完的docker镜像.

## 导出 neo4j 镜像

```
docker export knmap2024 -o knmap2024.tar
```

## 导入 镜像
```
docker import knmap2024.tar neo4j:latest
```

