import { defineStore } from 'pinia';

export const useSerialNumberStore = defineStore('serialNumbers', {
  state: () => ({
    serialNumbers: [],
  }),
  actions: {
    addSerialNumber(serialNumber) {
      this.serialNumbers.push(serialNumber);
    },
    setSerialNumbers(serialNumbers) {
      this.serialNumbers = serialNumbers;
    },
  },
});
