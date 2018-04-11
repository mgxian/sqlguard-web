<template>
  <div class="table-contanier">
    <el-table class="table" v-loading.body="listLoading" element-loading-text="拼命加载中" :data="roles" :row-class-name="tableRowClassName">
      <el-table-column align="center" prop="name" label="英文角色名">
      </el-table-column>
      <el-table-column align="center" prop="name_zh" label="中文角色名">
      </el-table-column>
      <el-table-column align="center" prop="desc" label="描述">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getRoles } from '@/api/user'

export default {
  data() {
    return {
      roles: [],
      listLoading: true
    }
  },
  created() {
    this.fetchRoles()
  },
  methods: {
    fetchRoles() {
      this.listLoading = true
      getRoles().then(response => {
        this.roles = response
        this.listLoading = false
        // console.log(this.roles)
      })
    },
    tableRowClassName({ row }) {
      if (row.default) {
        return 'default-role'
      }
      return ''
    }
  }
}
</script>

<style lang="stylus" scoped>
.table-contanier
  margin 10px 100px
  border-radius 3px
  border 1px solid #ebebeb
  padding 24px

  .table
    .default-role
      background red
</style>
