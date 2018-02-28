# coding:utf8

import MySQLdb as mysql


def get_result(sql):
    inception_host = '192.168.12.211'
    inception_port = 5506

    host = '192.168.12.211'
    port = 3306
    user = 'root'
    password = 'will'
    database = 'will'

    inception_prefix = '/*--user={};--password={};--host={};--check=1;--port={};*/\
inception_magic_start;\
use {};'.format(user, password, host, port, database)

    if not sql.endswith(';'):
        sql = sql + ';'

    inception_suffix = 'inception_magic_commit;'

    full_inception_sql = inception_prefix + sql + inception_suffix
    try:
        conn = mysql.connect(host=inception_host, user='',
                             passwd='', db='', port=inception_port)
        cur = conn.cursor()
        ret = cur.execute(full_inception_sql)
        result = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        print(field_names)
        res = ""
        for row in result:
            res += row[5] + "|" + row[4] + "|" + row[8] + "\n"
        cur.close()
        conn.close()
        return full_inception_sql + "\n" + res
    except mysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        return "error"
