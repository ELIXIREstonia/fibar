import Vue from 'vue'
import App from './App.vue'


import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';
import VueRouter from 'vue-router'
import VueCompositionAPI from '@vue/composition-api'

Vue.use(VueCompositionAPI)
Vue.use(VueRouter)

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);



Vue.config.productionTip = false

import Upload from './components/Upload.vue'
import About from './components/About.vue'
import Guide from './components/Guide.vue'

const routes = [
  { path: '/', component: Upload },
  { path: '/cite', component: About },
  { path: '/guide', component: Guide }

]

const router = new VueRouter({
  mode: 'history',
  base: '/',
  routes
})

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})