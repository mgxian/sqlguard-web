<style lang="stylus">
.login-tabs
  .el-tabs__nav
    width 100%
    .el-tabs__item
      width 50%
      text-align center
      padding 0
    .el-tabs__active-bar
      width 50% !important
.login-page
  text-align center
  padding-top 10%
  position absolute
  left 0
  right 0
  top 0
  bottom 0
  background-color #2d3a4b
  .el-tabs__item
    color #fff
.el-switch__label
  color #fff
.login-title
  color #eee
</style>

<template>
  <div class="login-page">
    <h3 class="login-title">SQL检测系统</h3>
    <el-row type="flex" justify="center">
      <el-col :span="4">
        <div>

          <el-tabs v-model="activeName" class="login-tabs">
            <el-tab-pane label="登录" name="first">
              <el-form :model="login" :rules="userRules" ref="login">
                <el-form-item prop="name">
                  <el-input v-model="login.name" prefix-icon="el-icon-my-user"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                  <el-input v-model="login.password" type="password" prefix-icon="el-icon-my-password"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-row type="flex" justify="end">
                    <el-col :span="6.5">
                      <el-switch v-model="login.rememberme" active-text="7天内免登录" inactive-text=""></el-switch>
                    </el-col>
                  </el-row>
                </el-form-item>
                <el-form-item>
                  <el-row type="flex" justify="space-around">
                    <el-col :span="0.5">
                      <el-button type="primary" @click="onSubmit('login')">登录</el-button>
                    </el-col>
                  </el-row>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="注册" name="second">
              <el-form ref="register" :model="register" :rules="userRules">
                <el-form-item prop="name">
                  <el-input v-model="register.name" prefix-icon="el-icon-my-user"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                  <el-input v-model="register.password" prefix-icon="el-icon-my-password"></el-input>
                </el-form-item>
                <el-form-item prop="password2">
                  <el-input v-model="register.password2" prefix-icon="el-icon-my-confirmpassword"></el-input>
                </el-form-item>
                <el-form-item prop="email">
                  <el-input v-model="register.email" prefix-icon="el-icon-my-email"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-row type="flex" justify="space-around">
                    <el-col :span="0.5">
                      <el-button type="primary" @click="onSubmit('register')">注册</el-button>
                    </el-col>
                  </el-row>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { isUsernameCanRegister } from '@/utils/validate'
export default {
  data() {
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.register.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }

    const validateUsername = (rule, value, callback) => {
      isUsernameCanRegister(value, callback)
    }

    return {
      login: {
        name: '',
        password: '',
        rememberme: false
      },
      userRules: {
        name: [
          {
            required: true,
            message: '请输入用户名',
            trigger: 'blur'
          },
          {
            min: 3,
            max: 20,
            message: '长度在 3 到 20 个字符',
            trigger: 'blur'
          },
          {
            validator: validateUsername,
            trigger: 'blur'
          }
        ],
        password: [
          {
            required: true,
            message: '请输入密码',
            trigger: 'blur'
          },
          {
            min: 6,
            max: 20,
            message: '长度在 6 到 20 个字符',
            trigger: 'blur'
          }
        ],
        password2: [
          {
            validator: validatePass2,
            trigger: 'blur'
          }
        ],

        email: [
          {
            required: true,
            type: 'email',
            message: '请输入正确邮箱',
            trigger: 'blur'
          }
        ]
      },

      register: {
        name: '',
        password: '',
        password2: '',
        email: ''
      },
      activeName: 'first'
    }
  },

  methods: {
    onSubmit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          alert('submit!')
          this.$ajax
            .post('oauth2/token', this.login)
            .then(response => {
              console.log(response)
            })
            .catch(function(error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>
