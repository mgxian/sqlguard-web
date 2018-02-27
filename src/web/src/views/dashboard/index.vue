<template>
  <div>
    <el-container :class="{'collapse': sidebarCollapse}">
      <el-aside width="200px">
        <el-menu class="sidebar" @open="handleOpen" @close="handleClose" text-color="#bfcbd9">
          <el-submenu index="1" class="submenu">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span slot="title">导航一</span>
            </template>
            <el-menu-item-group>
              <span slot="title">分组一</span>
              <el-menu-item index="1-1">选项1</el-menu-item>
              <el-menu-item index="1-2">选项2</el-menu-item>
            </el-menu-item-group>
            <el-submenu index="1-4">
              <span slot="title">选项4</span>
              <el-menu-item index="1-4-1">选项1</el-menu-item>
            </el-submenu>
          </el-submenu>
          <el-menu-item index="2">
            <i class="el-icon-menu"></i>
            <span slot="title">导航二</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container class="right-wrap">
        <el-header>
          <el-menu class="nav" mode="horizontal">
            <div class="hamburger-container" @click="sidebarCollapse = !sidebarCollapse">
              <i class="icon el-icon-my-hamburger-bold"></i>
            </div>
            <div class="breadcrumb-container">
              <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
                <el-breadcrumb-item>table</el-breadcrumb-item>
              </el-breadcrumb>
            </div>

            <el-dropdown trigger="click" class="avatar-container">
              <div class="avatar-wrapper">
                <img src="//img1.famulei.com/zhubo/393180/picture/15/7/10/2015071015242348601_100x100.png" class="user-avatar">
                <i class="el-icon-caret-bottom"></i>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>首页</el-dropdown-item>
                <el-dropdown-item>设置</el-dropdown-item>
                <el-dropdown-item>管理员页面</el-dropdown-item>
                <el-dropdown-item>登出</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

          </el-menu>
        </el-header>
        <el-main>
          <p v-for="i in 100" :key="i.id">xx</p>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sidebarCollapse: false
    }
  }
}
</script>

<style lang="stylus">
animateTime = 0.5s
// 头部导航
.el-header
  padding 0 0
// 侧边样导航初始样式
.el-aside
  position fixed
  overflow auto
  width 200px
  bottom 0
  top 0
  left 0
  background-color #324157
  color #333
  line-height 200px
  transition-duration animateTime
  .el-menu
    border none
    background-color transparent
    &.sidebar
      color #bfcbd9
    .el-submenu
      .el-submenu__title
        transition animateTime
        .el-submenu__icon-arrow
          margin-right 15px
          font-size 15px
        &:hover
          background-color #48576a
      .el-menu
        transition animateTime
        .el-menu-item-group
          .el-menu-item
            &:hover
              background-color #48576a
    >.el-menu-item
      transition animateTime
      &:hover
        background-color #48576a
      &.is-active
        background-color transparent
    .el-submenu
      &.is-opened
        .el-menu
          background-color #1d2633
.nav
  background-color #eef1f6
  height 50px
  align-items center
  display -webkit-flex
.right-wrap
  position absolute
  right 0
  left 183px
  background-color white
  transition-duration animateTime
  .breadcrumb-container
    margin-left 8px
.el-main
  line-height 160px
.hamburger-container
  height 50px
  padding 0 10px
  align-items center
  display -webkit-flex
  .icon
    transform rotate(90deg)
    transition-duration animateTime
.el-icon-my-hamburger-bold
  font-size 25px
// 点击折叠之后的样式
.el-container
  &.collapse
    .el-aside
      >.el-menu
        >.el-submenu
          >.el-submenu__title
            padding-left 8px !important
            transition animateTime
          >.el-menu
            padding-left 25px
            transition animateTime
        >.el-menu-item
          padding-left 8px !important
          transition animateTime
    .right-wrap
      left 41px
      z-index 10
    .hamburger-container
      .icon
        transform rotate(180deg)
.avatar-container
  height 50px
  position absolute
  display inline-block
  right 35px
  .avatar-wrapper
    position relative
    height 40px
    margin-top 5px
    .user-avatar
      height 40px
      width 40px
      border-radius 10px
</style>
