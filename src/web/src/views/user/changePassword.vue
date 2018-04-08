<template>
  <div class="change-password">
    <h3>修改密码</h3>
    <el-form class="form" label-position="left" label-width="80px">
      <el-form-item label="旧密码">
        <el-input class="password-input" type="password" v-model="old_password" placeholder="请输入旧密码" clearable></el-input>
      </el-form-item>
      <el-form-item label="新密码">
        <el-input class="password-input" type="password" v-model="new_password" placeholder="请输入新密码" clearable></el-input>
      </el-form-item>
      <el-form-item label="确认密码">
        <el-input class="password-input" type="password" v-model="verify_password" placeholder="请输入确认密码" clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onChangePassword" :disabled="isButtonDisabled">修改密码</el-button>
        <el-button type="info" @click="clearPasswordInput">清空输入</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { changePassword } from '@/api/user'
export default {
  data() {
    return {
      old_password: '',
      new_password: '',
      verify_password: ''
    }
  },
  methods: {
    onChangePassword() {
      if (this.new_password === this.verify_password) {
        changePassword(this.user_id, this.old_password, this.new_password).then(
          response => {
            this.$message.success('密码修改成功')
          }
        )
      } else {
        this.$message.error('两次输入的密码不一致')
        return
      }
    },
    clearPasswordInput() {
      this.old_password = ''
      this.new_password = ''
      this.verify_password = ''
    }
  },
  computed: {
    ...mapGetters(['user_id']),
    isButtonDisabled() {
      if (
        this.old_password.length === 0 ||
        this.new_password.length === 0 ||
        this.verify_password.length === 0
      ) {
        return true
      }

      return false
    }
  }
}
</script>

<style lang="stylus" scoped>
.change-password
  margin-left 200px
  margin-top 50px

  .form
    .password-input
      width 300px
</style>

