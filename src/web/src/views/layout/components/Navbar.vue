<template>
  <el-menu class="navbar" mode="horizontal">
    <hamburger class="hamburger-container" :toggleClick="toggleSideBar" :isActive="sidebar.opened"></hamburger>
    <breadcrumb></breadcrumb>
    <el-dropdown class="avatar-container" trigger="click">
      <div class="avatar-wrapper">
        <img class="user-avatar" :src="avatar+'?imageView2/1/w/80/h/80'">
        <i class="el-icon-caret-bottom"></i>
      </div>
      <el-dropdown-menu class="user-dropdown" slot="dropdown">
        <router-link class="inlineBlock" to="/">
          <el-dropdown-item>
            首页
          </el-dropdown-item>
        </router-link>
        <router-link class="inlineBlock" to="/user/profile">
          <el-dropdown-item>
            用户信息
          </el-dropdown-item>
        </router-link>
        <router-link class="inlineBlock" to="/user/change_password">
          <el-dropdown-item>
            修改密码
          </el-dropdown-item>
        </router-link>
        <router-link class="inlineBlock" to="/forget_password">
          <el-dropdown-item>
            忘记密码
          </el-dropdown-item>
        </router-link>
        <router-link class="inlineBlock" to="/reset_password">
          <el-dropdown-item>
            重置密码
          </el-dropdown-item>
        </router-link>
        <el-dropdown-item divided>
          <span @click="logout" style="display:block;">退出登录</span>
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </el-menu>
</template>

<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'

export default {
  components: {
    Breadcrumb,
    Hamburger
  },
  computed: {
    ...mapGetters(['sidebar', 'avatar'])
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('ToggleSideBar')
    },
    logout() {
      this.$store.dispatch('LogOut').then(() => {
        location.reload() // 为了重新实例化vue-router对象 避免bug
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.navbar
  height 50px
  line-height 50px
  border-radius 0px !important

  .hamburger-container
    line-height 58px
    height 50px
    float left
    padding 0 10px

  .screenfull
    position absolute
    right 90px
    top 16px
    color red

  .avatar-container
    height 50px
    display inline-block
    position absolute
    right 35px

    .avatar-wrapper
      cursor pointer
      margin-top 5px
      position relative

      .user-avatar
        width 40px
        height 40px
        border-radius 10px

      .el-icon-caret-bottom
        position absolute
        right -20px
        top 25px
        font-size 12px
</style>

