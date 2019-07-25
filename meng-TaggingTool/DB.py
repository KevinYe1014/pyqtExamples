import sqlite3
import os



TaggingToolInfoDB = 'TaggingToolInfo.db'
TaggingDetailTable = 'TaggingDetail'
TaggingIndexTable = 'TaggingIndex'

# region 数据库操作
def get_conn(path):
    '''创建数据库连接对象'''
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        print('硬盘上面：[{}]'.format(path))
        return conn
    else:
        conn = None
        print('内存上面：[:memory:]')
        return sqlite3.connect(':memory:')

def get_cursor(conn):
    '''创建游标对象'''
    if conn is not None:
        return conn.cursor()
    else:
        return get_conn('').cursor()

def closs_all(conn, cu):
    '''关闭数据库连接和游标对象'''
    try:
        if cu is not None:
            cu.close()
    finally:
        if conn is not None:
            conn.close()

def close_cursor(cu):
    '''关闭游标对象'''
    if cu is not None:
        cu.close()

def close_conn(conn):
    '''关闭数据库连接对象'''
    if conn is not None:
        conn.close()

def drop_table(conn, table):
    '''删除表'''
    if table is not None and table !='':
        sql = 'DROP TABLE IF EXISTS ' + table
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        print('删除数据库表[{}]成功!'.format(table))
        # closs_all(conn, cu)
        close_cursor(cu)
    else:
        print('the [{}] is empty or equal None'.format(table))


def create_table(conn, sql):
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        print('创建数据库表成功!')
        # closs_all(conn, cu)
        close_cursor(cu)
    else:
        print('the [{}] is empty or equal None'.format(sql))

def insert(conn, sql, data):
    """插入数据"""
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            for d in data:
                cu.execute(sql, d)
                conn.commit()
            # closs_all(conn, cu)
            close_cursor(cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def fetchall(conn, sql):
    """查询所有数据"""
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        cu.execute(sql)
        r = cu.fetchall()
        # if len(r) > 0:
        #     for e in range(len(r)):
        #         print(r[e])
        close_cursor(cu)
        return r
    else:
        print('the [{}] is empty or equal None!'.format(sql))


def fetchone(conn, sql, data):
    """查询一条数据"""
    if sql is not None and sql != '':
        if data is not None:
            # Do this instead
            d = (data,)
            cu = get_cursor(conn)
            cu.execute(sql, d)
            r = cu.fetchall()
            # if len(r) > 0:
            #     for e in range(len(r)):
            #         print(r[e])
            close_cursor(cu)
            return r
        else:
            print('the [{}] equal None!'.format(data))
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def update(conn, sql, data):
    """更新数据"""
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            for d in data:
                cu.execute(sql, d)
                conn.commit()
            # closs_all(conn, cu)
            close_cursor(cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def delete(conn, sql, data):
    """删除数据"""
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            for d in data:
                cu.execute(sql, d)
                conn.commit()
            # closs_all(conn, cu)
            close_cursor(cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))


def CreateTaggingDetailTable(conn):
    '''创建TaggingDetailTable表'''
    create_table_sql = '''CREATE TABLE 'TaggingDetail'(
    'id' SMALLINT NOT NULL ,
    'directory' VARCHAR(150) DEFAULT NULL ,
    'oldfilename' VARCHAR(100) DEFAULT  NULL ,
    'newfilename' VARCHAR(100) DEFAULT  NULL ,
    'classification' SMALLINT DEFAULT NULL,
    PRIMARY KEY ('id')
    )'''
    # conn = get_conn(TaggingToolInfoDB)
    create_table(conn, create_table_sql)

def CreateTaggingIndexTable(conn):
    '''创建TaggingIndex表'''
    create_table_sql = '''CREATE TABLE 'TaggingIndex'(
    'id' SMALLINT NOT NULL ,
    'index' SMALLINT NOT NULL ,
    PRIMARY KEY ('id')
    )'''
    # conn = get_conn(TaggingToolInfoDB)
    create_table(conn, create_table_sql)

def InsertTaggingDetailTable(conn):
    '''向TaggingDetail插入数据'''
    insert_sql = '''INSERT INTO TaggingDetail VALUES (?, ?, ?, ?, ?)'''
    data = [(1, r'c:/users/yelei/desktop/a', 'a.jpg', 'a1,jpg', 1),
            (2, r'c:/users/yelei/desktop/a', 'b.jpg', 'b1,jpg', 2),
            (3, r'c:/users/yelei/desktop/a', 'c.jpg', 'c1,jpg', 3)]
    # conn = get_conn(TaggingToolInfoDB)
    insert(conn, insert_sql, data)

def InsertTaggingIndexTable(conn):
    '''向TaggingDetail插入数据'''
    insert_sql = '''INSERT INTO TaggingIndex VALUES (?, ?)'''
    data = [(1, 1),
            (2, 2),
            (3, 3)]
    # conn = get_conn(TaggingToolInfoDB)
    insert(conn, insert_sql, data)


# endregion


if __name__ == '__main__':
    # 测试
    conn = get_conn(TaggingToolInfoDB)
    # 删除表 创建表
    # detail表
    drop_table(conn, TaggingDetailTable)
    try:
        fetchall_sql_minid = '''SELECT * FROM TaggingDetail '''
        conn = get_conn(TaggingToolInfoDB)
        r = fetchall(conn, fetchall_sql_minid)
    except:
        CreateTaggingDetailTable(conn)




    fetchall_sql_minid = '''SELECT * FROM TaggingDetail '''
    conn = get_conn(TaggingToolInfoDB)
    r = fetchall(conn, fetchall_sql_minid)
    print(len(r))

    InsertTaggingDetailTable(conn)
    # index表
    # conn = get_conn(TaggingToolInfoDB)
    drop_table(conn, TaggingIndexTable)
    CreateTaggingIndexTable(conn)
    InsertTaggingIndexTable(conn)

    # 查询所有数据
    fetchall_sql = '''SELECT * FROM TaggingDetail'''
    conn = get_conn(TaggingToolInfoDB)
    fetchall(conn, fetchall_sql)

    # 删除
    delete_sql = '''DELETE FROM TaggingDetail WHERE  id = ?'''
    data = [(1, )]
    # conn = get_conn(TaggingToolInfoDB)
    delete(conn, delete_sql, data)

    # min(id)
    fetchall_sql_minid = '''SELECT min(id) FROM TaggingDetail '''
    conn = get_conn(TaggingToolInfoDB)
    r = fetchall(conn, fetchall_sql_minid)
    print(r[0][0])

    # 查询单条数据
    fetchone_sql = '''SELECT * FROM TaggingDetail WHERE id = ?'''
    data = 1
    # conn = get_conn(TaggingToolInfoDB)
    fetchone(conn, fetchone_sql, data)
    # 更新数据
    update_sql = '''UPDATE TaggingDetail SET newfilename = ?  WHERE id = ?'''
    data = [('a11.jpg', 1),
            ('b11.jpg', 2)]
    # conn = get_conn(TaggingToolInfoDB)
    update(conn, update_sql, data)

    fetchall_sql = '''SELECT * FROM TaggingDetail'''
    # conn = get_conn(TaggingToolInfoDB)
    fetchall(conn, fetchall_sql)

    # 删除
    delete_sql = '''DELETE FROM TaggingDetail WHERE  oldfilename = ? AND id = ?'''
    data = [('a.jpg', 1)]
    # conn = get_conn(TaggingToolInfoDB)
    delete(conn, delete_sql, data)

    fetchall_sql = '''SELECT * FROM TaggingDetail'''
    # conn = get_conn(TaggingToolInfoDB)
    fetchall(conn, fetchall_sql)

    # 查询index表
    fetchall_sql = '''SELECT * FROM TaggingIndex'''
    # conn = get_conn(TaggingToolInfoDB)
    fetchall(conn, fetchall_sql)
    close_conn(conn)

