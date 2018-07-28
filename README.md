![apm](https://img.shields.io/apm/l/vim-mode.svg?style=plastic)
#### 介绍
`jsonDB2`是一个基于内存的键值对数据库(非关系型数据库)

#### 安装
```bash
$ pip install jdb2
```
或者
```bash
$ git clone https://github.com/spdir/jsonDB2.git
$ cd jsonDB2
$ python setup.py install
```

#### 使用

1. 初始化实例
```python
import jdb2
#初始化一个空的DB
n = jdb2.NoSql()
#将原来的数据导入到数据库,并配置自动持久化
n = jdb2.NoSql(dump=True, nosqlFile='filePath', dumpTime=10)
  # dump: 启动持久化,并导入已有数据, 默认: False
  # nosqlFile: 持久化文件路径
  # dumpTime: 持久化时间间隔(单位: 秒), 默认: 30
#创建一个数据库, 如果数据库存在此库，则返回存在库的对象
d1 = n.createDB('d1')
```
2. 操作使用
```python
>>> import jdb2
>>> n = jdb2.NoSql()   #初始化实例对象
>>> d1 = n.createDB('d1') #创建一个DB
>>> t1 = d1.createTable('t1') #创建一张表
>>> d1.setValue('a','b')  #db设置一个参数
>>> d1.getValue('a')  #db获取一个参数
'b'
>>> t1.setValue(1,2)  #tb设置一个参数
>>> t1.getValue(1)  #tb获取一个参数
2
>>> d1.getValues()  #获取所有的value
[{1: 2}, 'b']
>>> d1.getKeys()  #获取所有的key
['t1', 'a']
>>> d1.getItems() #获取所有的键值对, 返回list
[('t1', {1: 2}), ('a', 'b')]
>>> d1.dropKey('a') #删除一个键或者一张表
>>> d1.setValue('c','d')
>>> d1.clearKey('c')  #清除一个key的内容
>>> d1.getItems()
[('t1', {1: 2}), ('c', None)]
>>> d1.clearKey('t1') #清除一张表的内容
>>> d1.getItems()
[('t1', {}), ('c', None)]
>>> t1.lenTable() #获取数据库或表长度
1
>>> d1.allData()  #获取所有的表或库的所有键值对，返回dict
{'t1': {}, 'c': None}
```



