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
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button @click="handlePass(scope.$index, scope.row)" type="success" size="mini">通过</el-button>
          <el-button @click="handleNoPass(scope.$index, scope.row)" type="danger" size="mini">不通过</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getNeedReviewSqls, executeSql } from '@/api/sql'

export default {
  data() {
    return {
      status: 0,
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
      getNeedReviewSqls(this.status).then(response => {
        this.sqls = response
        this.listLoading = false
        console.log(this.sqls)
      })
    },
    handlePass(index, data) {
      console.log(index, data)
      executeSql(data.mysql_id, data.id).then(response => {
        this.fetchSqls()
      })
    },
    handleNoPass(index, data) {
      console.log(index, data)
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
