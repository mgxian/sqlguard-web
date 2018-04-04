<template>
  <div class="table-contanier">
    <el-table class="table" v-loading.body="listLoading" element-loading-text="拼命加载中" :data="users">
      <el-table-column align="center" prop="id" label="ID" sortable>
      </el-table-column>
      <el-table-column align="center" prop="username" label="用户名">
      </el-table-column>
      <el-table-column align="center" prop="name" label="昵称">
      </el-table-column>
      <el-table-column align="center" prop="email" label="邮箱">
      </el-table-column>
      <el-table-column align="center" prop="roles" label="角色" :filters="filters" :filter-method="filterTag" filter-placement="bottom-end">
        <template slot-scope="scope">
          <el-tag v-if="filter.value === scope.row.roles[0]" v-for="filter in filters" :key="filter.value" :type="filter.type" close-transition>{{filter.text}}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getUsers } from '@/api/user'

export default {
  data() {
    return {
      users: [],
      listLoading: true,
      filters: [
        { text: '管理员', value: 'Administrator', type: 'primary' },
        { text: '经理', value: 'Manager', type: 'success' },
        { text: '开发人员', value: 'User', type: 'info' }
      ]
    }
  },
  created() {
    this.fetchUsers()
  },
  methods: {
    filterTag(value, row) {
      return row.roles[0] === value
    },
    fetchUsers() {
      this.listLoading = true
      getUsers().then(response => {
        this.users = response
        this.listLoading = false
        console.log(this.users)
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.table-contanier
  margin 10px
  border-radius 3px
  border 1px solid #ebebeb
  padding 24px
</style>

