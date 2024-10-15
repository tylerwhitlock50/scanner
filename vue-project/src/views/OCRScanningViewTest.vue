<!-- OCRScanning.vue -->
<template>

    <!-- Vuetify Snackbar for notifications -->
    <v-snackbar v-model="snackbar" :timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>

    <div class="batch-info">
    <p><strong>Batch Number:</strong> {{ batchStore.batchData.batchNumber }}</p>
    <p><strong>Item:</strong> {{ batchStore.batchData.currentCount + 1 }} of {{ batchStore.batchData.numberOfItems }}</p>
    <p><strong>Last Scanned Serial Number:</strong> {{ lastScannedSerialNumber }}</p>
  </div>

    <div class="ocr-container">
        <!-- Batch Information -->

      <div v-if="!imageCaptured" class="video-wrapper">
        <div class="video-container">
          <video ref="video" autoplay></video>
        </div>
        <v-btn color="primary" @click="captureImage">Capture Image</v-btn>
      </div>
  
      <div v-if="imageCaptured" class="image-wrapper">
        <img :src="capturedImageUrl" alt="Captured Image" class="captured-image" />
        <v-btn color="primary" @click="sendImage">Send to OCR</v-btn>
        <v-btn color="secondary" @click="resetCapture">Retake Image</v-btn>
      </div>
  
      <canvas ref="canvas" width="640" height="480" style="display:none;"></canvas>
  
      <!-- <pre>{{ apiResponse }}</pre> -->
    </div>
  
    <!-- Modal Dialog for Serial Number Confirmation -->
      <!-- Vuetify Dialog for Serial Number Confirmation -->
      <v-dialog v-model="showModal" max-width="400px">
  <v-card>
    <v-card-title>Confirm Serial Number</v-card-title>
    <v-card-text>
      <v-text-field
        label="Serial Number"
        v-model="serialNumber"
        outlined
        dense
      ></v-text-field>
      <v-checkbox
        label="Product Tested"
        v-model="tested"
        dense
      ></v-checkbox>
    </v-card-text>
    <v-card-actions class="d-flex flex-column">
      <!-- Stack buttons vertically -->
      <v-btn color="primary" class="mb-2" @click="submitData">Submit</v-btn>
      <v-btn color="secondary" @click="closeModal">Cancel</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>



 

  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import { useBatchStore } from '../stores/batchStore';
  import { useRouter } from 'vue-router';
  import api from '../services/api';
  //import { VSnackbar } from 'vuetify/lib/components/index.mjs';
  import {
  VSnackbar,
  VDialog,
  VCard,
  VCardTitle,
  VCardText,
  VCardActions,
  VBtn,
  VCheckbox,
  VTextField,
  VSpacer,
} from 'vuetify/lib/components/index.mjs';
  
  const capturedImageUrl = ref(null);
  const imageCaptured = ref(false);
  const apiResponse = ref(null);
  const videoStreamReady = ref(false);
  const videoStream = ref(null);
  const showModal = ref(false);
  const serialNumber = ref('');
  const tested = ref(false);

  const snackbar = ref(false);
  const snackbarMessage = ref('Please Ensure That Batch Information is Entered First'); 
  
  const video = ref(null);
  const canvas = ref(null);
  
  const batchStore = useBatchStore();
  const lastScannedSerialNumber = ref('None');
  const router = useRouter();

  const isBatchDataEmpty = () => {
  const batchData = batchStore.getBatchData();
  
  // Check if the batchData matches the default values
  return (
    batchData.batchNumber === '' &&
    batchData.numberOfItems === 0 &&
    batchData.partNumber === ''
  );
};
  
  const startWebcam = async () => {
    try {
      if (videoStream.value) {
        videoStream.value.getTracks().forEach((track) => track.stop());
      }
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.value.srcObject = stream;
      videoStream.value = stream;
      videoStreamReady.value = true;
    } catch (err) {
      console.error('Error accessing the webcam: ', err);
    }
  };
  
  const captureImage = () => {
    if (videoStreamReady.value) {
      if (canvas.value && canvas.value.getContext) {
        const context = canvas.value.getContext('2d');
        context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height);
        capturedImageUrl.value = canvas.value.toDataURL('image/jpeg');
        imageCaptured.value = true;
        // Stop the video stream after capturing the image
        if (videoStream.value) {
          videoStream.value.getTracks().forEach((track) => track.stop());
        }
      } else {
        console.error('Canvas element not found or not ready.');
      }
    } else {
      console.error('Video stream not ready.');
    }
  };
  
  const resetCapture = () => {
    capturedImageUrl.value = null;
    imageCaptured.value = false;
    startWebcam();
  };
  
  const sendImage = async () => {
    try {
      const blob = await new Promise((resolve) => canvas.value.toBlob(resolve, 'image/jpeg'));
      const formData = new FormData();
      formData.append('file', blob, 'captured_image.jpg');
  
      const response = await api.post('/upload', formData);
      apiResponse.value = response.data;
      serialNumber.value = response.data.serial_number_extracted || '';
      showModal.value = true;
      console.log('Modal triggered'); 
    } catch (error) {
      console.error('Error sending image to the API:', error);
    }
  };
  
  const submitData = () => {
    const batchData = batchStore.getBatchData();
    const dataToSubmit = {
    // OCR-related fields
    ocr_detected_text: apiResponse.value.ocr_detected_text || '',
    image_file_name: apiResponse.value.image_file_name || '',
    image_channels: apiResponse.value.image_metadata.image_channels || 3,
    image_format: apiResponse.value.image_metadata.image_format || 'jpeg',
    image_height: apiResponse.value.image_metadata.image_height || 480,
    image_size_bytes: apiResponse.value.image_metadata.image_size_bytes || 400,
    image_width: apiResponse.value.image_metadata.image_width || 640,
    ocr_language: apiResponse.value.ocr_language || 'eng',
    
    // Handle serial number: use the extracted serial number or a fallback value
    serial_number_extracted: apiResponse.value.serial_number_extracted || serialNumber.value,
    
    // Use the timestamp from the API response
    ocr_timestamp: apiResponse.value.ocr_timestamp || new Date().toISOString(),
    
    uploaded_by: 'operator', // Replace with actual operator ID if available
    ocr_status: 'confirmed',
    
    // Check if the serial number was corrected by the user
    is_ocr_corrected: apiResponse.value.serial_number_extracted !== serialNumber.value,

    // Batch information fields
    batch_id: batchData.batchNumber,
    batch_quantity: batchData.numberOfItems,
    batch_item_no: batchData.partNumber,
    part_id: batchData.partNumber,

    batch_type: batchData.batchType,
    batch_description: batchData.batchDescription,

    verified_sn: serialNumber.value,
    is_verified: false,

    // Testing-related fields
    testing_selected: tested.value,

    // Default values for other required fields
    //recorded_sn: false,
    //recorded_sn_timestamp: new Date().toISOString(),
    //recorded_sn_user: 'None', // Replace with actual operator ID if available
    sn_status_id: 'NewScan', // Set appropriate status ID
    batch_info_id: batchData.batch_info_id
  };
  
    api
      .post('/serial_number', dataToSubmit)
      .then((response) => {
        console.log('Serial number record created', response.data);
        closeModal();
        // Reset for the next item
        batchStore.incrementCurrentCount();
        lastScannedSerialNumber.value = dataToSubmit.verified_sn;

        if (batchStore.batchData.currentCount >= batchStore.batchData.numberOfItems) {
          showNotification('Batch completed. Redirecting to Batch Review page...', 3000);
          router.push({ name: 'TransactionReviewView' });
        } else {
          resetCapture();
        }
        resetCapture();
      })
      .catch((error) => {
        console.error('Error submitting data to API:', error);
      });
  };
  
  const closeModal = () => {
    showModal.value = false;
  };



  const showNotification = (message, delay=0) => {
    //snackbarMessage.value = message;
    //snackbar.value = true;
    // Delay the redirection by `delay` milliseconds (default is 3000ms = 3 seconds)
    alert(message);
  // setTimeout(() => {
  //   router.push({ name: 'BatchInput' });  // Redirect to batch input route after the delay
  // }, delay);
  };


  
  onMounted(() => {
    if (isBatchDataEmpty()) {
        showNotification('Please enter batch information first.');
        router.push({ name: 'BatchInput' });  // Redirect to batch input route after the delay
    return;
  }
  if (batchStore.batchData.currentCount >= batchStore.batchData.numberOfItems) {
    showNotification('Batch scanning is complete. Redirecting to Batch Review page...');
    router.push({ name: 'TransactionReviewView' });
    return;
  }
    startWebcam();
  });
  
  onBeforeUnmount(() => {
    if (videoStream.value) {
      videoStream.value.getTracks().forEach((track) => track.stop());
    }
  });
  </script>
  
  <style scoped>
  /* Existing styles */
  
  .ocr-container {
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

.video-wrapper,
.image-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.video-container {
  width: 100%;
  max-width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

video {
  width: 100%;
  max-width: 100%;
  height: auto;
  border-radius: 1rem;
  border: 1px solid #ccc;
}

.captured-image {
  width: 100%;
  max-width: 100%;
  border-radius: 1rem;
  border: 1px solid #ccc;
  margin-bottom: 1rem;
}

button {
  width: 100%;
  padding: 12px;
  margin-bottom: 10px;
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

.btn-secondary {
  background-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

pre {
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 4px;
  font-size: 14px;
}

@media (max-width: 768px) {
  .ocr-container {
    max-width: 100%;
    padding: 15px;
  }

  video,
  canvas {
    width: 100%;
    height: auto;
  }

  .captured-image {
    width: 100%;
  }
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Make sure modal overlay is on top of all other content */
  visibility: visible;
  opacity: 1;
}

.modal {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  height: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: left;
  width: 90%;
  max-width: 400px;
  z-index: 10000; /* Ensure the modal content is on top of the overlay */
  visibility: visible;
  opacity: 1;
  color: #000;
  position: relative;
}

.modal h2 {
  margin-top: 0;
}

.modal .form-group {
  margin-top: 15px;
}

.modal input[type='text'] {
  width: 100%;
  padding: 8px;
  margin-top: 8px;
  box-sizing: border-box;
}

.modal button {
  margin-top: 15px;
  width: 100%;
}
.batch-info {
  background-color: #fff;
  padding: 2px;
  margin-bottom: 10px;
  border-radius: 8px;
  text-align: left;
}

.batch-info p {
  margin: 5px 0;
  font-size: 10px;
}

.v-selection-control__input input {
    CONTAIN-INTRINSIC-BLOCK-SIZE: auto none;
    cursor: pointer;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    opacity: .75 !important;
}
  </style>
  