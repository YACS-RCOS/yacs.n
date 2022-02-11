import Schedule from '../views/Schedule.vue'
import Admin from '../views/Admin.vue'
import Explore from '../views/Explore.vue'

export default [
    { path: '/', name: 'schedule', component: Schedule, meta: { sideBar: true } },
    { path: '/explore', name: 'explore', component: Explore, meta: { sideBar: true } },
    { path: '/admin', name: 'admin', component: Admin }
]