<template>
  <section class="app-main">
    <router-view :key="key"></router-view>
    <p v-for="i in 100" :key="i.id">xx</p>
  </section>
</template>

<script>
export default {
  name: 'AppMain',
  data () {
    return {
    }
  },
  computed: {
    key() {
      return 'bbb'
    }
  }
}
</script>

<style lang="stylus">
  .app-main {
    padding 20px 20px 20px 200px
  }
</style>
