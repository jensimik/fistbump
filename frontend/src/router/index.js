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
      name: 'add_problem',
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
      path: '/problems',
      name: 'problems',
      component: () => import('../views/ProblemsView.vue'),
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
    },
    {
      path: '/setter-stats',
      name: 'setter-stats',
      component: () => import('../views/SetterStatsView.vue'),
    },
    {
      path: '/stokt-stats',
      name: 'stokt-stats',
      component: () => import('../views/StoktStatsView.vue'),
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(savedPosition)
        }, 250)
      })
    } else {
      return { top: 0 }
    }
  },
})

export default router
