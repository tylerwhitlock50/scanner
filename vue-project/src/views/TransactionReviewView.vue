<template>
  <div class="container">

    <h1 class="text-center mb-4">Transaction Review</h1>
    <div class="summary row mb-3">
      <div class="col-md-6">
        <p><strong>Batch ID:</strong> {{ batchId }}</p>
        <p><strong>Part ID:</strong> {{ partId }}</p>
        <p><strong>Batch Quantity:</strong> {{ batchQuantity }}</p>
        <p><strong>Total Serial Numbers Scanned:</strong> {{ totalSerialNumbers }}</p>
        <p><strong>Difference:</strong> {{ difference }}</p>
      </div>
      <div class="col-md-6 text-md-right">
        <button class="btn btn-primary mb-2" @click="downloadReport">Download Barcodes</button>
      </div>
    </div>
    <div class="table-responsive">
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
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-primary mt-3" @click="markSelectedAsReviewed">Mark Selected as Reviewed</button>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useBatchStore } from '../stores/batchStore';
import { useRouter } from 'vue-router';
import api from '../services/api';



export default {
  setup() {
    const serialNumbers = ref([]);
    const selectedSerialNumbers = ref([]);
    const selectAll = ref(false);
    const snackbar = ref(false);
    const snackbarMessage = ref('Please enter batch information first.');

    // Access the batch store
    const batchStore = useBatchStore();
    const router = useRouter();

    // Computed properties for batch information
    const batchId = computed(() => batchStore.batchData.batchNumber || 'N/A');
    const partId = computed(() => batchStore.batchData.partNumber || 'N/A');
    const batchQuantity = computed(() => batchStore.batchData.numberOfItems || 0);

    const totalSerialNumbers = computed(() => serialNumbers.value.length);

    // Define the difference computed property
    const difference = computed(() => {
      return batchQuantity.value - totalSerialNumbers.value;
    });

    // Function to check if batch data is empty
    const isBatchDataEmpty = () => {
      const batchData = batchStore.getBatchData();
      return (
        batchData.batchNumber === '' &&
        batchData.numberOfItems === 0 &&
        batchData.partNumber === ''
      );
    };

    const fetchSerialNumbers = async () => {
      try {
        const response = await api.get('/serial_numbers/query', {
          params: {
            batch_id: batchStore.batchData.batchNumber,
          },
        });
        serialNumbers.value = response.data.data.map(sn => ({
          ...sn,
          editing: false,
        }));
      } catch (error) {
        console.error('Error fetching serial numbers:', error);
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
        await api.put(`/serial_number/${serialNumber.id}`, {
          verified_sn: serialNumber.verified_sn,
        });
        serialNumber.editing = false;
      } catch (error) {
        console.error('Error updating serial number:', error);
      }
    };

    const markAsReviewed = async (serialNumber) => {
      try {
        await api.put(`/serial_number/${serialNumber.id}`, {
          is_verified: true,
        });
        serialNumber.is_verified = true;
      } catch (error) {
        console.error('Error updating serial number:', error);
      }
    };

    const markSelectedAsReviewed = async () => {
      try {
        await Promise.all(
          selectedSerialNumbers.value.map(id =>
            api.put(`/serial_number/${id}`, { is_verified: true })
          )
        );
        serialNumbers.value.forEach(sn => {
          if (selectedSerialNumbers.value.includes(sn.id)) {
            sn.is_verified = true;
          }
        });
        selectedSerialNumbers.value = [];
        selectAll.value = false;
      } catch (error) {
        console.error('Error updating serial numbers:', error);
      }
    };

    const downloadReport = async () => {
      try {
        const response = await api.get('/serial_numbers/report', {
          params: { batch_id: batchStore.batchData.batchNumber },
          responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `Batch_${batchStore.batchData.batchNumber}_Report.pdf`);
        document.body.appendChild(link);
        link.click();
      } catch (error) {
        console.error('Error downloading report:', error);
      }
    };

    // Show notification and redirect if batch data is missing
    const showNotification = (message, delay = 0) => {
      alert(message);
      setTimeout(() => {
        router.push({ name: 'BatchInput' }); // Redirect to batch input screen
      }, delay);
    };

    // Check batch data when component is mounted
    onMounted(() => {
      if (isBatchDataEmpty()) {
        showNotification('Please enter batch information first.');
        return;
      }
      fetchSerialNumbers();
    });

    return {
      serialNumbers,
      selectedSerialNumbers,
      selectAll,
      batchId,
      partId,
      batchQuantity,
      totalSerialNumbers,
      difference,
      toggleSelectAll,
      editSerialNumber,
      saveSerialNumber,
      markAsReviewed,
      markSelectedAsReviewed,
      downloadReport,
    };
  },
};
</script>

<style scoped>
.summary p {
  margin-bottom: 0.5rem;
}
</style>
