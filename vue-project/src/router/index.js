import { createRouter, createWebHistory } from 'vue-router';
import BatchInputView from '../views/BatchInputView.vue';
import OCRScanningViewTest from '../views/OCRScanningViewTest.vue';
import TransactionReviewView from '../views/TransactionReviewView.vue';
import ComplianceView  from '@/views/ComplianceView.vue'; 
import ReportingView  from '@/views/ReportingView.vue';
import BulkAddView  from '@/views/BulkAddView.vue';



const routes = [
  { path: '/', name: 'BatchInput', component: BatchInputView },
  { path: '/scan', name: 'OCRScanning', component: OCRScanningViewTest },
  { path: '/review', name: 'TransactionReviewView', component: TransactionReviewView },
  { path: '/compliance', name: 'ComplianceView', component: ComplianceView },
  { path: '/reporting', name: 'ReportingView', component: ReportingView },
  { path: '/bulk', name: 'BulkView', component: BulkAddView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
