<template>
  <div class="batch-container">
    <h1>Enter Batch Information</h1>
    <form @submit.prevent="submitBatch" class="batch-form">
      <div class="form-group">
        <label for="batchNumber">Batch Number/Receiving Lot:</label>
        <input v-model="batchNumber" id="batchNumber" required @blur="checkBatchExists" />
      </div>

      <div class="form-group">
        <label for="numberOfItems">Number of Items:</label>
        <input type="number" v-model.number="numberOfItems" id="numberOfItems" required />
      </div>

      <div class="form-group">
        <label for="partNumber">Part Number:</label>
        <input type="text" v-model="partNumber" id="partNumber" required />
      </div>

      <!-- Batch Type Dropdown -->
      <div class="form-group">
        <label for="batchType">Batch Type:</label>
        <select v-model="batchType" id="batchType" required>
          <option value="Production">Production</option>
          <option value="Receiving">Receiving</option>
          <option value="Outbound">Outbound</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Batch Description Textarea -->
      <div class="form-group">
        <label for="batchDescription">Batch Description:</label>
        <textarea v-model="batchDescription" id="batchDescription" rows="3"></textarea>
      </div>

      <button type="submit" class="btn-primary">Start Scanning</button>
    </form>
  </div>
</template>

<script>
import { useBatchStore } from '../stores/batchStore';
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import api from '../services/api';

export default {
  setup() {
    const batchStore = useBatchStore();
    const router = useRouter();
    
    // Form fields
    const batchNumber = ref('');
    const numberOfItems = ref(0);
    const partNumber = ref('');
    const batchType = ref('Production'); // Default value
    const batchDescription = ref('');

    const submitBatch = () => {
      if (batchNumber.value && numberOfItems.value > 0 && partNumber.value) {
        // Set batch data in the store, including the new fields
        batchStore.setBatchData(
          batchNumber.value,
          numberOfItems.value,
          partNumber.value,
          batchType.value,
          batchDescription.value
        );
        router.push({ name: 'OCRScanning' });
      } else {
        alert('Please enter valid batch information.');
      }
    };

    const checkBatchExists = async () => {
      if (!batchNumber.value) {
        return;
      }

      try {
        const response = await api.get('/batch', {
          params: { batch_id: batchNumber.value },
        });
        if (response.status === 200) {
          const data = response.data;
          const overwrite = confirm(
            `Batch ${batchNumber.value} exists with ${data.total_records} records.\n` +
              `Part Number: ${data.part_number}\n` +
              `Batch Quantity: ${data.batch_quantity}\n\n` +
              `Do you want to load this batch?`
          );
          if (overwrite) {
            // Pre-fill the form fields
            numberOfItems.value = data.batch_quantity || 0;
            partNumber.value = data.part_number || '';
            // Add default values for new fields
            batchType.value = 'Production'; // Reset to default
            batchDescription.value = ''; // Reset description
            // Update the batch store
            batchStore.setBatchData(
              batchNumber.value,
              numberOfItems.value,
              partNumber.value,
              batchType.value,
              batchDescription.value
            );
            batchStore.setCurrentCount(data.total_records);
          } else {
            batchNumber.value = ''; // Clear batch number if user doesn't load the existing batch
          }
        }
      } catch (error) {
        if (error.response && error.response.status === 404) {
          console.log('Batch not found, proceeding with new batch.');
        } else {
          console.error('Error checking batch:', error);
          alert('An error occurred while checking the batch. Please try again.');
        }
      }
    };

    const checkForExistingBatchData = () => {
      const existingBatchData = batchStore.getBatchData();
      if (
        existingBatchData.batchNumber !== '' ||
        existingBatchData.numberOfItems > 0 ||
        existingBatchData.partNumber !== ''
      ) {
        const overwrite = confirm(
          'Existing batch data has been found in your session.\n' +
            'Do you want to load this data?'
        );
        if (overwrite) {
          batchNumber.value = existingBatchData.batchNumber;
          numberOfItems.value = existingBatchData.numberOfItems;
          partNumber.value = existingBatchData.partNumber;
          batchType.value = existingBatchData.batchType;
          batchDescription.value = existingBatchData.batch_description;
        } else {
          batchStore.setBatchData('', 0, '', batchStore.batchData.batchType, '');
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
      batchType,
      batchDescription,
      submitBatch,
      checkBatchExists,
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

input,
select,
textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  background-color: white;
}

input:focus,
select:focus,
textarea:focus {
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
