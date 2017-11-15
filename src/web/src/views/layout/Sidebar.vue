<template>
  <div>
    <el-menu class="sidebar" @open="handleOpen" @close="handleClose" text-color="#bfcbd9" :collapse="isCollapse">
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
  </div>
</template>

<style lang="stylus">
.sidebar
  width 180px
  min-height 400px
  background-color #324157
  position absolute
  left 0
  right 0
  top 0
  bottom 0

.el-menu 
  .el-submenu
    padding-left 0
    position relative

    &.is-opened
      .el-menu
        background-color #1d2633

    .el-submenu__title
      &:hover
        background-color #48576a
</style>


<script>
export default {
  data() {
    return {
      isCollapse: false
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>