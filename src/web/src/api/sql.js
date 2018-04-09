import request from '@/utils/request'

export function getSqls() {
  return request({
    url: '/user/sqls',
    method: 'get'
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
