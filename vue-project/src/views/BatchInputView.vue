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
          <option value="Purchase">Purchase</option>
          <option value="Production">Production</option>
          <option value="Sale">Sale</option>
          <option value="Return">Return</option>
          <option value="Transfer">Transfer</option>
          <option value="Destruction">Destruction</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Batch Description Textarea -->
      <div class="form-group">
        <label for="batchDescription">Batch Description:</label>
        <textarea v-model="batchDescription" id="batchDescription" rows="3"></textarea>
      </div>

      <button type="submit" class="btn-primary" :disabled="isLoading">
        {{ isLoading ? 'Processing...' : 'Start Scanning' }}
      </button>
    </form>
  </div>
</template>

<script>
import { useBatchStore } from '../stores/batchStore';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
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
    const isLoading = ref(false);
    const batchExists = ref(false);  // Track if the batch exists

    // Check if batch exists and update the store
    const checkBatchExists = async () => {
      if (!batchNumber.value) return;

      try {
        const response = await api.get('/batch', {
          params: { batch_number: batchNumber.value },
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
            // Pre-fill the form fields and update the store
            numberOfItems.value = data.batch_quantity || 0;
            partNumber.value = data.part_number || '';
            batchType.value = data.batch_type || 'Production';
            batchDescription.value = data.batch_description || '';

            // Set batch data in the store
            batchStore.setBatchData(
              batchNumber.value,
              numberOfItems.value,
              partNumber.value,
              batchType.value,
              batchDescription.value,
              data.batch_id
            );

            // Update the current count in the store
            batchStore.setCurrentCount(data.total_records);

            // Indicate that the batch exists and skip creation
            batchExists.value = true;

            // Redirect to the scanning page
            router.push({ name: 'OCRScanning' });
          } else {
            batchNumber.value = '';  // Clear the batch number if the user cancels
          }
        }
      } catch (error) {
        if (error.response && error.response.status === 404) {
          console.log('Batch not found, proceeding with new batch.');
          batchExists.value = false;  // Set batchExists to false if batch is not found
        } else {
          console.error('Error checking batch:', error);
          alert('An error occurred while checking the batch. Please try again.');
        }
      }
    };

    // Submit batch logic (creates new batch if it doesn't exist)
    const submitBatch = async () => {
      if (batchExists.value) {
        // If batch already exists, just go to the scanning page
        router.push({ name: 'OCRScanning' });
        return;
      }

      if (!batchNumber.value || numberOfItems.value <= 0 || !partNumber.value) {
        alert('Please enter valid batch information.');
        return;
      }

      isLoading.value = true;

      try {
        // Create a new batch if it doesn't exist
        const response = await api.post('/batch', {
          batch_number: batchNumber.value,
          number_of_items: numberOfItems.value,
          part_number: partNumber.value,
          batch_type: batchType.value,
          batch_description: batchDescription.value,
        });

        if (response.status === 201) {
          // Save batch data to the store
          batchStore.setBatchData(
            batchNumber.value,
            numberOfItems.value,
            partNumber.value,
            batchType.value,
            batchDescription.value,
            response.data.data.id
          );

          // Redirect to the scanning page
          router.push({ name: 'OCRScanning' });
        } else {
          alert('Batch creation failed. Please try again.');
        }
      } catch (error) {
        console.error('Error creating batch:', error);
        alert('An error occurred. Please try again.');
      } finally {
        isLoading.value = false;
      }
    };

    return {
      batchNumber,
      numberOfItems,
      partNumber,
      batchType,
      batchDescription,
      submitBatch,
      checkBatchExists,
      isLoading,
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
