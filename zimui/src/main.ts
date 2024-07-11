import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import loadVuetify from './plugins/vuetify'

loadVuetify()
  .then((vuetify) => {
    const app = createApp(App)
    app.use(createPinia())
    app.use(vuetify)
    app.use(router)
    app.mount('#app')
  })
  .catch((error) => {
    console.error('Error initializing app:', error)
  })
