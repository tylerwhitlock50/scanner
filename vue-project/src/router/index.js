import { createRouter, createWebHistory } from 'vue-router';
import BatchInputView from '../views/BatchInputView.vue';
import OCRScanningView from '../views/OCRScanningView.vue';
import ComplianceReviewView from '../views/ComplianceReviewView.vue';

const routes = [
  { path: '/', name: 'BatchInput', component: BatchInputView },
  { path: '/scan', name: 'OCRScanning', component: OCRScanningView },
  { path: '/review', name: 'ComplianceReview', component: ComplianceReviewView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
