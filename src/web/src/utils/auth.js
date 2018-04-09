import Cookies from 'js-cookie'

const TokenKey = 'Access-Token'
const UserIDKey = 'User-ID'
const ExpiresMin = 120

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  const expiresTime = new Date(new Date().getTime() + ExpiresMin * 60 * 1000)
  return Cookies.set(TokenKey, token, { expires: expiresTime })
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function getUserID() {
  return Cookies.get(UserIDKey)
}

export function setUserID(id) {
  const expiresTime = new Date(new Date().getTime() + ExpiresMin * 60 * 1000)
  return Cookies.set(UserIDKey, id, { expires: expiresTime })
}

export function removeUserID() {
  return Cookies.remove(UserIDKey)
}
