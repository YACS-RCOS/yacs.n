import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import * as Icons from '@element-plus/icons-vue' // Introduce all icons , And named it Icons
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(router).use(ElementPlus)
// Register all through traversal svg Components , Will sacrifice a little performance 
for (let i in Icons) {
    app.component(i, Icons[i])
}
app.mount('#app')

// dev startup
// docker-compose -f docker-compose.yml -f docker-compose.development.yml up