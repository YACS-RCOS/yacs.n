import "@babel/polyfill";
import "mutationobserver-shim";
import "./plugins/bootstrap-vue";
import "./plugins/fontawesome-vue";
import Vue from "vue";
import Vuex from "vuex";
import App from "./App.vue";
import VueRouter from "vue-router";
import router from "./routes";
import VueCookies from "vue-cookies";
import "vue-virtual-scroller/dist/vue-virtual-scroller.css";

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VueCookies);
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    darkMode: false,
  },
  mutations: {
    setDarkMode(state, bool) {
      state.darkMode = bool;
      Vue.$cookies.set("darkMode", bool, null, null, null, null, "Strict");
    },
  },
});

Vue.$cookies.config("7d");

new Vue({
  render: (h) => h(App),
  router,
  store: store,
}).$mount("#app");
