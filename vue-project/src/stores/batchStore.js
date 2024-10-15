// stores/batchStore.js
import { defineStore } from 'pinia';

export const useBatchStore = defineStore('batch', {
  state: () => ({
    batchData: {
      batchNumber: '', // Example default value
      numberOfItems: 0,    // Example default value
      partNumber: '', // Example default value
      batchVerified: false,
      currentCount: 0,
      batchType: 'inbound', // Example default value
      batch_description: '', // Example default value
      batch_info_id: null, // Example default value
    },
  }),
  actions: {
    // Method to get batch data
    getBatchData() {
      return this.batchData;
    },
    // Method to set or update batch data
    setBatchData(batchNumber, numberOfItems, partNumber, batchType, batch_description, batch_info_id) {
      this.batchData = {
        batchNumber: batchNumber,
        numberOfItems: numberOfItems,
        partNumber: partNumber,
        batchVerified: false,
        currentCount: 0,
        batchType: batchType,
        batch_description: batch_description,
        batch_info_id: batch_info_id,
      };
    },
    // Method to verify batch
    verifyBatch() {
      this.batchData.batchVerified = true;
    },
    // Method to increment current count
    incrementCurrentCount() {
      this.batchData.currentCount++;
    },
    // Method to update current count
    setCurrentCount(count) {
      this.batchData.currentCount = count;
    },
  },
});
