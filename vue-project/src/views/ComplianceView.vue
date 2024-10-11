<template>
    <div class="container">
      <h1 class="text-center mb-4">Unrecorded Serial Numbers</h1>
      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col" class="text-center">
                <input type="checkbox" v-model="selectAll" @change="toggleSelectAll">
              </th>
              <th scope="col">Serial Number</th>
              <th scope="col">Recorded Status</th>
              <th scope="col">Part ID</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(serialNumber, index) in serialNumbers" :key="serialNumber.id">
              <td class="text-center">
                <input type="checkbox" v-model="selectedSerialNumbers" :value="serialNumber.id">
              </td>
              <td>{{ serialNumber.verified_sn }}</td>
              <td>{{ serialNumber.recorded_sn ? 'Recorded' : 'Not Recorded' }}</td>
              <td>{{ serialNumber.part_id }}</td>
              <td>
                <button
                  class="btn btn-sm btn-primary mb-1"
                  @click="markAsRecorded(serialNumber)"
                >Mark as Recorded</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button class="btn btn-primary mt-3" @click="markSelectedAsRecorded">Mark Selected as Recorded</button>
      <button class="btn btn-secondary mt-3 ml-2" @click="downloadCsv">Download CSV</button>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import api from '../services/api';
  
  export default {
    setup() {
      const serialNumbers = ref([]);
      const selectedSerialNumbers = ref([]);
      const selectAll = ref(false);
  
      // Fetch serial numbers with recorded_sn = false
      const fetchSerialNumbers = async () => {
        try {
          const response = await api.get('/serial_numbers/query', 
            { params: { recorded_sn: false } }
          );
          
          serialNumbers.value = response.data.data;
        } catch (error) {
          console.error('Error fetching serial numbers:', error);
        }
      };
  
      // Mark as Recorded
      const markAsRecorded = async (serialNumber) => {
        try {
          await api.put(`/serial_number/${serialNumber.id}`, {
            recorded_sn: true,
            recorded_sn_timestamp: new Date(),
            recorded_sn_user: 'Current User' // Update with actual user data
          });
          serialNumber.recorded_sn = true;
        } catch (error) {
          console.error('Error updating serial number:', error);
        }
      };
  
      // Mark selected items as Recorded
      const markSelectedAsRecorded = async () => {
        try {
          await Promise.all(
            selectedSerialNumbers.value.map(id =>
              api.put(`/serial_number/${id}`, { 
                recorded_sn: true, 
                recorded_sn_timestamp: new Date(),
                recorded_sn_user: 'Current User' 
              })
            )
          );
          serialNumbers.value.forEach(sn => {
            if (selectedSerialNumbers.value.includes(sn.id)) {
              sn.recorded_sn = true;
            }
          });
          selectedSerialNumbers.value = [];
          selectAll.value = false;
        } catch (error) {
          console.error('Error updating serial numbers:', error);
        }
      };
  
      // CSV download
      const downloadCsv = () => {
  const headers = "ID,Serial Number,Recorded Status,Part ID\n";
  const csvContent = "data:text/csv;charset=utf-8,"
    + headers
    + serialNumbers.value.map(sn => `${sn.id},${sn.verified_sn},${sn.recorded_sn},${sn.part_id}`).join("\n");

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "unrecorded_serial_numbers.csv");
  document.body.appendChild(link);
  link.click();
};

  
      const toggleSelectAll = () => {
        if (selectAll.value) {
          selectedSerialNumbers.value = serialNumbers.value.map(sn => sn.id);
        } else {
          selectedSerialNumbers.value = [];
        }
      };
  
      onMounted(() => {
        fetchSerialNumbers();
      });
  
      return {
        serialNumbers,
        selectedSerialNumbers,
        selectAll,
        markAsRecorded,
        markSelectedAsRecorded,
        downloadCsv,
        toggleSelectAll
      };
    }
  };
  </script>
  
  <style scoped>
  /* Add any styling here */
  </style>
  