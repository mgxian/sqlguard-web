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
