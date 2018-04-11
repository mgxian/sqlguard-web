import { login, logout, getInfo } from '@/api/login'
import { getToken, setToken, removeToken, getUserID, setUserID, removeUserID } from '@/utils/auth'

const user = {
  state: {
    token: getToken(),
    user_id: getUserID(),
    username: '',
    name: '',
    avatar: '',
    role: {}
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_USER_ID: (state, id) => {
      state.user_id = id
    },
    SET_USERNAME: (state, username) => {
      state.username = username
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLE: (state, role) => {
      state.role = role
    }
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      const username = userInfo.username.trim()
      return new Promise((resolve, reject) => {
        login(username, userInfo.password).then(response => {
          const data = response
          if (userInfo.rememberMe) {
            setToken(data.access_token)
          }
          commit('SET_TOKEN', data.access_token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo({ commit, state }) {
      // console.log('----->get user info')
      return new Promise((resolve, reject) => {
        getInfo(state.token).then(response => {
          const data = response
          setUserID(data.id)
          commit('SET_ROLE', data.role)
          commit('SET_USER_ID', data.id)
          commit('SET_NAME', data.name)
          commit('SET_USERNAME', data.username)
          commit('SET_AVATAR', data.avatar)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit, state }) {
      return new Promise((resolve, reject) => {
        logout(state.token).then(() => {
          commit('SET_TOKEN', '')
          commit('SET_USER_ID', 0)
          commit('SET_ROLE', {})
          removeToken()
          removeUserID()
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 前端 登出
    FedLogOut({ commit }) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        commit('SET_USER_ID', 0)
        removeToken()
        removeUserID()
        resolve()
      })
    }
  }
}

export default user
