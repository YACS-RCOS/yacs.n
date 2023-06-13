<template>
<b-col>
  <b-row>
    <b-dropdown text="Color Mode" style="padding-right: 5px;">
      <b-dropdown-item
        :class="this.darkMode === false ? 'drop-down-item' : ''"
        @click="toggle_style(false)"
      >
        Light Mode
      </b-dropdown-item>
      <b-dropdown-item
        :class="this.darkMode === true ? 'drop-down-item' : ''"
        @click="toggle_style(true)"
      >
        Dark Mode
      </b-dropdown-item>
      <b-dropdown-item
        :class="this.darkMode === null ? 'drop-down-item' : ''"
        @click="toggle_device"
      >
        Follow Device Theme
      </b-dropdown-item>
    </b-dropdown>

  </b-row>

  <b-row>
    <b-form-checkbox
      class="mt-2"
      size="sm"
      :checked="$store.state.colorBlindAssist"
      @change="toggleColors()"
      switch
    >
      Color Blind Assistance
    </b-form-checkbox>
  </b-row>
</b-col>
</template>


<script>

import { mapGetters, mapState } from "vuex";

import {
  COOKIE_DARK_MODE,
  TOGGLE_DARK_MODE,
  SAVE_DARK_MODE,
  RESET_DARK_MODE,
  TOGGLE_COLOR_BLIND_ASSIST,
} from "@/store";

export default {
  name: "Settings",
  data() {
    return {
      darkMode: this.$store.getters.darkModeState, //false for light mode, true for dark mode
      notify: false,
      // colorBlindAssist: this.$store.getters.colorBlindAssistState,
    };
  },
  mounted() {
    if (this.$cookies.get(COOKIE_DARK_MODE) === null) {
      this.darkMode = null;
      this.notify = true;
    }
  },
  methods: {
    toggle_style(mode) {
      //Sends message to user that device theme is no longer followed
      if (this.notify) {
        this.unFollowDeviceTheme();
        this.notify = false;
      }

      //determines the default theme of user (either light or dark)
      const deviceTheme = window.matchMedia("(prefers-color-scheme: dark)")
        .matches;

      //if the button mode user pressed is opposite of the current color, then toggle
      // OR if the user was previously following their device theme and button pressed isn't their device theme, toggle
      if (
        (mode === false && this.darkMode === true) ||
        (mode === true && this.darkMode === false) ||
        (this.darkMode == null && mode !== deviceTheme)
      ) {
        this.$store.commit(TOGGLE_DARK_MODE);
        this.$store.commit(SAVE_DARK_MODE);
      } else {
        // if user was following device theme and pressed the same button color, make the cookie with curr color
        this.$store.commit(SAVE_DARK_MODE);
      }

      this.darkMode = this.$store.getters.darkModeState; //resets to match current color mode
    },
    toggle_device() {
      this.followDeviceTheme(); //sends user message
      this.notify = true;

      this.$store.commit(RESET_DARK_MODE);
      this.$store.commit(TOGGLE_DARK_MODE);
      this.darkMode = null; //sets color mode
    },
    unFollowDeviceTheme() {
      this.$bvToast.toast(`No Longer Following Device Theme`, {
        title: "Color Scheme Changed",
        autoHideDelay: 2000,
        noHoverPause: true,
        variant: "danger",
        toaster: "b-toaster-top-center",
      });
    },
    followDeviceTheme() {
      this.$bvToast.toast(`Now Following Device Theme`, {
        title: "Color Scheme Changed",
        autoHideDelay: 2000,
        noHoverPause: true,
        variant: "success",
        toaster: "b-toaster-top-center",
      });
    },
    toggleColors() {
      this.$store.commit(TOGGLE_COLOR_BLIND_ASSIST);
    },
  }
};

</script>