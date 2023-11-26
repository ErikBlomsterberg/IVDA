import { createApp } from 'vue'
import App from './App.vue'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/dist/vuetify.min.css'
import LabelizeRatings from './components/LabelizeRatings.vue'
import DataVisualization from './components/DataVisualization.vue'
import {createRouter, createWebHashHistory} from 'vue-router'

const vuetify = createVuetify({
  components,
  directives,
})

const routes = [
  { path: '/',name: 'LabelizeRatings', component: LabelizeRatings },
  { path: '/visualization', name: 'DataVisualization', component: DataVisualization},
]

const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
})



createApp(App).use(vuetify).use(router).mount('#app')
