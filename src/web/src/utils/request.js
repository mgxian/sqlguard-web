import axios from 'axios'
import { Message } from 'element-ui'
import store from '../store'
// import { getToken } from '@/utils/auth'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.BASE_API, // api的base_url
  timeout: 2000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(config => {
  const token = store.getters.token
  if (token) {
    config.headers['Authorization'] = 'Bearer ' + token // 让每个请求携带自定义token 请根据实际情况自行修改
  }
  return config
}, error => {
  // Do something with request error
  console.log(error) // for debug
  Promise.reject(error)
})

// respone拦截器
service.interceptors.response.use(
  response => {
    /**
    * status_code为非2xx是抛错 可结合自己业务进行修改
    */
    const res = response.data
    const status_code = response.status
    if (status_code >= 300) {
      Message({
        message: res.msg,
        type: 'error',
        duration: 3 * 1000
      })
      return Promise.reject('error')
    } else {
      return response.data
    }
  },
  error => {
    console.log('axios interceptors get error ----> ' + error)// for debug
    const errorResp = error.response.data
    const errorCode = error.response.status
    console.log('axios interceptors error code ----> ', errorCode)
    let errMsg = ''
    if (errorResp.msg) {
      errMsg = errorResp.msg
    } else {
      errMsg = errorResp.description
    }
    Message({
      message: errMsg,
      type: 'error',
      duration: 3 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
