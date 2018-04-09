<template>
  <div class="table-contanier">
    <div class="table-header">
      <el-input class="search-input" v-model="queryText" placeholder="请输入地址" clearable></el-input>
      <el-button type="primary" icon="el-icon-search">搜索</el-button>
      <el-button @click="handleCreate" type="primary" icon="el-icon-edit">添加</el-button>
    </div>
    <el-table class="table" v-loading.body="listLoading" element-loading-text="拼命加载中" :data="mysqls">
      <el-table-column align="center" prop="id" label="数据库ID" sortable>
      </el-table-column>
      <el-table-column align="center" prop="host" label="地址">
      </el-table-column>
      <el-table-column align="center" prop="port" label="端口">
      </el-table-column>
      <el-table-column align="center" prop="username" label="用户名">
      </el-table-column>
      <el-table-column align="center" prop="database" label="数据库名">
      </el-table-column>
      <el-table-column align="center" prop="env_id" label="环境ID">
      </el-table-column>
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button @click="handleUpdate(scope.row)" type="primary" size="mini">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="编辑" :visible.sync="dialogEditVisible" :before-close="handleClose">
      <el-form v-if="temp" class="form" label-position="left" label-width="80px" :model="temp">
        <el-form-item label="ID">
          {{temp.id}}
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="temp.host" placeholder="请输入地址" clearable></el-input>
        </el-form-item>
        <el-form-item label="端口">
          <el-input v-model="temp.port" placeholder="请输入端口" clearable></el-input>
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="temp.username" placeholder="请输入用户名" clearable></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="temp.username" placeholder="请输入密码" clearable></el-input>
        </el-form-item>
        <el-form-item label="数据库名">
          <el-input v-model="temp.database" placeholder="请输入数据库名" clearable></el-input>
        </el-form-item>
        <el-form-item label="环境">
          <el-select v-model="temp.env_id" placeholder="请选择">
            <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogEditVisible = false">取消</el-button>
        <el-button type="primary" @click="updateMysql">确定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="添加" :visible.sync="dialogAddVisible" :before-close="handleClose">
      <el-form v-if="temp" class="form" label-position="left" label-width="80px" :model="temp">
        <el-form-item label="地址">
          <el-input v-model="temp.host" placeholder="请输入地址" clearable></el-input>
        </el-form-item>
        <el-form-item label="端口">
          <el-input v-model="temp.port" placeholder="请输入端口" clearable></el-input>
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="temp.username" placeholder="请输入用户名" clearable></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="temp.username" placeholder="请输入密码" clearable></el-input>
        </el-form-item>
        <el-form-item label="数据库名">
          <el-input v-model="temp.database" placeholder="请输入数据库名" clearable></el-input>
        </el-form-item>
        <el-form-item label="环境">
          <el-select v-model="temp.env_id" placeholder="请选择">
            <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogAddVisible = false">取消</el-button>
        <el-button type="primary" @click="createMysql">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getMySQLs, getEnvs } from '@/api/db'

export default {
  data() {
    return {
      mysqls: [],
      listLoading: true,
      dialogEditVisible: false,
      dialogAddVisible: false,
      temp: Object,
      envOptions: [],
      queryText: ''
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
        // console.log(this.mysqls)
      })
    },
    getEnvOptions() {
      if (this.envOptions.length !== 0) {
        return
      }
      getEnvs().then(response => {
        response.forEach(env => {
          this.envOptions.push({ value: env.id, label: env.name })
        })
      })
    },
    handleUpdate(data) {
      this.temp = Object.assign({}, data)
      this.getEnvOptions()
      this.dialogEditVisible = true
    },
    handleCreate() {
      this.resetTemp()
      this.getEnvOptions()
      this.dialogAddVisible = true
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    updateMysql() {
      // console.log(this.temp)
      this.dialogEditVisible = false
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        host: '',
        port: 3306,
        username: '',
        password: '',
        database: ''
      }
    },
    createMysql() {
      this.dialogAddVisible = false
    }
  }
}
</script>

<style lang="stylus" scoped>
.table-contanier
  margin 20px 100px
  border-radius 3px
  border 1px solid #ebebeb
  padding 24px

  .table-header
    .search-input
      width 25%
</style>
