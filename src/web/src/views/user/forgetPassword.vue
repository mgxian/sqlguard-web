<template>
  <div class="forget-password-container">
    <div class="forget-password">
      <h3>重置密码</h3>
      <el-form class="form" label-position="left" label-width="80px">
        <el-form-item label="用户名">
          <el-input class="username-input" v-model="username" placeholder="请输入用户名" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSendResetPasswordMail" :disabled="isButtonDisabled">重置密码</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { sendResetPasswordMail } from '@/api/user'
export default {
  data() {
    return {
      username: ''
    }
  },
  methods: {
    onSendResetPasswordMail() {
      sendResetPasswordMail(this.username).then(response => {
        this.$message.success('重置密码链接已发送到注册邮箱')
      })
    }
  },
  computed: {
    isButtonDisabled() {
      if (this.username.length === 0) {
        return true
      }

      return false
    }
  }
}
</script>

<style lang="stylus" scoped>
.forget-password-container
  display flex
  justify-content center
  .forget-password
    margin-top 150px

    .form
      .username-input
        width 300px
</style>

