import { defineStore } from 'pinia';

export const useBatchStore = defineStore('batch', {
  state: () => ({
    batchNumber: '',
    numberOfItems: 0,
  }),
  actions: {
    setBatchData(batchNumber, numberOfItems) {
      this.batchNumber = batchNumber;
      this.numberOfItems = numberOfItems;
    },
  },
});
