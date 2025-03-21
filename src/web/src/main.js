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
import VueMatomo from 'vue-matomo'

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VueCookies);
Vue.use(Meta);
Vue.$cookies.config("7d");
Vue.use(VueMatomo, {
  host: 'http://localhost:7070/',
  siteId: 1,
});

new Vue({
  render: (h) => h(App),
  router,
  components: { App },
  store,
}).$mount("#app");

window._paq.push(['trackPageView']); //To track pageview