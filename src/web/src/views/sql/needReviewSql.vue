<template>
  <div class="table-contanier">
    <div class="table-header">
      <el-input class="search-input" v-model="queryText" placeholder="请输入地址" clearable></el-input>
      <el-button type="primary" icon="el-icon-search">搜索</el-button>
      <!-- <el-button @click="handleCreate" type="primary" icon="el-icon-edit">添加</el-button> -->
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
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button @click="handleExecute(scope.row)" type="danger" size="mini">执行</el-button>
        </template>
      </el-table-column>
      <!-- <el-table-column align="center" prop="result_execute" label="执行结果">
      </el-table-column> -->
    </el-table>
    <el-dialog title="执行确认" :visible.sync="dialogConfirmVisible">
      <span>确定要执行吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogConfirmVisible = false">取消</el-button>
        <el-button type="primary" @click="executeSql">确定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="执行结果" :visible.sync="dialogResultVisible">
      <div v-if="isHaveError">
        <h4>SQL: {{resultSql}}</h4>
        <li v-for="(line,index) in resultText" :key="index">
          {{line.sql}}
          <ul v-for="(line,index) in line.result" :key="index">{{line}}</ul>
        </li>
      </div>
      <h3 v-if="!isHaveError">
        {{executeSuccessText}}
        <i class="el-icon-circle-check"></i>
      </h3>
      <h3 v-if="isHaveError">
        {{executeFailureText}}
        <i class="el-icon-circle-close"></i>
      </h3>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogResultVisible = false">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getMySqls, executeSql } from '@/api/sql'
const TYPE = 1
export default {
  data() {
    return {
      status: 0,
      sqls: [],
      listLoading: true,
      queryText: '',
      envFilters: [
        { name: 'Development', type: 'info' },
        { name: 'Staging', type: 'warning' },
        { name: 'Production', type: 'danger' }
      ],
      dialogResultVisible: false,
      dialogConfirmVisible: false,
      result: '',
      resultText: [],
      executeSuccessText: '执行成功',
      executeFailureText: '执行失败',
      temp: {}
    }
  },
  created() {
    this.fetchSqls()
  },
  computed: {
    isHaveError() {
      if (this.resultText.length === 0) {
        return false
      }
      return true
    }
  },
  watch: {
    result: function() {
      this.resultSql = this.temp.sql
      if (this.result.length === 0) {
        this.resultText = []
        return
      }

      const rows = this.result.split('||')
      const sqlResuts = []
      rows.forEach(row => {
        const tmp = row.split('|')
        const sql = tmp[0]
        const result = tmp[1]
        sqlResuts.push({
          sql,
          result: result.split('\n')
        })
      })

      this.resultText = sqlResuts
      // console.log(this.resultText)
    }
  },
  methods: {
    fetchSqls() {
      this.listLoading = true
      getMySqls(TYPE).then(response => {
        this.sqls = response
        this.listLoading = false
        // console.log(this.sqls)
      })
    },
    executeSql() {
      this.dialogConfirmVisible = false
      executeSql(this.temp.mysql_id, this.temp.id).then(response => {
        this.result = response.result_execute
        this.dialogResultVisible = true
        this.fetchSqls()
      })
    },

    handleExecute(data) {
      this.temp = data
      this.dialogConfirmVisible = true
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
