<template>
    <div class="ocr-container">
      <h1>OCR Scanning</h1>
  
      <div v-if="!imageCaptured" class="video-wrapper">
        <div class="video-container">
          <video ref="video" autoplay></video>
        </div>
        <button @click="captureImage" class="btn-primary">Capture Image</button>
      </div>
  
      <div v-if="imageCaptured" class="image-wrapper">
        <img :src="capturedImageUrl" alt="Captured Image" class="captured-image" />
        <button @click="sendImage" class="btn-primary">Send to OCR</button>
        <button @click="resetCapture" class="btn-secondary">Retake Image</button>
      </div>
  
      <canvas ref="canvas" width="640" height="480" style="display:none;"></canvas>
  
      <pre>{{ apiResponse }}</pre>
    </div>
  </template>
  
  <script>
  //import axios from 'axios';
  import api from '../services/api'; // Adjust the path as needed
  
  export default {
    data() {
      return {
        capturedImageUrl: null,
        imageCaptured: false,
        apiResponse: null,
        videoStreamReady: false,
        videoStream: null,
      };
    },
    async mounted() {
      await this.startWebcam();
    },
    methods: {
      async startWebcam() {
        try {
          if (this.videoStream) {
            this.videoStream.getTracks().forEach(track => track.stop());
          }
          const stream = await navigator.mediaDevices.getUserMedia({ video: true });
          this.$refs.video.srcObject = stream;
          this.videoStream = stream;
          this.videoStreamReady = true;
        } catch (err) {
          console.error('Error accessing the webcam: ', err);
        }
      },
      captureImage() {
        if (this.videoStreamReady) {
          const video = this.$refs.video;
          const canvas = this.$refs.canvas;
  
          if (canvas && canvas.getContext) {
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            this.capturedImageUrl = canvas.toDataURL('image/jpeg');
            this.imageCaptured = true;
  
            // Stop the video stream after capturing the image
            if (this.videoStream) {
              this.videoStream.getTracks().forEach(track => track.stop());
            }
          } else {
            console.error('Canvas element not found or not ready.');
          }
        } else {
          console.error('Video stream not ready.');
        }
      },
      resetCapture() {
        this.capturedImageUrl = null;
        this.imageCaptured = false;
        this.startWebcam();
      },
      async sendImage() {
        try {
          const canvas = this.$refs.canvas;
          const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg'));
          const formData = new FormData();
          formData.append('file', blob, 'captured_image.jpg');
  
          const response = await api.post('/upload', formData);
          this.apiResponse = response.data;
        } catch (error) {
          console.error('Error sending image to the API:', error);
        }
      },
    },
    destroyed() {
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
      }
    },
  };
  </script>
  
  <style scoped>
  .ocr-container {
    max-width: 500px;
    margin: 50px auto;
    padding: 20px;
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
    height: auto;
    border-radius: 8px;
    border: 1px solid #ccc;
  }
  
  .captured-image {
    width: 100%;
    max-width: 100%;
    border-radius: 8px;
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
  </style>
  