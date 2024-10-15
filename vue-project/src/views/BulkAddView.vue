<template>
    <div class="container">
      <h1 class="text-center mb-4">Bulk Add Serial Numbers</h1>
      <p>Generating Serial number may take a minute, please be patient and do not reload the page until the transaction is completed.</p>
  
      <!-- Batch Information -->
      <div v-if="!batchEmpty" class="batch-info">
        <p><strong>Batch Number:</strong> {{ batchStore.batchData.batchNumber }}</p>
        <p><strong>Part Number:</strong> {{ batchStore.batchData.partNumber }}</p>
        <p><strong>Batch Quantity:</strong> {{ batchStore.batchData.numberOfItems }}</p>
      </div>
  
      <div v-if="batchEmpty" class="alert alert-danger mt-3">
        Please load batch information before proceeding.
      </div>

      <div v-if="batchEmpty" class="alert alert-danger mt-3">
        <div class="form-group mb-3">
      <label for="batchNumber">Change Batch Number:</label>
      <input
        type="text"
        v-model="batchNumberInput"
        id="batchNumber"
        class="form-control"
      />
      <button class="btn btn-primary mt-2" @click="fetchBatchData">Fetch Batch Data</button>
    </div>
      </div>
  
      <!-- Serial Number Input -->
      <div class="form-group mt-3">
        <label for="prefix">Serial Number Prefix:</label>
        <input type="text" v-model="prefix" id="prefix" class="form-control" placeholder="e.g., CV1025" />
      </div>
  
      <div class="form-group">
        <label for="startingValue">Starting Value:</label>
        <input type="number" v-model.number="startingValue" id="startingValue" class="form-control" placeholder="e.g., 1" />
      </div>
  
      <div class="form-group">
        <label for="digits">Number of Digits:</label>
        <input type="number" v-model.number="digits" id="digits" class="form-control" placeholder="e.g., 5" />
      </div>
  
      <div class="form-group">
        <label for="count">Number of Serial Numbers to Generate:</label>
        <input type="number" v-model.number="count" id="count" class="form-control" placeholder="e.g., 200" />
      </div>
  
      <button class="btn btn-primary" @click="generateSerialNumbers" :disabled="batchEmpty">Generate Serial Numbers</button>
  
      <!-- Display First and Last Serial Numbers -->
      <div v-if="serialNumbers.length > 0" class="mt-4">
        <p><strong>First Serial Number:</strong> {{ serialNumbers[0] }}</p>
        <p><strong>Last Serial Number:</strong> {{ serialNumbers[serialNumbers.length - 1] }}</p>
      </div>
  
      <!-- Table to Display Generated Serial Numbers -->
      <div v-if="serialNumbers.length > 0" class="table-responsive mt-4">
        <h3>Generated Serial Numbers</h3>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Serial Number</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(serialNumber, index) in serialNumbers" :key="index">
              <td>{{ serialNumber }}</td>
              <td>
                <button class="btn btn-sm btn-danger" @click="removeSerialNumber(index)">Remove</button>
              </td>
            </tr>
          </tbody>
        </table>
  
        <!-- <div class="text-center mt-3" v-if="isLoading">
        <b-spinner label="Spinning"></b-spinner>
        <b-spinner variant="primary" type="grow" label="Spinning"></b-spinner>
      </div> -->
      <button class="btn btn-success mt-3" @click="createAllSerialNumbers" :disabled="isLoading">
  {{ isLoading ? 'Working...' : 'Create All Serial Numbers' }}
</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import api from '../services/api';
  import { useBatchStore } from '../stores/batchStore';
  import { useRouter } from 'vue-router';
  
  // Form variables
  const batchStore = useBatchStore();
  const router = useRouter();
  const batchEmpty = ref(false);
  const serialNumbers = ref([]);
  const isLoading = ref(false);

  const batchNumberInput = ref(batchStore.getBatchData().batchNumber);
  
  // Serial number generation variables
  const prefix = ref('');
  const startingValue = ref(1);
  const digits = ref(5);
  const count = ref(1);
  const progressValue = ref(0);
  
  // Check if batch information is available
  const checkBatchInformation = () => {
    const batchData = batchStore.getBatchData();
    if (!batchData.batchNumber || batchData.numberOfItems === 0 || !batchData.partNumber) {
      batchEmpty.value = true;
    } else {
      batchEmpty.value = false;
    }
  };

  const fetchBatchData = async () => {
      if (!batchNumberInput.value) {
        alert('Please enter a batch number.');
        return;
      }

      isLoading.value = true;
      try {
        const response = await api.get('/batch', { params: { batch_number: batchNumberInput.value } });
        if (response.status === 200) {
          const data = response.data;
          serialNumbers.value = data.records.map(record => ({
            ...record,
            editing: false,
          }));

          // Update batch store with new data
          batchStore.setBatchData(
                data.batch_number,        // batchNumber
                data.batch_quantity,      // numberOfItems
                data.part_number,         // partNumber
                data.batch_type,          // batchType
                data.batch_description,   // batchDescription
                data.batch_id             // batch_info_id
            );
        } else {
          serialNumbers.value = [];
          alert('Batch not found or an error occurred.');
        }
      } catch (error) {
        console.error('Error fetching batch data:', error);
        alert('An error occurred while fetching batch data.');
      } finally {
        isLoading.value = false;
        checkBatchInformation();
      }
    };
  
  // Generate serial numbers based on prefix, starting value, count, and number of digits
  const generateSerialNumbers = () => {
    serialNumbers.value = [];
    for (let i = 0; i < count.value; i++) {
      const serialNumber = `${prefix.value}${(startingValue.value + i).toString().padStart(digits.value, '0')}`;
      serialNumbers.value.push(serialNumber);
    }
  };
  
  // Remove a serial number from the list
  const removeSerialNumber = (index) => {
    serialNumbers.value.splice(index, 1);
  };
  
  // Submit all generated serial numbers to the API
  const createAllSerialNumbers = async () => {
    isLoading.value = true;
    try {
      const batchData = batchStore.getBatchData();
      const totalSerialNumbers = serialNumbers.value.length;
      
      // Reset progress
      progressValue.value = 0;
  
      const serialNumberObjects = serialNumbers.value.map(sn => ({
        serial_number_extracted: 'BULK ADDED',
        batch_id: batchData.batchNumber,
        batch_quantity: batchData.numberOfItems,
        batch_item_no: batchData.partNumber,
        part_id: batchData.partNumber,
        batch_type: batchData.batchType,
        batch_description: batchData.batchDescription,
        verified_sn: sn,
        is_verified: false,
        sn_status_id: '1',
        ocr_detected_text: 'Bulk Added',
        sn_status_id: 'NewScan',
        verified_sn: sn,
        batch_info_id: batchData.batch_info_id,
      }));
  
      // Submit the serial numbers in chunks and update the progress bar
      for (let i = 0; i < totalSerialNumbers; i++) {
        await api.post('/serial_number', serialNumberObjects[i]);
        progressValue.value = Math.floor(((i + 1) / totalSerialNumbers) * 100);
      }
  
      alert('Serial numbers created successfully!');
    } catch (error) {
      console.error('Error creating serial numbers:', error);
      alert('An error occurred while creating serial numbers.');
    }
    isLoading.value = false;
  };
  
  onMounted(() => {
    checkBatchInformation();
  });
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
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
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .table-responsive {
    margin-top: 20px;
  }
  
  button {
    padding: 8px 12px;
    margin: 4px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #007bff;
    color: white;
  }
  
  input,
  select,
  textarea {
    padding: 8px;
    margin: 10px 0;
    width: 100%;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .v-progress-linear {
    margin-top: 20px;
  }
  </style>
  