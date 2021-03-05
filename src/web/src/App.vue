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
} from "@/store";
export default {
  name: "App",
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
  created() {
    const bodyClassList = document.getElementsByTagName("body")[0].classList;
    if (this.$cookies.get("darkMode") == "true") {
      bodyClassList.add("dark");
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
