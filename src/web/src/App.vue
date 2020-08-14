<template>
  <div id="root" :class="$store.state.darkMode ? 'dark' : 'light'">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
  created() {
    if (this.$cookies.get("darkMode") == "true") {
      this.$store.commit("TOGGLE_DARK_MODE");
    }
  },
};
</script>

<style lang="scss">
@import "./assets/dark.scss";
#root,
html,
body {
  height: 100%;
}
</style>
