import VueRouter from 'vue-router';
import AdminPage from './pages/AdminDashboard';
import MainPage from './pages/Main';
import UploadCsvPage from './pages/UploadCsv';
import MapDatePage from './pages/MapDates';

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
    },
    {
      path: '/admin/csv',
      component: UploadCsvPage,
      name: 'UploadCsv'
    },
    {
      path: '/admin/mapdate',
      component: MapDatePage,
      name: 'MapDates'
    }
  ],
  mode: 'history'
});

export default router;
