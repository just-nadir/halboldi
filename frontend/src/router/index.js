import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../pages/MainPage.vue'
import OrdersPage from '../pages/OrdersPage.vue'
import WorkersPage from '../pages/WorkersPage.vue'
import JobsPage from '../pages/JobsPage.vue'
import BalancePage from '../pages/BalancePage.vue'
import ReportsPage from '../pages/ReportsPage.vue'
import CalcelledOrdersPage from '../pages/CalcelledOrdersPage.vue'
import SmsLogsPage from '../pages/SmsLogsPage.vue'

// boshqa sahifalar...

const routes = [
  { path: '/', component: MainPage }, // Asosiy sahifa
  { path: '/orders', component: OrdersPage },
  { path: '/workers', component: WorkersPage },
  { path: '/jobs', component: JobsPage },
  { path: '/balance', component: BalancePage },
  { path: '/reports', component: ReportsPage},
  { path: '/cancelled-orders', component: CalcelledOrdersPage},
  { path: '/sms-logs', component: SmsLogsPage}
  // boshqa sahifalar bo‘lsa ularni ham shu yerga qo‘shasiz
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
