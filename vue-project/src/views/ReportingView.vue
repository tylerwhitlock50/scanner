<template>
    <div class="container">
      <h1 class="text-center mb-4">Serial Number Query</h1>
      
      <!-- Search Form -->
      <form @submit.prevent="fetchSerialNumbers">
        <div class="row">
          <!-- Batch ID -->
          <div class="col-md-4 mb-3">
            <label for="batchId">Batch ID</label>
            <input type="text" v-model="filters.batch_id" class="form-control" id="batchId">
          </div>
          <!-- Part ID -->
          <div class="col-md-4 mb-3">
            <label for="partId">Part ID</label>
            <input type="text" v-model="filters.part_id" class="form-control" id="partId">
          </div>
          <!-- Serial Number -->
          <div class="col-md-4 mb-3">
            <label for="verifiedSn">Serial Number</label>
            <input type="text" v-model="filters.verified_sn" class="form-control" id="verifiedSn">
          </div>
        </div>
        <div class="row">
          <!-- Start Date -->
          <div class="col-md-4 mb-3">
            <label for="startDate">Start Date</label>
            <input type="date" v-model="filters.start_date" class="form-control" id="startDate">
          </div>
          <!-- End Date -->
          <div class="col-md-4 mb-3">
            <label for="endDate">End Date</label>
            <input type="date" v-model="filters.end_date" class="form-control" id="endDate">
          </div>
          <!-- Recorded SN -->
          <div class="col-md-4 mb-3">
            <label for="recordedSn">Recorded SN</label>
            <select v-model="filters.recorded_sn" class="form-control" id="recordedSn">
              <option value="">Any</option>
              <option value="true">True</option>
              <option value="false">False</option>
            </select>
          </div>
        </div>
        <!-- Add more fields as needed -->
        <button type="submit" class="btn btn-primary">Search</button>
      </form>
  
      <!-- Results Table -->
      <div class="table-responsive mt-4" v-if="serialNumbers.length > 0">
        <table class="table table-striped">
          <thead>
            <tr>
              <!-- Table Headers -->
              <th scope="col">ID</th>
              <th scope="col">Batch ID</th>
              <th scope="col">Part ID</th>
              <th scope="col">Serial Number</th>
              <th scope="col">OCR Timestamp</th>
              <th scope="col">Recorded SN</th>
              <!-- Add more columns as needed -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="sn in serialNumbers" :key="sn.id">
              <!-- Table Data -->
              <td>{{ sn.id }}</td>
              <td>{{ sn.batch_id }}</td>
              <td>{{ sn.part_id }}</td>
              <td>{{ sn.verified_sn }}</td>
              <td>{{ formatDate(sn.ocr_timestamp) }}</td>
              <td>{{ sn.recorded_sn ? 'True' : 'False' }}</td>
              <!-- Add more data as needed -->
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="mt-4">
        <p>No results found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import api from '../services/api';
  
  export default {
    setup() {
      const filters = ref({
        batch_id: '',
        part_id: '',
        verified_sn: '',
        start_date: '',
        end_date: '',
        recorded_sn: '',
        // Add more filters as needed
      });
  
      const serialNumbers = ref([]);
  
      const fetchSerialNumbers = async () => {
        try {
          // Build query parameters
          const params = {};
          for (const key in filters.value) {
            if (filters.value[key]) {
              params[key] = filters.value[key];
            }
          }
  
          const response = await api.get('/serial_numbers/query_v2', { params });
          serialNumbers.value = response.data.data;
        } catch (error) {
          console.error('Error fetching serial numbers:', error);
        }
      };
  
      const formatDate = (dateString) => {
        if (!dateString) return '';
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      };
  
      return {
        filters,
        serialNumbers,
        fetchSerialNumbers,
        formatDate,
      };
    },
  };
  </script>
  
  <style scoped>
  /* Keep styling consistent with your existing pages */
  .container {
    max-width: 960px;
    margin: auto;
  }
  
  .text-center {
    text-align: center;
  }
  
  .mb-3 {
    margin-bottom: 1rem;
  }
  
  .mt-4 {
    margin-top: 1.5rem;
  }
  </style>
  