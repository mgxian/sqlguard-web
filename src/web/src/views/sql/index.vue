<template>
  <div class="table-contanier">
    <div class="table-header">
      <el-input class="search-input" v-model="queryText" placeholder="请输入地址" clearable></el-input>
      <el-button type="primary" icon="el-icon-search">搜索</el-button>
      <el-button @click="handleCreate" type="primary" icon="el-icon-edit">添加</el-button>
    </div>
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
    <el-dialog title="添加" :visible.sync="dialogCreateVisible">
      <el-form v-if="temp" class="form" label-position="left" label-width="80px" :model="temp">
        <el-form-item label="数据库">
          <el-select v-model="temp.mysql_id" placeholder="请选择">
            <el-option v-for="item in mysqlOptions" :key="item.value" :label="item.label" :value="item.value">
              <span style="float: left;width: 250px">{{ item.label }}</span>
              <el-tag type="primary" style="margin-left: 10px">{{ item.value }}</el-tag>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="SQL语句">
          <el-input v-model="temp.sql" type="textarea" placeholder="请输入SQL" clearable></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="temp.type" placeholder="请选择">
            <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogCreateVisible = false">取消</el-button>
        <el-button type="primary" @click="createSql">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getSqls, createSql } from '@/api/sql'
import { getMySQLs } from '@/api/db'

export default {
  data() {
    return {
      sqls: [],
      listLoading: true,
      dialogCreateVisible: false,
      mysqlOptions: [],
      typeOptions: [
        { value: 0, label: '优化建议' },
        { value: 1, label: '执行' }
      ],
      temp: Object,
      queryText: ''
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
        // console.log(this.sqls)
      })
    },
    handleCreate() {
      this.resetTemp()
      this.getMysqlOptions()
      this.dialogCreateVisible = true
    },
    resetTemp() {
      this.temp = {
        mysql_id: '',
        sql: '',
        type: 0
      }
    },
    getMysqlOptions() {
      if (this.mysqlOptions.length !== 0) {
        return
      }
      getMySQLs().then(response => {
        response.forEach(mysql => {
          const labelText = mysql.host + ':' + mysql.port + '/' + mysql.database
          this.mysqlOptions.push({ value: mysql.id, label: labelText })
        })
      })
    },
    createSql() {
      createSql(this.temp).then(response => {
        this.dialogCreateVisible = false
        this.fetchSqls()
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

  .table-header
    .search-input
      width 25%
</style>
