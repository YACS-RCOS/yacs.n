import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

export const TOGGLE_DARK_MODE = "TOGGLE_DARK_MODE";

const store = new Vuex.Store({
  state: {
    darkMode: false,
  },
  mutations: {
    [TOGGLE_DARK_MODE] (state) {
        state.darkMode = !state.darkMode;
        Vue.$cookies.set("darkMode", state.darkMode, null, null, null, null, "Strict");
    },
  },
});

export default store;