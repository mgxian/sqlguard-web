<template>
  <div class="table-contanier">
    <el-table class="table" v-loading.body="listLoading" element-loading-text="拼命加载中" :data="mysqls">
      <el-table-column align="center" prop="id" label="ID" sortable>
      </el-table-column>
      <el-table-column align="center" prop="host" label="地址">
      </el-table-column>
      <el-table-column align="center" prop="port" label="端口">
      </el-table-column>
      <el-table-column align="center" prop="username" label="连接用户名">
      </el-table-column>
      <el-table-column align="center" prop="database" label="数据库名">
      </el-table-column>
      <el-table-column align="center" prop="env_id" label="环境ID">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getMySQLs } from '@/api/db'

export default {
  data() {
    return {
      mysqls: [],
      listLoading: true
    }
  },
  created() {
    this.fetchMySQLs()
  },
  methods: {
    filterTag(value, row) {
      return row.roles[0] === value
    },
    fetchMySQLs() {
      this.listLoading = true
      getMySQLs().then(response => {
        this.mysqls = response
        this.listLoading = false
        console.log(this.mysqls)
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
