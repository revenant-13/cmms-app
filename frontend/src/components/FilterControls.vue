<template>
    <div class="filters">
      <input v-model="localSearchQuery" placeholder="Search by Name" @input="$emit('update:searchQuery', $event.target.value)" />
      <select v-model="localFilterLocation" @change="$emit('update:filterLocation', $event.target.value)">
        <option value="">All Locations</option>
        <option value="in-house">In-House</option>
        <option value="off-site">Off-Site</option>
      </select>
      <select v-model="localFilterManufacturer" @change="$emit('update:filterManufacturer', $event.target.value)">
        <option value="">All Manufacturers</option>
        <option v-for="vendor in vendors" :key="vendor.id" :value="vendor.id">
          {{ vendor.name }}
        </option>
      </select>
    </div>
  </template>
  
  <script>
  import { ref, watch } from 'vue'
  
  export default {
    name: 'FilterControls',
    props: {
      searchQuery: String,
      filterLocation: String,
      filterManufacturer: String,
      vendors: Array
    },
    setup(props, { emit }) {
      const localSearchQuery = ref(props.searchQuery)
      const localFilterLocation = ref(props.filterLocation)
      const localFilterManufacturer = ref(props.filterManufacturer)
  
      watch([localSearchQuery, localFilterLocation, localFilterManufacturer], ([sq, fl, fm]) => {
        emit('update:searchQuery', sq)
        emit('update:filterLocation', fl)
        emit('update:filterManufacturer', fm)
      })
  
      return { localSearchQuery, localFilterLocation, localFilterManufacturer }
    }
  }
  </script>
  
  <style scoped>
  .filters {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
  }
  input, select {
    padding: 8px;
    width: 200px;
  }
  </style>