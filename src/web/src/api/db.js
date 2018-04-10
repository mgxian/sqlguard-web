import request from '@/utils/request'

export function getEnvs() {
  return request({
    url: '/envs',
    method: 'get'
  })
}

export function getMySQLs() {
  return request({
    url: '/mysqls',
    method: 'get'
  })
}

export function createMysql(mysql) {
  return request({
    url: '/mysqls',
    method: 'post',
    data: {
      host: mysql.host,
      port: mysql.port,
      username: mysql.username,
      password: mysql.password,
      database: mysql.database,
      env_id: mysql.env_id
    }
  })
}

export function updateMysql(mysql) {
  return request({
    url: '/mysql/' + mysql.id.toString(),
    method: 'put',
    data: {
      host: mysql.host,
      port: mysql.port,
      username: mysql.username,
      password: mysql.password,
      database: mysql.database,
      env_id: mysql.env_id
    }
  })
}

export function deleteMysql(id) {
  return request({
    url: '/mysql/' + id.toString(),
    method: 'delete'
  })
}
