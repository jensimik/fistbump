import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/add_problem',
      name: 'addproblem',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AddProblemView.vue')
    },
    {
      path: '/problem/:id',
      name: 'problem',
      component: () => import('../views/ProblemView.vue'),
      props: true,
    },
    {
      path: '/problem/:id/edit',
      name: 'problem_edit',
      component: () => import('../views/EditProblemView.vue'),
      props: true,
    },
    {
      path: '/section/:id',
      name: 'section',
      component: () => import('../views/SectionView.vue'),
      props: true,
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
    }
  ]
})

export default router
