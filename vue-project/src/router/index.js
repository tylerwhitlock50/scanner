import { createRouter, createWebHistory } from 'vue-router';
import BatchInputView from '../views/BatchInputView.vue';
import OCRScanningViewTest from '../views/OCRScanningViewTest.vue';
import TransactionReviewView from '../views/TransactionReviewView.vue';
import ComplianceView  from '@/views/ComplianceView.vue'; 
import ReportingView  from '@/views/ReportingView.vue';
import BulkAddView  from '@/views/BulkAddView.vue';
import keycloak from '../services/keycloak';



const routes = [
  { path: '/', name: 'BatchInput', component: BatchInputView },
  { path: '/scan', name: 'OCRScanning', component: OCRScanningViewTest },
  { path: '/review', name: 'TransactionReviewView', component: TransactionReviewView },
  { path: '/compliance', name: 'ComplianceView', component: ComplianceView },
  { path: '/reporting', name: 'ReportingView', component: ReportingView },
  { path: '/bulk', name: 'BulkView', component: BulkAddView, meta:  { requiresAuth: true }  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!keycloak.authenticated) {
      // If not authenticated, redirect to the Keycloak login
      keycloak.login({ redirectUri: window.location.href });
    } else {
      next();  // Allow access to the route if authenticated
    }
  } else {
    next();  // No authentication required, allow access
  }
});

export default router;
