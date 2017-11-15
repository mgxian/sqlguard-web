import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/views/login'
import Nav from '@/views/layout/Navbar'
import Side from '@/views/layout/Sidebar'
import Dash from '@/views/layout/Layout'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/nav',
      name: 'nav',
      component: Nav
    },
    {
      path: '/side',
      name: 'side',
      component: Side
    },
    {
      path: '/dashboard',
      name: 'dash',
      component: Dash
    }
  ]
})
