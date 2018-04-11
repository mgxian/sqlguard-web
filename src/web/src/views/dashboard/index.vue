<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name:{{name}}</div>
    <div class="dashboard-text">
      role:<span>{{role.name_zh}}</span>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'dashboard',
  computed: {
    ...mapGetters(['name', 'role'])
  }
}
</script>

<style lang="stylus" scoped>
.dashboard-container
  margin 30px

.dashboard-text
  font-size 30px
  line-height 46px
</style>
