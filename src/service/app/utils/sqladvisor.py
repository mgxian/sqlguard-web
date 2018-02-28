# coding:utf8


from subprocess import Popen, PIPE
import logging

def getResult(sql):
    host = '192.168.12.211'
    port = 3306
    database = 'will'
    user = 'root'
    password = 'will'

    cmd_prefix = "/usr/local/bin/sqladvisor -h {}  -P {}  -u {} -p '{}' -d {} -v 2 -q \"".format(
        host, port, user, password, database)
    sql = sql.replace('"', '\\"')
    sql = sql.replace('`', '\\`')
    cmd = cmd_prefix + sql + '"'
    
    #logging.warning(cmd)
    res = Popen(cmd, stderr=PIPE, shell=True).stderr.read()

    return res
