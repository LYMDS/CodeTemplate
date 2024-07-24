import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children:[
        {
          path: '/about',
          name: 'about',
          component: () => import('../views/AboutView.vue'),
          meta: {
            title: '关于'
          }
        },
        {
          path: '/TemplateGroupList',
          name: 'TemplateGroupList',
          component: () => import('../views/TemplateGroupList.vue'),
          meta: {
            title: '模板组列表页'
          }
        },
        {
          path: '/TemplateGroupEdit',
          name: 'TemplateGroupEdit',
          component: () => import('../views/TemplateGroupEdit.vue'),
          meta: {
            title: '模板组详情页'
          }
        },
        {
          path: '/TemplateContentEdit',
          name: 'TemplateContentEdit',
          component: () => import('../views/TemplateContentEdit.vue'),
          meta: {
            title: '模板内容详情页'
          }
        }
      ]
    },
    {
      path: '/RichText',
      name: 'RichText',
      component: () => import('../views/RichTextTest.vue')
    }
  ]
})

export default router
