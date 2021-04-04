<template>
  <div id="root">
    <router-view></router-view>
  </div>
</template>

<script>
import { LOAD_DEPARTMENTS, TOGGLE_DARK_MODE } from "@/store";
import { TOGGLE_COLOR_BLIND_ASSIST } from "@/store";

export default {
  name: "App",
  components: {},
  async created() {
    if (this.$cookies.get("darkMode") == "true") {
      this.$store.commit(TOGGLE_DARK_MODE, true);
    }
    if (this.$cookies.get("colorBlindAssist") == "true") {
      this.$store.commit(TOGGLE_COLOR_BLIND_ASSIST, true);
    }

    this.$store.dispatch(LOAD_DEPARTMENTS);
  },
  metaInfo() {
    return {
      title: "YACS",
      titleTemplate: null,
      meta: [
        {
          vmid: "description",
          name: "description",
          content:
            "YACS is a RPI course scheduler to help students plan out their semester.",
        },
        {
          vmid: "keywords",
          content: "RPI, YACS, Rensselaer Polytechnic Institute",
        },
        { property: "og:title", content: "RPI - YACS Course Scheduler" },
        { property: "og:site_name", content: "YACS" },
        { property: "og:type", content: "website" },
        { name: "robots", content: "index" },
      ],
    };
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
