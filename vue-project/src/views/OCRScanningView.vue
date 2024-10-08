<template>
    <div>
      <h1>OCR Scanning</h1>
      <SerialNumberVerification @serial-number-confirmed="handleSerialNumberConfirmed" />
      <SerialNumberList :serialNumbers="serialNumbers" />
    </div>
  </template>
  
  <script>
  import { useSerialNumberStore } from '../stores/serialNumberStore';
  import SerialNumberVerification from '../components/SerialNumberVerification.vue';
  import SerialNumberList from '../components/SerialNumberList.vue';
  import api from '../services/api';
  
  export default {
    components: {
      SerialNumberVerification,
      SerialNumberList,
    },
    setup() {
      const serialNumberStore = useSerialNumberStore();
      const { serialNumbers } = storeToRefs(serialNumberStore);
  
      const handleSerialNumberConfirmed = async (serialNumberData) => {
        try {
          const response = await api.post('/serial_number', serialNumberData);
          serialNumberStore.addSerialNumber(response.data.data);
        } catch (error) {
          console.error('Error saving serial number:', error);
        }
      };
  
      return {
        serialNumbers,
        handleSerialNumberConfirmed,
      };
    },
  };
  </script>
  