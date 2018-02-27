import axios from 'axios'
// import { Message, MessageBox } from 'element-ui'

// 创建axios实例
const service = axios.create({
  baseURL: '/api/', // api的base_url
  timeout: 15000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(config => {
  const token = '123456789'
  config.headers['Authorization'] = 'Bearer ' + token // 让每个请求携带自定义token 请根据实际情况自行修改
  return config
}, error => {
  // Do something with request error
  console.log(error) // for debug
  Promise.reject(error)
})

// respone拦截器
service.interceptors.response.use(
  // 1xx 2xx 3xx 响应码的响应处理逻辑
  response => {
    return response
  },

  // 4xx 5xx 响应码的响应处理逻辑
  error => {
    console.log('err' + error)// for debug
    console.log(error.response)
    // Message({
    //     message: error.message,
    //     type: 'error',
    //     duration: 5 * 1000
    // })
    return Promise.reject(error)
    // return error
  }
)

export default service
