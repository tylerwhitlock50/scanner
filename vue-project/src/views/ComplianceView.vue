<template>
  <div class="container">
    <h1 class="text-center mb-4">Unrecorded Serial Numbers</h1>

    <!-- Pagination and Sort Controls -->
    <div class="row mb-3">
      <div class="col-md-6">
        <label for="perPage">Items per Page:</label>
        <select id="perPage" v-model="perPage" @change="fetchSerialNumbers">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </div>
      <div class="col-md-6 text-right">
        <label for="sortBy">Sort By:</label>
        <select id="sortBy" v-model="sortBy" @change="fetchSerialNumbers">
          <option value="verified_sn">Serial Number</option>
          <option value="recorded_sn">Recorded Status</option>
          <option value="part_id">Part ID</option>
        </select>

        <button @click="toggleSortOrder">
          Sort: {{ sortOrder === 'asc' ? 'Ascending' : 'Descending' }}
        </button>
      </div>
    </div>

    <!-- Serial Numbers Table -->
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
              <button class="btn btn-sm btn-primary mb-1" @click="markAsRecorded(serialNumber)">
                Mark as Recorded
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Controls -->
    <div class="pagination-controls">
      <button :disabled="currentPage === 1" @click="currentPage--; fetchSerialNumbers()">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++; fetchSerialNumbers()">Next</button>
    </div>

    <button class="btn btn-primary mt-3" @click="markSelectedAsRecorded">Mark Selected as Recorded</button>
    <button class="btn btn-secondary mt-3 ml-2" @click="downloadCsv">Download Current Page CSV</button>
    <button class="btn btn-secondary mt-3 ml-2" @click="downloadAllUnrecordedCsv">Download All Unrecorded CSV</button>
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
    const currentPage = ref(1);
    const perPage = ref(20);
    const sortBy = ref('verified_sn');
    const sortOrder = ref('asc');
    const totalPages = ref(1);

    // Fetch serial numbers with pagination, sorting, and filtering
    const fetchSerialNumbers = async () => {
      try {
        const response = await api.get('/serial_numbers/query_v2', {
          params: {
            recorded_sn: false,
            page: currentPage.value,
            per_page: perPage.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value
          }
        });

        serialNumbers.value = response.data.data;
        totalPages.value = response.data.pages;
      } catch (error) {
        console.error('Error fetching serial numbers:', error);
      }
    };

    // Toggle sorting order
    const toggleSortOrder = () => {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
      fetchSerialNumbers();
    };

    // Download CSV for current page data
    const downloadCsv = () => {
      const headers = "ID,Serial Number,Recorded Status,Part ID\n";
      const csvContent = "data:text/csv;charset=utf-8,"
        + headers
        + serialNumbers.value.map(sn => `${sn.id},${sn.verified_sn},${sn.recorded_sn},${sn.part_id}`).join("\n");

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "unrecorded_serial_numbers_current_page.csv");
      document.body.appendChild(link);
      link.click();
    };

    // Download CSV for all unrecorded serial numbers
    const downloadAllUnrecordedCsv = async () => {
      try {
        const response = await api.get('/serial_numbers/query_v2', {
          params: {
            recorded_sn: false,
            page: 1,
            per_page: 10000, // Adjust per_page as necessary, or use pagination to fetch all records
            sort_by: sortBy.value,
            sort_order: sortOrder.value
          }
        });

        const allSerialNumbers = response.data.data;
        const headers = "ID,Serial Number,Recorded Status,Part ID\n";
        const csvContent = "data:text/csv;charset=utf-8,"
          + headers
          + allSerialNumbers.map(sn => `${sn.id},${sn.verified_sn},${sn.recorded_sn},${sn.part_id}`).join("\n");

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "unrecorded_serial_numbers_all.csv");
        document.body.appendChild(link);
        link.click();
      } catch (error) {
        console.error('Error fetching all unrecorded serial numbers:', error);
      }
    };

    // Toggle select all checkboxes
    const toggleSelectAll = () => {
      if (selectAll.value) {
        selectedSerialNumbers.value = serialNumbers.value.map(sn => sn.id);
      } else {
        selectedSerialNumbers.value = [];
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

    onMounted(() => {
      fetchSerialNumbers();
    });

    return {
      serialNumbers,
      selectedSerialNumbers,
      selectAll,
      currentPage,
      perPage,
      sortBy,
      sortOrder,
      totalPages,
      fetchSerialNumbers,
      downloadCsv,
      downloadAllUnrecordedCsv,
      toggleSelectAll,
      toggleSortOrder,
      markAsRecorded,
      markSelectedAsRecorded
    };
  }
};
</script>



<style scoped>
.container {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

label {
  font-weight: 500;
  margin-right: 10px;
}

select {
  padding: 8px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  background-color: #fff;
  font-size: 1rem;
  color: #495057;
  outline: none;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

select:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}


.pagination-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}



input[type="checkbox"] {
  width: 20px;
  height: 20px;
}
</style>
