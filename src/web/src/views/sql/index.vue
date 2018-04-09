<template>
  <div class="table-contanier">
    <el-table class="table" v-loading.body="listLoading" element-loading-text="拼命加载中" :data="sqls">
      <el-table-column align="center" prop="id" label="ID" sortable>
      </el-table-column>
      <el-table-column align="center" prop="mysql_id" label="MySQL-ID">
      </el-table-column>
      <el-table-column align="center" prop="sql" label="SQL">
      </el-table-column>
      <el-table-column align="center" prop="type" label="类型">
      </el-table-column>
      <el-table-column align="center" prop="user_id" label="用户">
      </el-table-column>
      <el-table-column align="center" prop="status" label="状态">
      </el-table-column>
      <el-table-column align="center" prop="result" label="结果">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getSqls } from '@/api/sql'

export default {
  data() {
    return {
      sqls: [],
      listLoading: true
    }
  },
  created() {
    this.fetchSqls()
  },
  methods: {
    fetchSqls() {
      this.listLoading = true
      getSqls().then(response => {
        this.sqls = response
        this.listLoading = false
        console.log(this.sqls)
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
