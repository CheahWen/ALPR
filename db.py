import sys, traceback
import csv
import asyncio
import aiomysql
from datetime import date, datetime

from ConfigParserManager import ConfigParserManager
from LogManager import LogManager
from CSVManager import CSVManager

server, user, password, port, db = ConfigParserManager.getDBConfig()

# Connect to server
class DB:
    def __init__(self, server=server, port=port, user=user, password=password, db=db):
        print("----------SQL DB Configuration Start----------")
        self.server=server
        self.user=user
        self.password=password
        self.port=port
        self.db=db
        LogManager.makeLog(message="Server: {}".format(self.server), type=0)
        LogManager.makeLog(message="Port: {}".format(self.port), type=0)
        LogManager.makeLog(message="User: {}".format(self.user), type=0)
        LogManager.makeLog(message="Password: {}".format(self.password), type=0)
        LogManager.makeLog(message="DB: {}".format(self.db), type=0)

        print("----------SQL DB Configuration Done----------")

        self.loop = asyncio.get_event_loop()
            
    async def createPool(self):
        self.pool = await aiomysql.create_pool(
            autocommit=True,
            host=self.server,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            loop=self.loop,
        )
    @asyncio.coroutine
    async def selectOne(self, sql):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql)
                    r = await cur.fetchone()
                    return r
        except aiomysql.MySQLError as e:
            LogManager.makeLog(message='Got error {!r}, errno is {}'.format(e, e.args[0]), type=1)
            LogManager.makeLog(message=f'{traceback.format_exc()}', type=1)

    async def selectAll(self, sql):
        
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql)
                    r = await cur.fetchall()
                    return r
        except aiomysql.MySQLError as e:
            LogManager.makeLog(message='Got error {!r}, errno is {}'.format(e, e.args[0]), type=1)
            LogManager.makeLog(message=f'{traceback.format_exc()}', type=1)

    async def insertOne(self, sql):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql)

        except aiomysql.MySQLError as e:
            LogManager.makeLog(message='Got error {!r}, errno is {}'.format(e, e.args[0]), type=1)
            LogManager.makeLog(message=f'{traceback.format_exc()}', type=1)

    
    async def makeTrx(self, sql):
        
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    r = await cur.execute(sql)
                

        except aiomysql.MySQLError as e:
            LogManager.makeLog(message='Got error {!r}, errno is {}'.format(e, e.args[0]), type=1)
            LogManager.makeLog(message=f'{traceback.format_exc()}', type=1)
    
    def close_pool(self):
        self.pool.close()