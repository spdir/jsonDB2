# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2018 Musker.Chao

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json, threading, time


class NosqlFileNotDefineError():
  """
  if Nosql File not define and
  use DB.loadDB() or DB.dumpDB() function
  raise NosqlFileNotDefineError
  """
  pass


class _ObjLock(object):
  """Process lock Class

  Process lock to prevent dirty data

  """

  def __init__(self):
    import threading
    self.Lock = threading.RLock()

  def lock(self):
    return self.Lock.acquire()

  def ulock(self):
    return self.Lock.release()


class BaseJson:
  """dict base function

  Defining processing dictionary data secondary encapsulation method

  """

  def __init__(self, obj):
    """
    init BaseJons class
    :param obj: dict object
    """
    self.obj = obj
    self.objLock = _ObjLock()

  def setValue(self, key, value):
    """
    set an key: value
    :param key: key
    :param value: value
    :return: None
    """
    self.objLock.lock()
    self.obj[key] = value
    self.objLock.ulock()

  def getValue(self, key):
    """
    get an  value
    :param key: key
    :return: value
    """
    return self.obj.get(key)

  def dropKey(self, key):
    """
    delete an key
    :param key: key
    :return: None
    """
    self.objLock.lock()
    try:
      self.obj.pop(key)
    except KeyError:
      pass
    self.objLock.ulock()

  def getKeys(self):
    """
    get all keys
    :return: keys list []
    """
    keys_list = []
    keys = self.obj.keys()
    for k in keys:
      keys_list.append(k)
    return keys_list

  def getValues(self):
    """
    get all values
    :return: values list []
    """
    values_list = []
    values = self.obj.values()
    for v in values:
      values_list.append(v)
    return values_list

  def getItems(self):
    """
    get all key:value
    :return: tuple in list [(key,value)]
    """
    items_list = []
    for k, v in self.obj.items():
      items_list.append((k, v))
    return items_list

  def clearKey(self, key):
    """
    clear key body
    :param key: key
    :return: None
    """
    self.objLock.lock()
    val_obj = self.obj[key]
    if isinstance(val_obj, dict):
      self.obj[key] = {}
    elif isinstance(val_obj, list):
      self.obj[key] = []
    elif isinstance(val_obj, tuple):
      self.obj[key] = ()
    elif isinstance(val_obj, set):
      self.obj[key] = set()
    else:
      self.obj[key] = None
    self.objLock.ulock()

  def lenTable(self):
    """
    get now table length
    :return: None
    """
    return len(self.obj)

  def allData(self):
    """
    get now table data
    :return: dict {}
    """
    return self.obj

  def createTable(self, tname):
    """
    create table
    :param subtname:  table name
    :return: BaseJson class object
    """
    table = BaseJson({})
    if self.obj.get(tname):
      table = BaseJson(self.obj[tname])
    else:
      self.obj[tname] = table.allData()
    return table


class DB:
  """
  jdb2 load and dump class
  """

  def __init__(self, dump=False, nosqlFile=None, dumpTime=30):
    """
    init DB object
    :param dump: whether to persist data
    :param nosqlFile: persistent data file path
    :param dumpTime: persistence interval
    """
    self.db = {}
    self.dump = dump
    self.nosqlFile = nosqlFile
    self.dumpTime = dumpTime

  def loadDB(self):
    """
    Load persistent data file data
    :return: None
    """
    if (self.dump and self.nosqlFile != None):
      with open(self.nosqlFile, 'r', encoding='utf-8') as  f:
        self.db = json.loads(str(f.read()))
    else:
      raise NosqlFileNotDefineError

  def dumpDB(self):
    """
    persistence data
    :return: None
    """
    tmp_db = {}
    for k, v in self.db.items():
      if isinstance(v, BaseJson):
        tmp_db[k] = v.allData()
      else:
        tmp_db[k] = v
    if (self.dump and self.nosqlFile != None):
      with open(self.nosqlFile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(tmp_db))
    else:
      raise NosqlFileNotDefineError

  def timingump(self):
    """
    start a new thread to persist data
    :return: None
    """
    while True:
      time.sleep(int(self.dumpTime))
      self.dumpDB()

  def initDB(self):
    """
    init jdb2 object
    Load nosqlFile data and generate db object if nosqlFile has data,
    Create an empty db object if nosqlFile has no data
    :return: JsonDB object
    """
    if self.dump:
      with open(self.nosqlFile, 'r', encoding='utf-8') as f:
        if len(f.read()) > 0:
          self.loadDB()
      t = threading.Thread(target=self.timingump)
      t.start()
    return self.db


class NoSql:
  """
  jdb2 main Class
  """

  def __init__(self, dump=False, nosqlFile=None, dumpTime=30):
    """
    get DB object param and init db obj
    :param dump: whether to persist data
    :param nosqlFile: persistent data file path
    :param dumpTime: persistence interval
    """
    self.dump = dump
    self.nosqlFile = nosqlFile
    self.dumpTime = dumpTime
    self.db = DB(self.dump, self.nosqlFile, self.dumpTime).initDB()

  def createDB(self, dbname):
    """
    create an database
    :param dbname: database name
    :return:
    """
    one_db = BaseJson({})
    if self.db.get(dbname):
      one_db = BaseJson(self.db[dbname])
    else:
      self.db[dbname] = one_db
    return one_db
