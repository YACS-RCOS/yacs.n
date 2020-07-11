import "@babel/polyfill";
import "mutationobserver-shim";
import "./plugins/bootstrap-vue";
import "./plugins/fontawesome-vue";
import Vue from "vue";
import App from "./App.vue";
import VueRouter from "vue-router";
import router from "./routes";
import VueCookies from "vue-cookies";
import "vue-virtual-scroller/dist/vue-virtual-scroller.css";

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VueCookies);

Vue.$cookies.config("7d");

// global dark mode variable
Vue.prototype.$darkMode = localStorage.darkMode;

new Vue({
  render: (h) => h(App),
  router,
}).$mount("#app");
