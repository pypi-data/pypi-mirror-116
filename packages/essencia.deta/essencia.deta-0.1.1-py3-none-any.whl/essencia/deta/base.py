#!/usr/bin/env python
# coding: utf-8

import contextlib
from deta import Deta
from typing import Tuple, Dict, Any, Union


class DetaProject:
    def __init__(self, project, key):
        self.project = project
        self.key = key
        self.secret = self.project + '_' + self.key

    def sync_connect(self, table: str):
        return Deta(self.secret).Base(table)

    async def connect(self, table: str):
        return Deta(self.secret).Base(table)


    @contextlib.asynccontextmanager
    async def Count(self, table):
        db = await self.connect(table)
        count = 0
        try:
            count = len(next(db.fetch({})))
        except:
            pass
        finally:
            yield count
            db.client.close()


    @contextlib.asynccontextmanager
    async def Update(self, table, data):
        key = data.get("key")
        if not key:
            raise AttributeError("a key is necessary")
        db = await self.connect(table)
        try:
            yield db.update(data, key)
        except:
            yield
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def ListAll(self, table):
        print(f'looking all for table {table}')
        db = await self.connect(table)
        try:
            data = next(db.fetch({}))
            print(data)
            yield data
        except:
            yield
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def CheckCode(self, table, code):
        db = await self.connect(table)
        result = None
        try:
            result = next(db.fetch({'meta.code': code}))[0]
        except:
            pass
        finally:
            yield result
            db.client.close()


    @contextlib.asynccontextmanager
    async def Insert(self, table, data):
        key = data.get("key")
        if not key:
            raise AttributeError("a key is necessary")
        db = await self.connect(table)
        try:
            yield db.insert(data)
        except:
            yield
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def Delete(self, table, key):
        db = await self.connect(table)
        try:
            yield db.delete(key=key)
        except:
            yield
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def Put(self, table, data):
        db = await self.connect(table)
        try:
            yield db.put(data)
        except:
            yield
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def Get(self, table, key):
        db = await self.connect(table)
        data = None
        try:
            data = db.get(key=key)
        except:
            pass
        finally:
            yield data
            db.client.close()


    @contextlib.asynccontextmanager
    async def SearchName(self, table, name):
        db = await self.connect(table)
        try:
            yield next(db.fetch({'fullname?contains': name}))
        except:
            yield []
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def Search(self, table, query={}):
        db = await self.connect(table)
        try:
            yield next(db.fetch(query))
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def First(self, table, query={}):
        db = await self.connect(table)
        try:
            yield next(db.fetch(query))[0]
        except BaseException as e:
            yield
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def Last(self, table, query={}):
        db = await self.connect(table)
        try:
            yield next(db.fetch(query))[-1]
        except BaseException as e:
            raise ValueError(e)
        finally:
            db.client.close()


    @contextlib.asynccontextmanager
    async def GetOrCreate(self, table: str, data: Dict[ str, Any ]) -> Tuple[Union[Dict[str, Any]], Union[Dict[str, Any]]]:
        '''
        This function need the code kwarg to perform search in database before saving.
        :param table:
        :param data:
        :return:
        '''
        code = data.get('code', None)
        assert code != None, 'CODE could not be found'
        exist, created = None, None
        base = await self.connect(table)
        try:
            exist = next(base.fetch({'code': code}))[0]
        except:
            created = base.put(data)
        finally:
            yield exist, created
            base.client.close()







