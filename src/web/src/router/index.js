import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/views/login'
import Nav from '@/views/layout/Navbar'
import Side from '@/views/layout/Sidebar'
import Layout from '@/views/layout/Layout'
import Dash from '@/views/dashboard'

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
      path: '/layout',
      name: 'layout',
      component: Layout
    },
    {
      path: '/dashboard',
      name: 'dash',
      component: Dash
    }
  ]
})
