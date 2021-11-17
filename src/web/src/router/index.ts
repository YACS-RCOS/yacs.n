import { routes } from './routes'
import { createRouter, createWebHistory } from 'vue-router'

export default createRouter({
  routes,
  history: createWebHistory()
})
