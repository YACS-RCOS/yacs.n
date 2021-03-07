import Vue from "vue";
import Vuex from "vuex";

import { userModule, USER_NAMESPACE } from "./modules/user";

Vue.use(Vuex);

export const TOGGLE_DARK_MODE = "TOGGLE_DARK_MODE";
export const SAVE_DARK_MODE   = "SAVE_DARK_MODE";
export const RESET_DARK_MODE  = "RESET_DARK_MODE";
export const SET_COURSE_LIST  = "SET_COURSE_LIST";

const store = new Vuex.Store({
  state: {
    darkMode: false,
    courseList: [],
  },
  mutations: {
    [TOGGLE_DARK_MODE](state) {
      if (Vue.$cookies.get("darkMode" === null)) {
        state.darkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
      } else {
        state.darkMode = !state.darkMode;
      }
    },
    [SAVE_DARK_MODE](state) {
      Vue.$cookies.set(
        "darkMode",
        state.darkMode,
        null,
        null,
        null,
        null,
        "Strict"
      );
    },
    [RESET_DARK_MODE](state) {
      Vue.$cookies.remove("darkMode");
      state.darkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
    },
    [SET_COURSE_LIST](state, classes) {
      state.courseList = classes;
    },
  },
  modules: {
    [USER_NAMESPACE]: userModule,
  },
});

export default store;
