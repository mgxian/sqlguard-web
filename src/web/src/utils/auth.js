import Cookies from 'js-cookie'

const TokenKey = 'Access-Token'
const UserIDKey = 'User-ID'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function getUserID() {
  return Cookies.get(UserIDKey)
}

export function setUserID(id) {
  return Cookies.set(UserIDKey, id)
}

export function removeUserID() {
  return Cookies.remove(UserIDKey)
}
