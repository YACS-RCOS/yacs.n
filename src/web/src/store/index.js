import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    darkMode: false,
  },
  mutations: {
    setDarkMode (state, bool) {
      state.darkMode = bool;
      Vue.$cookies.set('darkMode', bool, null, null, null, null, "Strict");
    }
  }
});

export default store;