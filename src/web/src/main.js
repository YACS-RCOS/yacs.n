import "@babel/polyfill";
import "mutationobserver-shim";
import "@/plugins";
import "vue-virtual-scroller/dist/vue-virtual-scroller.css";
import Vue from "vue";
import App from "./App.vue";
import router from "./routes";
import store from "./store";

Vue.config.productionTip = false;
Vue.config.performance = true;

new Vue({
  render: (h) => h(App),
  router,
  store,
}).$mount("#app");
