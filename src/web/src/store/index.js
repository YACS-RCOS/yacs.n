import Vue from "vue";
import Vuex from "vuex";

import { userModule, USER_NAMESPACE } from "./modules/user";

Vue.use(Vuex);

export const TOGGLE_DARK_MODE = "TOGGLE_DARK_MODE";
export const SET_COURSE_LIST = "SET_COURSE_LIST";

const store = new Vuex.Store({
  state: {
    darkMode: false,
    courseList: [],
  },
  mutations: {
    [TOGGLE_DARK_MODE](state) {
      state.darkMode = !state.darkMode;
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
    [SET_COURSE_LIST](state, classes) {
      state.courseList = classes;
    },
  },
  modules: {
    [USER_NAMESPACE]: userModule,
  },
});

export default store;
