<template>
  <div class="table-contanier">
    <el-table class="table" v-loading.body="listLoading" element-loading-text="拼命加载中" :data="envs">
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
import { getEnvs } from '@/api/db'

export default {
  data() {
    return {
      envs: [],
      listLoading: true
    }
  },
  created() {
    this.fetchEnvs()
  },
  methods: {
    fetchEnvs() {
      this.listLoading = true
      getEnvs().then(response => {
        this.envs = response
        this.listLoading = false
        console.log(this.envs)
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
