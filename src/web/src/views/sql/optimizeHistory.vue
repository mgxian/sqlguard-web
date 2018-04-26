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
      {{resultText}}
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
      ]
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
      getMySqls().then(response => {
        this.sqls = response
        this.listLoading = false
        // console.log(this.sqls)
      })
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
        this.resultText = response.result
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
</style>
