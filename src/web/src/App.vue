<template>
  <div id="root">
    <router-view></router-view>
  </div>
</template>

<script>
import { TOGGLE_DARK_MODE, SET_COURSE_LIST } from "@/store";
import { getCourses } from "@/services/YacsService";
import { getDefaultSemester } from "@/services/AdminService";

export default {
  name: "App",
  components: {},
  async created() {
    if (this.$cookies.get("darkMode")  === "true" ||
        (this.$cookies.get("darkMode") ===  null  &&
          window.matchMedia("(prefers-color-scheme: dark)").matches)) {
      this.$store.commit(TOGGLE_DARK_MODE);
    }

    const querySemester = this.$route.query.semester;
    this.selectedSemester =
      querySemester && querySemester != "null"
        ? querySemester
        : await getDefaultSemester();
    const courses = await getCourses(this.selectedSemester);
    this.$store.commit(SET_COURSE_LIST, courses);
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
