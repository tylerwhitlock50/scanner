<template>
    <div>
      <h1>Enter Batch Information</h1>
      <form @submit.prevent="submitBatch">
        <div>
          <label for="batchNumber">Batch Number:</label>
          <input v-model="batchNumber" id="batchNumber" required />
        </div>
        <div>
          <label for="numberOfItems">Number of Items:</label>
          <input type="number" v-model.number="numberOfItems" id="numberOfItems" required />
        </div>
        <button type="submit">Start Scanning</button>
      </form>
    </div>
  </template>
  
  <script>
  import { useBatchStore } from '../stores/batchStore';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const batchStore = useBatchStore();
      const router = useRouter();
      const batchNumber = ref('');
      const numberOfItems = ref(0);
  
      const submitBatch = () => {
        if (batchNumber.value && numberOfItems.value > 0) {
          batchStore.setBatchData(batchNumber.value, numberOfItems.value);
          router.push({ name: 'OCRScanning' });
        } else {
          alert('Please enter valid batch information.');
        }
      };
  
      return {
        batchNumber,
        numberOfItems,
        submitBatch,
      };
    },
  };
  </script>
  