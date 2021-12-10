import HelloWorld from '../components/HelloWorld.vue'
import Scheduler from '../views/Scheduler.vue'
import Admin from '../views/admin/index.vue'

export const routes = [
  {
    path: '/',
    name: 'schedule',
    component: Scheduler
  },
  {
    path: '/explore',
    name: 'explore',
    component: HelloWorld
  },
  {
    path: '/admin',
    name: 'admin',
    component: Admin
  }
]
