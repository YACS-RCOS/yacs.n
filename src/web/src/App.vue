<template>
  <div id="root">
    <router-view></router-view>
  </div>
</template>

<script>
import { TOGGLE_DARK_MODE } from "@/store";

export default {
  name: "App",
  components: {},
  created() {
    if (this.$cookies.get("darkMode") == "true") {
      this.$store.commit(TOGGLE_DARK_MODE);
    }
  },
  computed: {
    darkMode() {
      return this.$store.state.darkMode;
    },
  },
  watch: {
    darkMode(newState, oldState) {
      if (newState === oldState) {
        return;
      }

      const bodyClassList = document.getElementsByTagName("body")[0].classList;
      if (newState) {
        bodyClassList.add("dark");
      } else {
        bodyClassList.remove("dark");
      }
    },
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
