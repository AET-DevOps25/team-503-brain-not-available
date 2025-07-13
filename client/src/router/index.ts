import { createRouter, createWebHistory } from 'vue-router'

// Importiere deine Seitenkomponenten
import PageView from '@/views/PageView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

const routes = [
    { path: '/', name: 'Dashboard', component: PageView },
    { path: '/login', name: 'Dashboard', component: LoginView },
    { path: '/register', name: 'Register', component: RegisterView },
    { path: '/settings', name: 'Settings', component: PageView },
    { path: '/profile', name: 'Profile', component: PageView },
    { path: '/pages', name: 'PageViewEmpty', component: PageView },
    { path: '/pages/:id', name: 'PageView', component: PageView },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router