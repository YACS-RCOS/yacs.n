import VueRouter from 'vue-router';
import AdminPage from './pages/AdminDashboard';
import MainPage from './pages/Main';

var router = new VueRouter({
  routes: [
    {
      path: '/',
      component: MainPage,
      name: 'Schedule'
    },
    {
      path: '/Admin',
      component: AdminPage,
      name: 'Admin'
    }
  ],
  mode: 'history'
});

export default router;
