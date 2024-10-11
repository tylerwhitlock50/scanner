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
    },
  }),
  actions: {
    // Method to get batch data
    getBatchData() {
      return this.batchData;
    },
    // Method to set or update batch data
    setBatchData(batchNumber, numberOfItems, partNumber) {
      this.batchData = {
        batchNumber: batchNumber,
        numberOfItems: numberOfItems,
        partNumber: partNumber,
        batchVerified: false,
        currentCount: 0,
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
  },
});
