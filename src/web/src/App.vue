<template>
  <div id="root">
    <router-view></router-view>
  </div>
</template>

<script>
import {
  LOAD_DEPARTMENTS,
  TOGGLE_COLOR_BLIND_ASSIST,
  TOGGLE_DARK_MODE,
  COOKIE_DARK_MODE,
} from "@/store";

export const DARK_MODE_MEDIA_QUERY = "(prefers-color-scheme: dark)";

export default {
  name: "App",
  components: {},
  async created() {
    this.darkModeInit();

    if (this.$cookies.get("colorBlindAssist") == "true") {
      this.$store.commit(TOGGLE_COLOR_BLIND_ASSIST, true);
    }

    this.$store.dispatch(LOAD_DEPARTMENTS);
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
      window
        .matchMedia(DARK_MODE_MEDIA_QUERY)
        .addEventListener("change", () => {
          if (this.isFollowingDeviceColor()) {
            this.$store.commit(TOGGLE_DARK_MODE);
          }
        });
    },
    isFollowingDeviceColor() {
      return this.$cookies.get(COOKIE_DARK_MODE) === null;
    },
    isCookieOrDeviceInDarkMode() {
      return (
        this.$cookies.get(COOKIE_DARK_MODE) === "true" ||
        (this.isFollowingDeviceColor() &&
          window.matchMedia(DARK_MODE_MEDIA_QUERY).matches)
      );
    },
  },
  computed: {
    colorSchemeMeta() {
      return this.isFollowingDeviceColor()
              ? "light dark"
              : this.$cookies.get(COOKIE_DARK_MODE) === "true"
                  ? "dark"
                  : "light";
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
        { name: "color-scheme", content: this.colorSchemeMeta },
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
