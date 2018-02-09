##20180130 & 20180131

__author__ = 'WuYan'

import aiohttp,logging
import aiomysql

def log(sql,args=()):
	logging.info('SQL: %s' % sql)

#创建连接池，连接池由__pool存储，编码设置为utf-8
async def create_pool(loop,**kw):
	logging.info('create database connection pool...')

	global __pool
	__pool = await aiomysql.create_pool(
		host = kw.get('host','localhost'),
		port = kw.get('port',3306),
		user = kw['user'],
		password = kw['password'],
		db = kw['db'],
		charset = kw.get('charset','utf8'),
		autocommit = kw.get('autocommit',True),
		maxsize = kw.get('maxsize',10),
		minsize = kw.get('minsize',1),
		loop = loop
		)

#执行select语句，传入参数sql语句和SQL参数
async def select(sql,args,size=None):
	log(sql,args)

	global __pool
	async with __pool.get() as conn:
		async with conn.cursor(aiomysql.DictCursor) as cur:
			#SQL语句的占位符是?，而MySQL的占位符是%s，select()函数在内部自动替换。注意要始终坚持使用带参数的SQL，而不是自己拼接SQL字符串，这样可以防止SQL注入攻击。
			await cur.execute(sql.replace('?','%s'),args or ())
			#如果传入size参数，就通过fetchmany()获取最多指定数量的记录，否则，通过fetchall()获取所有记录。
			if size:
				rs = await cur.fetchmany(size)
			else:
				rs = await cur.fetchall()
		logging.info('rows returned:%s' % len(rs))
		return rs

#execute函数返回值：被影响的行数
async def execute(sql,args,autocommit=True):
	log(mysql)

	async with __pool.get() as conn:
		if not autocommit:
			await conn.begin()
		try:
			async with conn.cursor(aiomysql.DictCursor) as cur:
				await cur.execute(sql.replace('?','%s'),args)
				affected = cur.rowcount
			if not autocommit:
				await conn.commit()
		except BaseException as e:
			if not autocommit:
				await conn.rollback()
			raise
		return affected

def create_args_string(num):
	L = []
	for n in range(num):
		L.append('?')
	return ','.join(L)

##设计 ORM框架####

class Field(object):
	def __init__(self, name,column_type,primary_key,default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default

	def __str__(self):
		return '<%s,%s,%s>' % (self.__class__.__name__,self.column_type,self.name)


##以下几个函数定义了 几种常见的数据类型 String、bool、int、float等
class StringField(Field):
	def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100)'):
		super().__init__(name,ddl,primary_key,default)

class BooleanField(Field):
	def __init__(self,name=None,default=False):
		super().__init__(name,'boolean',False,default)

class IntergetField(Field):
	def __init__(self, name=None,primary_key=False,default=0):
		super().__init__(name,'bright',primary_key,default)

class FloatField(Field):
	def __init__(self, name=None,primary_key=False,default=0.0):
		super().__init__(name,'real',primary_key,default)

class TextField(Field):
	def __init__(self, name=None,default=None):
		super().__init__(name,'text',False,default)

class ModelMetaclass(type):
	def __new__(cls,name,bases,attrs):
		#排除Model类本身
		if name =='Model':
			return type.__new__(cls,name,bases,attrs)
		#获取table名称
		tableName = attrs.get('__table__',None) or name
		logging.info('found model: %s (table:%s)' % (name,tableName))
		mappings = dict()
		fields = []
		primaryKey = None
		for k,v in attrs.items():
			if isinstance(v,Field):
				logging.info(' found mapping:%s ==> %s' %(k,v))
				mappings[k] = v
				if v.primary_key:
					#找到主键
					if primaryKey:
						raise StandardError('Duplicate primary key for field:%s' % k)
					primaryKey = k
				else:
					fields.append(k)
		if not primaryKey:
			raise StandardError('Primary key not found.')
		for k in mappings.keys():
			attrs.pop(k)
		escaped_fields = list(map(lambda f: '`%s`' % f,fields))
		attrs['__mappings__'] = mappings # 保存属性和列的映射关系
		attrs['__table__'] = tableName
		attrs['__primary_key__'] = primaryKey  # 主键属性名
		attrs['__fields__'] = fields # 除主键外的属性名
		attrs['__select__'] = 'select `%s`,%s from `%s` '% (primaryKey,','.join(escaped_fields),tableName)
		attrs['__insert__'] = 'insert into `%s` (%s,%s) value (%s)' % (tableName,','.join(escaped_fields),primaryKey,create_args_string(len(escaped_fields) + 1))
		attrs['__update__'] = 'update `%s` set %s where `%s` = ?' % (tableName,','.join(map(lambda f:'`%s`=?' % (mappings.get(f).name or f),fields)),primaryKey)
		attrs['__delete__'] = 'delte from `%s` where `%s` =?' % (tableName,primaryKey)
		return type.__new__(cls,name,bases,attrs)

class Model(dict,metaclass=ModelMetaclass):
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self,key,value):
		self[key] = value

	def getValue(self,key):
		return getattr(self,key,None)

	def getValueOrDefault(self,key):
		value = getattr(self,key,None)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.debug('using default value for %s: %s' % (key,str(value)))
				setattr(self,key,value)
		return value

	@classmethod
	async def findAll(cls,where=None,args=None,**kw): #findAll() 根据where条件查找；
		' find objects by where clause. '
		sql = [cls.__select__]
		if where:
			sql.append('where')
			sql.append(where)
		if args is None:
			args = []

		orderBy = kw.get('orderBy',None)
		if orderBy:
			sql.append('order by')
			sql.append(orderBy)

		limit = kw.get('limit',None)
		if limit is not None:
			sql.append('limit')
			if isinstance(limit,int):
				sql.append('?')
				args.append(limit)
			elif isinstance(limit,tuple) and len(limit) == 2:
				sql.append('?,?')
				args.extend(limit)
			else:
				raise ValueError('Invalid limit value: %s' % str(limit))

		rs = await select(''.join(sql),args)
		return [cls(**r) for r in rs]

	@classmethod
	async def findNumber(cls,selectField,where=None,args=None):
		#根据where条件查找，但返回的是整数，适用于select count(*)类型的SQL
		' find number by select and where. '
		sql = ['select %s _num_ from `%s`' % (selectField ,cls.__table__)]
		if where:
			sql.append('where')
			sql.append(where)
		rs = await select(' '.join(sql),args,1)
		if len(rs) == 0:
			return None
		return rs[0]['_num_']

	@classmethod
	async def find(cls,pk):
		' find object by primary key. '
		rs = await select('%s where `%s`=?' % (cls.__select__,cls.__primary_key__),[pk],1)
		if len(rs) == 0:
			return None
		return cls(**rs[0])

	async def save(self):
		args = list(map(self.getValueOrDefault,self.__fields__))
		args.append(self.getValueOrDefault(self.__primary_key__))
		rows = await execute(self.__insert__,args)
		if row != 1:
			logging.warn('failed to insert record:affected rows: %s ' % rows)

	async def update(self):
		args = list(map(self.getValue,self.__fields__))
		args.append(self.getValue(self.__primary_key__))
		rows = await execute(self.__update__,args)
		if row != 1:
			logging.warn('failed to update by primary key:affected rows: %s' % rows)

	async def remove(self):
		args = [self.getValue(self.__primary_key__)]
		rows = await execute(self.__delete__,args)
		if rows != 1:
			logging.warn('failed to remove by primary key:affected rows: %s' % rows)








		

						





		
		
		
		
		
