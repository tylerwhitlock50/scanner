<template>
    <div>
      <h2>Scan Serial Number</h2>
      <input v-model="scannedSerialNumber" placeholder="Enter or scan serial number" />
      <div>
        <label>
          <input type="checkbox" v-model="selectedForTesting" />
          Selected for Testing
        </label>
      </div>
      <button @click="confirmSerialNumber">Confirm</button>
    </div>
  </template>
  
  <script>
  import { useBatchStore } from '../stores/batchStore';
  import { ref } from 'vue';

  
  export default {
    emits: ['serial-number-confirmed'],
    setup(_, { emit }) {
      const scannedSerialNumber = ref('');
      const selectedForTesting = ref(false);
      const batchStore = useBatchStore();
  
      const confirmSerialNumber = () => {
        if (scannedSerialNumber.value) {
          const serialNumberData = {
            batch_id: batchStore.batchNumber,
            serial_number_extracted: scannedSerialNumber.value,
            testing_selected: selectedForTesting.value,
            // Add other required fields
            verified_sn: scannedSerialNumber.value, // Assuming verification is done here
          };
          emit('serial-number-confirmed', serialNumberData);
          scannedSerialNumber.value = '';
          selectedForTesting.value = false;
        } else {
          alert('Please scan or enter a serial number.');
        }
      };
  
      return {
        scannedSerialNumber,
        selectedForTesting,
        confirmSerialNumber,
      };
    },
  };
  </script>
  