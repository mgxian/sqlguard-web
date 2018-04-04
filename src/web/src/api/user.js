import request from '@/utils/request'

export function getUser(id) {
  return request({
    url: '/user/' + id.toString(),
    method: 'get'
  })
}

export function getUsers() {
  return request({
    url: '/users',
    method: 'get'
  })
}

export function createUser(username, name, email, password) {
  return request({
    url: '/users',
    method: 'post',
    data: {
      username,
      name,
      email,
      password
    }
  })
}

export function modifyUserName(id, name) {
  return request({
    url: '/user/' + id.toString(),
    method: 'put',
    data: {
      name
    }
  })
}

export function changePassword(id, password_old, password_new) {
  return request({
    url: '/user/' + id.toString() + '/change_password',
    method: 'post',
    data: {
      password_old,
      password_new
    }
  })
}

export function sendResetPasswordMail(username) {
  return request({
    url: '/user/' + username.toString() + '/reset_password',
    method: 'get'
  })
}

export function resetPassword(username, token, password) {
  return request({
    url: '/user/' + username.toString() + '/reset_password',
    method: 'post',
    data: {
      token,
      password
    }
  })
}

export function getRoles() {
  return request({
    url: '/roles',
    method: 'get'
  })
}
