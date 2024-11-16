import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ActividadesNoticiasView from '../views/ActividadesNoticiasView.vue'
import ContactoView from '../views/ContactoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    { 
      path: '/actividades-noticias', 
      name: 'actividades-noticias', 
      component: ActividadesNoticiasView 
    },
    { 
      path: '/contacto', 
      name: 'contacto', 
      component: ContactoView 
    },
  ],
})

export default router
