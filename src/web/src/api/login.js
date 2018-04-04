import request from '@/utils/request'

export function login(username, password) {
  return request({
    url: '/oauth2/token',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

export function getInfo(token) {
  return request({
    url: '/user',
    method: 'get'
  })
}

export function logout() {
  return new Promise((resolve, reject) => {
    resolve()
  })
}
