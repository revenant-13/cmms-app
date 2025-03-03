import { createRouter, createWebHistory } from 'vue-router';
import Equipment from '../components/Equipment.vue';
import Parts from '../components/Parts.vue';
import Tasks from '../components/Tasks.vue';
import Schedules from '../components/Schedules.vue';
import Dashboard from '../components/Dashboard.vue';

const routes = [
  { path: '/', name: 'DashboardPage', component: Dashboard }, // Replaced Home with Dashboard
  { path: '/equipment', name: 'EquipmentPage', component: Equipment },
  { path: '/parts', name: 'PartsPage', component: Parts },
  { path: '/tasks', name: 'TasksPage', component: Tasks },
  { path: '/schedules', name: 'SchedulesPage', component: Schedules }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;