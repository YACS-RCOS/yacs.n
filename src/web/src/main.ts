import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

fetch('https://unpkg.com/spacingjs')
  .then((res) => res.text())
  .then((res) => eval(res))

const app = createApp(App)
app.use(router)
app.mount('#app')
