import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
**/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'Dashboard',
    hidden: true,
    children: [{
      path: 'dashboard',
      component: () => import('@/views/dashboard/index')
    }]
  },

  {
    path: '/admin',
    component: Layout,
    redirect: '/admin/user',
    name: 'Admin',
    meta: { title: '用户管理', icon: 'example' },
    children: [
      {
        path: 'user',
        name: 'AdminUser',
        component: () => import('@/views/user/index'),
        meta: { title: '用户', icon: 'user' }
      },
      {
        path: 'role',
        name: 'Role',
        component: () => import('@/views/user/role'),
        meta: { title: '角色', icon: 'user' }
      }
    ]
  },

  {
    path: '/user',
    component: Layout,
    hidden: true,
    name: 'User',
    meta: { title: '用户', icon: 'user' },
    children: [
      {
        path: 'profile',
        name: '用户资料',
        component: () => import('@/views/user/profile'),
        meta: { title: '用户资料', icon: 'user' }
      },
      {
        path: 'change_password',
        name: '修改密码',
        component: () => import('@/views/user/changePassword'),
        meta: { title: '修改密码', icon: 'user' }
      }
    ]
  },

  {
    path: '/db',
    component: Layout,
    name: 'Db',
    redirect: '/db/env',
    meta: { title: '数据库管理', icon: 'tree' },
    children: [
      {
        path: 'env',
        name: '环境',
        component: () => import('@/views/db/env'),
        meta: { title: '环境', icon: 'tree' }
      },
      {
        path: 'mysql',
        name: '数据库',
        component: () => import('@/views/db/mysql'),
        meta: { title: '数据库', icon: 'tree' }
      }
    ]
  },
  {
    path: '/sql-optimize',
    component: Layout,
    name: 'Sql-optimize',
    redirect: '/sql-optimize/history',
    // meta: { title: 'SQL优化', icon: 'tree' },
    children: [
      {
        path: 'history',
        name: 'history',
        component: () => import('@/views/sql/optimizeHistory'),
        meta: { title: 'SQL优化', icon: 'tree' }
      }
    ]
  },
  {
    path: '/sql-review',
    component: Layout,
    name: 'Sql-review',
    redirect: '/sql-review/index',
    meta: { title: 'SQL执行', icon: 'tree' },
    children: [
      {
        path: 'index',
        name: '我的申请',
        component: () => import('@/views/sql/index'),
        meta: { title: '我的申请', icon: 'tree' }
      },
      {
        path: 'review',
        name: '待审核',
        component: () => import('@/views/sql/needReviewSql'),
        meta: { title: '待审核', icon: 'tree' }
      },
      {
        path: 'history',
        name: '审核历史',
        component: () => import('@/views/sql/reviewHistory'),
        meta: { title: '审核历史', icon: 'tree' }
      }
    ]
  },
  {
    path: '/forget_password',
    name: 'ForgetPassword',
    component: () => import('@/views/user/forgetPassword'),
    meta: { title: '忘记密码', icon: 'user' }
  },
  {
    path: '/reset_password',
    name: 'ResetPassword',
    component: () => import('@/views/user/resetPassword'),
    meta: { title: '重置密码', icon: 'user' }
  },

  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

