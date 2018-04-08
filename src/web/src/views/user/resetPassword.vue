<template>
  <div class="reset-password-container">
    <div class="reset-password">
      <h3>重置密码</h3>
      <el-form class="form" label-position="left" label-width="80px">
        <el-form-item label="新密码">
          <el-input class="password-input" type="password" v-model="new_password" placeholder="请输入新密码" clearable></el-input>
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input class="password-input" type="password" v-model="verify_password" placeholder="请输入确认密码" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onResetPassword" :disabled="isButtonDisabled">重置密码</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { resetPassword } from '@/api/user'
export default {
  data() {
    return {
      new_password: '',
      verify_password: '',
      username: '',
      token: ''
    }
  },
  methods: {
    onResetPassword() {
      if (this.new_password === this.verify_password) {
        console.log(this.username, this.token, this.new_password)
        resetPassword(this.username, this.token, this.new_password).then(
          response => {
            this.$message.success('密码修改成功')
          }
        )
      } else {
        this.$message.error('两次输入的密码不一致')
        return
      }
    },
    getParameters() {
      this.username = this.$route.query.username
      this.token = this.$route.query.token
    }
  },
  mounted() {
    this.getParameters()
  },
  computed: {
    isButtonDisabled() {
      if (this.new_password.length === 0 || this.verify_password.length === 0) {
        return true
      }

      return false
    }
  }
}
</script>

<style lang="stylus" scoped>
.reset-password-container
  display flex
  justify-content center

  .reset-password
    margin-top 150px

    .form
      .password-input
        width 300px
</style>

