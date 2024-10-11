import { createRouter, createWebHistory } from 'vue-router';
import BatchInputView from '../views/BatchInputView.vue';
import OCRScanningView from '../views/OCRScanningViewTest.vue';
import TransactionReviewView from '../views/TransactionReviewView.vue';

const routes = [
  { path: '/', name: 'BatchInput', component: BatchInputView },
  { path: '/scan', name: 'OCRScanning', component: OCRScanningView },
  { path: '/review', name: 'TransactionReviewView', component: TransactionReviewView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
