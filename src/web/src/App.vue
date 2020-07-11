<template>
  <div
    id="root"
    :class="$store.state.darkMode ? 'dark' : ' '"
  >
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
  created () {
    this.$store.commit("setDarkMode", this.$cookies.get("darkMode") == 'true');
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
