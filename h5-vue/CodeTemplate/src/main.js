import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'
import locale from 'element-plus/dist/locale/zh-cn.mjs'
import './assets/main.css'

const app = createApp(App)

app.use(router)
app.use(ElementPlus, { locale })
app.mount('#app')
