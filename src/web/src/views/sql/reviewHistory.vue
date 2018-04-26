<template>
  <div class="table-contanier">
    <div class="table-header">
      <el-input class="search-input" v-model="queryText" placeholder="请输入地址" clearable></el-input>
      <el-button type="primary" icon="el-icon-search">搜索</el-button>
    </div>
    <el-table class="table" v-loading.body="listLoading" element-loading-text="拼命加载中" :data="sqls">
      <el-table-column label="数据库">
        <template slot-scope="scope">
          {{scope.row.mysql.database}}
          <el-tag v-if="filter.name === scope.row.mysql.env.name" v-for="filter in envFilters" :key="filter.name" :type="filter.type" close-transition>
            {{scope.row.mysql.env.name_zh}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="sql" label="SQL">
      </el-table-column>
      <el-table-column align="center" prop="result" label="语法检查结果">
      </el-table-column>
      <el-table-column align="center" prop="result_execute" label="执行结果">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getSqls } from '@/api/sql'

const TYPE_INCEPTION = 1
export default {
  data() {
    return {
      sqls: [],
      listLoading: true,
      queryText: '',
      envFilters: [
        { name: 'Development', type: 'info' },
        { name: 'Staging', type: 'warning' },
        { name: 'Production', type: 'danger' }
      ]
    }
  },
  created() {
    this.fetchSqls()
  },
  methods: {
    fetchSqls() {
      this.listLoading = true
      getSqls(TYPE_INCEPTION).then(response => {
        this.sqls = response
        this.listLoading = false
        // console.log(this.sqls)
      })
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

  .table-header
    .search-input
      width 25%

  .el-icon-circle-check, .el-icon-circle-close
    font-size 24px
    line-height 24px
    vertical-align top

  .el-icon-circle-check
    color green

  .el-icon-circle-close
    color red
</style>
