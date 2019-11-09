# pg2mysql

数据同步工具

## 用途

用全量方式, 将指定表从一个数据库抽取到另外一个数据

## 支持的数据库

`sqlalchemy`支持的数据库都支持

### 上游支持的数据库

[X] `Postgresql`

[X] `MySQL`

[X] `Oracle`

[X] `SQLite`

[X] `Hive` 通过 [`PyHive`](https://github.com/dropbox/PyHive#sqlalchemy)

### 下游支持的数据库


[X] `Postgresql`

[X] `MySQL`

## p.s.

pg 链接URL

```python
# psycopg2
engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')
```

MySQL链接URL

```python
# mysql-connector
engine = create_engine("mysql+mysqlconnector://user:pswd@host:port/db")
```
