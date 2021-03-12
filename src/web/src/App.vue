<template>
  <div id="root">
    <router-view></router-view>
  </div>
</template>

<script>
import { TOGGLE_DARK_MODE, SET_COURSE_LIST, COOKIE_DARK_MODE } from "@/store";
import { getCourses } from "@/services/YacsService";
import { getDefaultSemester } from "@/services/AdminService";

export const DARK_MODE_MEDIA_QUERY = "(prefers-color-scheme: dark)";

export default {
  name: "App",
  components: {},
  async created() {
    this.darkModeInit();

    const querySemester = this.$route.query.semester;
    this.selectedSemester =
      querySemester && querySemester != "null"
        ? querySemester
        : await getDefaultSemester();
    const courses = await getCourses(this.selectedSemester);
    this.$store.commit(SET_COURSE_LIST, courses);
  },
  methods: {
    darkModeInit() {
      this.syncColorScheme();
      this.registerColorSchemeListener();
    },
    syncColorScheme() {
      if (this.isCookieOrDeviceInDarkMode()) {
        this.$store.commit(TOGGLE_DARK_MODE);
      }
    },
    registerColorSchemeListener() {
      window.matchMedia(DARK_MODE_MEDIA_QUERY).addEventListener(
        "change", () => {
          if (this.isFollowingDeviceColor()) {
            this.$store.commit(TOGGLE_DARK_MODE);
        }
      });
    },
    isFollowingDeviceColor() {
      return this.$cookies.get(COOKIE_DARK_MODE) === null;
    },
    isCookieOrDeviceInDarkMode() {
      return this.$cookies.get(COOKIE_DARK_MODE) === "true" ||
              (this.isFollowingDeviceColor() &&
               window.matchMedia(DARK_MODE_MEDIA_QUERY).matches);
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
        { name: "color-scheme", content: "light dark" },
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
