import HelloWorld from '../components/HelloWorld.vue'
import Scheduler from '../views/Scheduler.vue'

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
  }
]
