<template>
  <div class="batch-container">
    <h1>Enter Batch Information</h1>
    <form @submit.prevent="submitBatch" class="batch-form">
      <div class="form-group">
        <label for="batchNumber">Batch Number/Receiving Lot:</label>
        <input v-model="batchNumber" id="batchNumber" required />
      </div>
      <div class="form-group">
        <label for="numberOfItems">Number of Items:</label>
        <input type="number" v-model.number="numberOfItems" id="numberOfItems" required />
      </div>
      <div class="form-group">
        <label for="partNumber">Part Number:</label>
        <input type="string" v-model="partNumber" id="partNumber" required />
      </div>
      <button type="submit" class="btn-primary">Start Scanning</button>
    </form>
  </div>
</template>

<script>
import { useBatchStore } from '../stores/batchStore';
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue'; 

export default {
  setup() {
    const batchStore = useBatchStore();
    const router = useRouter();
    const batchNumber = ref('');
    const numberOfItems = ref(0);
    const partNumber = ref('');
    const existingBatchData = batchStore.getBatchData();

    const submitBatch = () => {
      if (batchNumber.value && numberOfItems.value > 0 && partNumber.value) {
        batchStore.setBatchData(batchNumber.value, numberOfItems.value, partNumber.value);
        router.push({ name: 'OCRScanning' });
      } else {
        alert('Please enter valid batch information.');
      }
    };

    const checkForExistingBatchData = () => {
      if (
        existingBatchData.batchNumber !== '' || 
        existingBatchData.numberOfItems > 0 || 
        existingBatchData.partNumber !== ''
      ) {
        const overwrite = confirm(
          'Existing batch data has been found. Are you sure you want to overwrite it?'
        );
        if (!overwrite) {
          // Prevent overwriting and reset the form to avoid accidental submission
          batchNumber.value = existingBatchData.batchNumber;
          numberOfItems.value = existingBatchData.numberOfItems;
          partNumber.value = existingBatchData.partNumber;
        }
      }
    };

    onMounted(() => {
      checkForExistingBatchData();
    });

    return {
      batchNumber,
      numberOfItems,
      partNumber,
      submitBatch,
    };
  },
};
</script>

<style scoped>
.batch-container {
  max-width: 500px;
  margin: auto;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.batch-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.btn-primary {
  background-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
