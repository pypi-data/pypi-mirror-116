__version__ = '0.0.1'

class DB:
  def __createFile__():
    from os import path
    
    if path.exists("db.json") == False:
      with open('db.json', 'w') as db:
        pass
    else: 
      pass

  def all():
    import json
    DB.__createFile__()
    rDB = open('db.json', 'r')
    read = rDB.read()
    if read == '':
      rDB.close()
      wDB = open('db.json', 'w')
      finalData = json.dumps({"mData": []})
      wDB.write(finalData)
      wDB.close()
      rDB = open('db.json', 'r')
      read = rDB.read()
      rDB.close()
      return json.loads(read)
    else:
      rDB.close()
      return json.loads(read)
      
  
  def get(key):
    from termcolor import colored

    currentDB = DB.all()
    arr = currentDB['mData']
    for x in range(len(arr)):
      if arr[x]['key'] == key:
        return arr[x]['data']
    return print(colored(f'Error: \"{key}\" not found in database.', 'red'))

  def set(key, data):
    import json

    currentDB = DB.all()
    initData = {'key': key, 'data': data}
    arr = currentDB['mData']
    wDB = open('db.json', 'w')
    for x in range(len(arr)):
      if arr[x]['key'] == key:
       arr[x] = {"key": key, "data": data}
       finalData = json.dumps({"mData": arr})
       wDB.write(finalData)
       wDB.close()
       return data
    arr.append(initData)
    finalData = json.dumps({"mData": arr})
    wDB.write(finalData)
    wDB.close()
    return data

  def delete(key):
    import json
    from termcolor import colored

    if key == 'all':
      wDB = open('db.json', 'w')
      finalData = json.dumps({"mData": []})
      wDB.write(finalData)
    else:
      currentDB = DB.all()
      arr = currentDB['mData']
      wDB = open('db.json', 'w')
      for x in range(len(arr)):
        if arr[x]['key'] == key:
          del arr[x]
          finalData = json.dumps({"mData": arr})
          wDB.write(finalData)
          wDB.close()
          return
      finalData = json.dumps({"mData": arr})
      wDB.write(finalData)
      wDB.close()
      print(colored(f'Error: \"{key}\" not found in database.', 'red'))
      return
  
  def add(key, data):
    import json
    from termcolor import colored
    
    currentDB = DB.all()
    arr = currentDB['mData']
    for x in range(len(arr)):
      if arr[x]['key'] == key:
        if type(data) is int or type(data) is float:
          arr[x]['data'] += data;
          finalData = json.dumps({"mData": arr})
          wDB = open('db.json', 'w')
          wDB.write(finalData)
          wDB.close()
          return arr[x]['data'];
        else:
          varType = type(data)
          return print(colored(f'Error: expected type - \'int\' or \'float\', got {varType}.', 'red'))
  
  def subtract(key, data):
    import json
    from termcolor import colored
    currentDB = DB.all()
    arr = currentDB['mData']
    for x in range(len(arr)):
      if arr[x]['key'] == key:
        if type(data) is int or type(data) is float:
          arr[x]['data'] -= data
          finalData = json.dumps({"mData": arr})
          wDB = open('db.json', 'w')
          wDB.write(finalData)
          wDB.close()
          return arr[x]['data']
        else:
          varType = type(data)
          return print(colored(f'Error: expected type - \'int\' or \'float\', got {varType}.', 'red'))