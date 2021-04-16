import "@babel/polyfill";
import "mutationobserver-shim";
import "./plugins/bootstrap-vue";
import "./plugins/fontawesome-vue";
import "./registerServiceWorker";
import "vue-virtual-scroller/dist/vue-virtual-scroller.css";
import store from "./store";
import Vue from "vue";
import App from "./App.vue";
import VueRouter from "vue-router";
import router from "./routes";
import VueCookies from "vue-cookies";
import Meta from "vue-meta";

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VueCookies);
Vue.use(Meta);

Vue.$cookies.config("7d");

new Vue({
  render: (h) => h(App),
  router,
  store,
}).$mount("#app");
