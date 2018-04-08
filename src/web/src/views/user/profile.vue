<template>
  <div class="profile-contanier" v-loading.body="loading" element-loading-text="拼命加载中" :data="user">
    <div class="profile">
      <h3>基本资料</h3>
      <el-form class="form" label-position="left" label-width="80px">
        <el-form-item label="用户名">
          {{user.username}}
        </el-form-item>
        <el-form-item label="昵称">
          <el-input class="name-input" v-model="user.name" placeholder="请输入昵称" clearable></el-input>
          <el-button class="name-button" :disabled="user.name.length===0" type="primary" @click="changeName">修改</el-button>
        </el-form-item>
        <el-form-item label="邮箱">
          {{user.email}}
        </el-form-item>
        <el-form-item label="角色" v-if="user.roles">
          <el-tag v-if="filter.value === user.roles[0]" v-for="filter in filters" :key="filter.value" :type="filter.type" close-transition>{{filter.text}}</el-tag>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { getInfo } from '@/api/login'
import { modifyUserName } from '@/api/user'
import { mapGetters } from 'vuex'
export default {
  data() {
    return {
      user: Object,
      loading: true,
      filters: [
        { text: '管理员', value: 'Administrator', type: 'primary' },
        { text: '经理', value: 'Manager', type: 'success' },
        { text: '开发人员', value: 'User', type: 'info' }
      ]
    }
  },
  created() {
    this.fetchProfile()
  },
  computed: {
    ...mapGetters(['user_id'])
  },
  methods: {
    fetchProfile() {
      this.loading = true
      getInfo().then(response => {
        this.user = response
        this.loading = false
      })
    },
    changeName() {
      console.log(this.user_id, this.user.id)
      this.loading = true
      modifyUserName(this.user.id, this.user.name).then(response => {
        this.user = response
        this.loading = false
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.profile-contanier
  .profile
    margin-left 200px
    .form
      .name-input
        width 200px
</style>

