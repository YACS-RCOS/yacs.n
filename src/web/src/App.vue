<template>
  <div id="root">
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<script>
import {
  LOAD_DEPARTMENTS,
  LOAD_SEMESTERS,
  LOAD_SUBSEMESTERS,
  SELECT_SEMESTER,
  TOGGLE_DARK_MODE,
} from "@/store";
export default {
  name: "App",
  created() {
    if (this.$cookies.get("darkMode") == "true") {
      this.$store.commit(TOGGLE_DARK_MODE, true);
    }

    this.$store.dispatch(SELECT_SEMESTER);
    this.$store.dispatch(LOAD_DEPARTMENTS);
    this.$store.dispatch(LOAD_SEMESTERS);
    this.$store.dispatch(LOAD_SUBSEMESTERS);
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
