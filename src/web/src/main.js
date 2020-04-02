import '@babel/polyfill';
import 'mutationobserver-shim';
import './plugins/bootstrap-vue';
import './plugins/fontawesome-vue';
import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router';
import router from './routes';
import store from './store'
import VueCookies from 'vue-cookies'


Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VueCookies);

Vue.$cookies.config('7d')

new Vue({
  render: h => h(App),
  store,
  router
}).$mount('#app');
