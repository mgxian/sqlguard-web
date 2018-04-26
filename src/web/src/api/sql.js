import request from '@/utils/request'

export function getMySqls(type) {
  return request({
    url: '/user/sqls',
    method: 'get',
    params: {
      type
    }
  })
}

export function getNeedReviewSqls(status) {
  return request({
    url: '/sqls',
    method: 'get',
    params: {
      status
    }
  })
}

export function checkSql(mysql_id, sql_id) {
  return request({
    url: '/mysql/' + mysql_id.toString() + '/sql/' + sql_id.toString() + '/check',
    method: 'post'
  })
}

export function executeSql(mysql_id, sql_id) {
  return request({
    url: '/mysql/' + mysql_id.toString() + '/sql/' + sql_id.toString() + '/execute',
    method: 'post'
  })
}

export function createSql(sql) {
  return request({
    url: '/mysql/' + sql.mysql_id.toString() + '/sqls',
    method: 'post',
    data: {
      sql: sql.sql,
      type: sql.type,
      reviewer_id: sql.reviewer_id
    }
  })
}
