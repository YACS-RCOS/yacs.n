import '@babel/polyfill';
import 'mutationobserver-shim';
import './plugins/bootstrap-vue';
import './plugins/fontawesome-vue';
import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router';
import router from './routes';

Vue.config.productionTip = false;

Vue.use(VueRouter);

new Vue({
  render: h => h(App),
  router
}).$mount('#app');
