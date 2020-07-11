<template>
  <div
    id="root" 
    :class="$darkMode ? 'dark' : ' '"
  >
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
  beforeDestroy () {
    // save style state to local storage
    localStorage.darkMode = this.$darkMode;
    console.log(this.$darkMode);
  },
};
</script>

<style lang="scss">
#root,
html,
body {
  height: 100%;
}

.dark {
  background-color: #111 !important;
}

</style>
