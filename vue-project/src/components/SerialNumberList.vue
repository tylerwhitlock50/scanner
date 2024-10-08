<template>
    <div>
      <h2>Scanned Serial Numbers</h2>
      <ul>
        <li v-for="serialNumber in serialNumbers" :key="serialNumber.id">
          {{ serialNumber.serial_number_extracted }} - Testing Selected: {{ serialNumber.testing_selected }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      serialNumbers: {
        type: Array,
        required: true,
      },
    },
  };
  </script>
  