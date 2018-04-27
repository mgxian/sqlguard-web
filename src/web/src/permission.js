import router from './router'
import store from './store'
import NProgress from 'nprogress' // Progress 进度条
import 'nprogress/nprogress.css'// Progress 进度条样式
import { Message } from 'element-ui'
import { getToken } from '@/utils/auth' // 验权

const whiteList = ['/login', '/forget_password', '/reset_password'] // 不重定向白名单
router.beforeEach((to, from, next) => {
  NProgress.start()
  let token = store.getters.token
  if (!token) {
    token = getToken()
  }
  if (token) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      // console.log(store.getters.role)
      if (store.getters.role.id === undefined) {
        store.dispatch('GetInfo').then(res => { // 拉取用户信息
          next()
        }).catch(() => {
          store.dispatch('FedLogOut').then(() => {
            Message.error('验证失败,请重新登录')
            next({ path: '/login' })
          })
        })
      } else {
        next()
      }
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next('/login')
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  NProgress.done() // 结束Progress
})
