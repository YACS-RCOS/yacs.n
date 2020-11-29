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

import store from "./store";

new Vue({
  render: (h) => h(App),
  router,
  store,
}).$mount("#app");
