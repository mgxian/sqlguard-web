<template>
  <div class="table-contanier">
    <el-table class="table" v-loading.body="listLoading" element-loading-text="拼命加载中" :data="roles">
      <el-table-column align="center" prop="id" label="ID" sortable>
      </el-table-column>
      <el-table-column align="center" prop="name" label="角色名">
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
    filterTag(value, row) {
      return row.roles[0] === value
    },
    fetchRoles() {
      this.listLoading = true
      getRoles().then(response => {
        this.roles = response
        this.listLoading = false
        console.log(this.roles)
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
