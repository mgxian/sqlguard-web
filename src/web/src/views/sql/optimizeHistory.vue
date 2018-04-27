<template>
  <div class="table-contanier">
    <div class="table-header">
      <el-input class="search-input" v-model="queryText" placeholder="请输入地址" clearable></el-input>
      <el-button type="primary" icon="el-icon-search">搜索</el-button>
      <el-button @click="handleCreate" type="primary" icon="el-icon-edit">添加</el-button>
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
      <el-table-column align="center" prop="result" label="优化建议">
      </el-table-column>
    </el-table>
    <div v-if="sqls.length>0" class="page">
      <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="pageSizes" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total">
      </el-pagination>
    </div>
    <el-dialog title="添加" :visible.sync="dialogCreateVisible">
      <el-form class="form" label-position="left" label-width="80px" :model="temp">
        <el-form-item label="环境">
          <el-select v-model="selectedEnv" placeholder="请选择">
            <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据库">
          <el-select v-model="temp.mysql_id" placeholder="请选择">
            <el-option v-for="item in mysqlOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="SQL语句">
          <el-input v-model="temp.sql" type="textarea" placeholder="请输入SQL" clearable></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogCreateVisible = false">取消</el-button>
        <el-button type="primary" @click="createSql">确定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="优化建议" :visible.sync="dialogResultVisible">
      <h3 v-if="!isHaveError">
        {{resultText}}
        <i class="el-icon-circle-check"></i>
      </h3>
      <h3 v-if="isHaveError">
        {{resultText}}
        <i class="el-icon-circle-close"></i>
      </h3>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogResultVisible = false">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getMySqls, createSql } from '@/api/sql'
import { getMySQLs, getEnvs } from '@/api/db'

const TYPE_SQLADVISOR = 0

export default {
  data() {
    return {
      sqls: [],
      listLoading: true,
      queryText: '',
      resultText: '',
      temp: {},
      dialogCreateVisible: false,
      dialogResultVisible: false,
      mysqlOptions: [],
      envOptions: [],
      selectedEnv: '',
      envFilters: [
        { name: 'Development', type: 'info' },
        { name: 'Staging', type: 'warning' },
        { name: 'Production', type: 'danger' }
      ],
      isHaveError: false,
      currentPage: 1,
      total: 40,
      pageSizes: [10, 20, 50, 100],
      pageSize: 10
    }
  },
  created() {
    this.fetchSqls()
  },
  watch: {
    selectedEnv: function() {
      this.getMysqlOptions()
    }
  },
  methods: {
    fetchSqls() {
      this.listLoading = true
      getMySqls(TYPE_SQLADVISOR, this.pageSize, this.currentPage).then(
        response => {
          this.sqls = response.sqls
          this.total = response.total
          this.listLoading = false
          // console.log(this.total)
        }
      )
    },
    handleCreate() {
      this.resetTemp()
      this.getEnvOptions()
      this.dialogCreateVisible = true
    },
    resetTemp() {
      this.temp = {
        mysql_id: '',
        sql: '',
        selectedEnv: '',
        type: TYPE_SQLADVISOR
      }
    },
    getEnvOptions() {
      if (this.envOptions.length !== 0) {
        return
      }
      getEnvs().then(response => {
        response.forEach(env => {
          this.envOptions.push({ value: env.id, label: env.name_zh })
        })
      })
    },
    getMysqlOptions() {
      this.mysqlOptions = []
      getMySQLs(this.selectedEnv).then(response => {
        response.forEach(mysql => {
          // const labelText = mysql.host + ':' + mysql.port + '/' + mysql.database
          const labelText = mysql.database
          this.mysqlOptions.push({ value: mysql.id, label: labelText })
        })
      })
    },
    createSql() {
      this.dialogCreateVisible = false
      createSql(this.temp).then(response => {
        this.dialogCreateVisible = false
        if (response.has_error) {
          this.resultText = '系统错误，无法给出优化建议'
          this.isHaveError = true
        } else {
          this.resultText = response.result
          this.isHaveError = false
        }

        this.dialogResultVisible = true
        // this.showResult(response.result)
        this.fetchSqls()
      })
    },
    showResult(result) {
      this.$alert(result, '优化建议', {
        confirmButtonText: '确定',
        lockScroll: false,
        callback: action => {}
      })
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
    },
    handleCurrentChange(val) {
      this.currentPage = val
      // console.log(`当前页: ${this.currentPage}`)
      // console.log(`每页 ${this.pageSize} 条`)
      this.fetchSqls()
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

  .page
    text-align center
    padding-top 24px
</style>
