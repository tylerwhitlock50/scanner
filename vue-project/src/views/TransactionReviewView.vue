<template>
  <div class="container">
    <h1 class="text-center mb-4">Transaction Review</h1>

    <!-- Input to change batch number -->
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

    <!-- Display Batch Info -->
    <div class="summary row mb-3" v-if="batchInfo">
      <div class="col-md-6">
        <p><strong>Batch ID:</strong> {{ batchInfo.batchNumber }}</p>
        <p><strong>Part ID:</strong> {{ batchInfo.partNumber }}</p>
        <p><strong>Batch Quantity:</strong> {{ batchInfo.numberOfItems }}</p>
        <p><strong>Total Serial Numbers Scanned:</strong> {{ totalSerialNumbers }}</p>
        <p><strong>Difference:</strong> {{ difference }}</p>
      </div>
      <div class="col-md-6 text-md-right">
        <button class="btn btn-primary mb-2" @click="downloadReport">Download Barcodes</button>
      </div>
    </div>

    <!-- Table to Display Serial Numbers -->
    <div v-if="serialNumbers.length > 0" class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col" class="text-center">
              <input type="checkbox" v-model="selectAll" @change="toggleSelectAll">
            </th>
            <th scope="col">Serial Number</th>
            <th scope="col">Status</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(serialNumber, index) in serialNumbers" :key="serialNumber.id">
            <td class="text-center">
              <input type="checkbox" v-model="selectedSerialNumbers" :value="serialNumber.id">
            </td>
            <td>
              <span v-if="!serialNumber.editing">{{ serialNumber.verified_sn }}</span>
              <input
                v-else
                v-model="serialNumber.verified_sn"
                class="form-control form-control-sm"
              >
            </td>
            <td>{{ serialNumber.is_verified ? 'Verified' : 'Not Verified' }}</td>
            <td>
              <button
                class="btn btn-sm btn-secondary mr-1 mb-1"
                @click="editSerialNumber(serialNumber)"
                v-if="!serialNumber.editing"
              >Edit</button>
              <button
                class="btn btn-sm btn-success mr-1 mb-1"
                @click="saveSerialNumber(serialNumber)"
                v-else
              >Save</button>
              <button
                class="btn btn-sm btn-primary mb-1"
                @click="markAsReviewed(serialNumber)"
              >Confirm</button>
              <button class="btn btn-sm btn-danger mb-1" @click="deleteSerialNumber(serialNumber.id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- If No Serial Numbers Found -->
    <div v-else>
      <p>No serial numbers found for this batch.</p>
    </div>

    <div v-if="isLoading">Loading...</div>

    <!-- Mark Selected Serial Numbers as Reviewed -->
    <button class="btn btn-primary mt-3" @click="markSelectedAsReviewed" :disabled="selectedSerialNumbers.length === 0">
      Mark Selected as Reviewed
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';
import { useBatchStore } from '../stores/batchStore';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const batchStore = useBatchStore();
    const router = useRouter();
    const serialNumbers = ref([]);
    const selectedSerialNumbers = ref([]);
    const selectAll = ref(false);
    const isLoading = ref(false);

    // Input for changing batch number
    const batchNumberInput = ref(batchStore.getBatchData().batchNumber);

    const batchInfo = computed(() => batchStore.getBatchData());
    const totalSerialNumbers = computed(() => serialNumbers.value.length);
    const difference = computed(() => batchInfo.value.numberOfItems - totalSerialNumbers.value);

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
            data.batch_number,
            data.batch_quantity,
            data.part_number,
            data.batch_type,
            data.batch_description,
            data.id
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
      }
    };

    const toggleSelectAll = () => {
      if (selectAll.value) {
        selectedSerialNumbers.value = serialNumbers.value.map(sn => sn.id);
      } else {
        selectedSerialNumbers.value = [];
      }
    };

    const editSerialNumber = (serialNumber) => {
      serialNumber.editing = true;
    };

    const saveSerialNumber = async (serialNumber) => {
      try {
        await api.put(`/serial_number/${serialNumber.id}`, { verified_sn: serialNumber.verified_sn });
        serialNumber.editing = false;
      } catch (error) {
        console.error('Error updating serial number:', error);
      }
    };

    const markAsReviewed = async (serialNumber) => {
      try {
        await api.put(`/serial_number/${serialNumber.id}`, { is_verified: true });
        serialNumber.is_verified = true;
      } catch (error) {
        console.error('Error marking serial number as reviewed:', error);
      }
    };

    const deleteSerialNumber = async (id) => {
      const confirmed = confirm('Are you sure you want to delete this serial number?');
      if (!confirmed) return;

      try {
        await api.delete(`/serial_number/${id}`);
        serialNumbers.value = serialNumbers.value.filter(record => record.id !== id);
      } catch (error) {
        console.error('Error deleting serial number:', error);
      }
    };

    const markSelectedAsReviewed = async () => {
      try {
        await Promise.all(
          selectedSerialNumbers.value.map(id => api.put(`/serial_number/${id}`, { is_verified: true }))
        );
        serialNumbers.value.forEach(sn => {
          if (selectedSerialNumbers.value.includes(sn.id)) {
            sn.is_verified = true;
          }
        });
        selectedSerialNumbers.value = [];
        selectAll.value = false;
      } catch (error) {
        console.error('Error marking selected serial numbers as reviewed:', error);
      }
    };

    const downloadReport = async () => {
      try {
        const response = await api.get('/serial_numbers/report', {
          params: { batch_id: batchInfo.value.batchNumber },
          responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `Batch_${batchInfo.value.batchNumber}_Report.pdf`);
        document.body.appendChild(link);
        link.click();
      } catch (error) {
        console.error('Error downloading report:', error);
      }
    };

    onMounted(() => {
      // Fetch batch data immediately if batch number exists
      if (batchStore.getBatchData().batchNumber) {
        fetchBatchData();
      }
    });

    return {
      batchNumberInput,
      batchInfo,
      serialNumbers,
      selectedSerialNumbers,
      selectAll,
      totalSerialNumbers,
      difference,
      isLoading,
      toggleSelectAll,
      editSerialNumber,
      saveSerialNumber,
      markAsReviewed,
      markSelectedAsReviewed,
      deleteSerialNumber,
      downloadReport,
      fetchBatchData,
    };
  },
};
</script>

<style scoped>
.summary p {
  margin-bottom: 0.5rem;
}

.table-responsive {
  margin-top: 20px;
}

.table th, .table td {
  text-align: center;
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

.btn {
  padding: 8px 12px;
}

input[type="checkbox"] {
  cursor: pointer;
}
</style>
