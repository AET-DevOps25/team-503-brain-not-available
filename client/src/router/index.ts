import { createRouter, createWebHistory } from 'vue-router'

// Importiere deine Seitenkomponenten
import PageView from '@/views/PageView.vue'

const routes = [
    { path: '/', name: 'Dashboard', component: PageView },
    { path: '/settings', name: 'Settings', component: PageView },
    { path: '/profile', name: 'Profile', component: PageView },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router