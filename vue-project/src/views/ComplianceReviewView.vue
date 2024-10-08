<template>
    <div>
      <h1>Compliance Review</h1>
      <ul>
        <li v-for="serialNumber in serialNumbers" :key="serialNumber.id">
          {{ serialNumber.serial_number_extracted }}
          <button @click="markAsReviewed(serialNumber)">Mark as Reviewed</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import api from '../services/api';
  import { useBatchStore } from '../stores/batchStore';
  
  export default {
    setup() {
      const serialNumbers = ref([]);
      const batchStore = useBatchStore();
  
      const fetchSerialNumbers = async () => {
        try {
          const response = await api.get('/serial_numbers/query', {
            params: {
              batch_id: batchStore.batchNumber,
            },
          });
          serialNumbers.value = response.data.data;
        } catch (error) {
          console.error('Error fetching serial numbers:', error);
        }
      };
  
      const markAsReviewed = async (serialNumber) => {
        try {
          await api.put(`/serial_number/${serialNumber.id}`, { /* fields to update */ });
          // Update the local serialNumbers array if needed
        } catch (error) {
          console.error('Error updating serial number:', error);
        }
      };
  
      onMounted(fetchSerialNumbers);
  
      return {
        serialNumbers,
        markAsReviewed,
      };
    },
  };
  </script>
  