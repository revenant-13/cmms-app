<template>
  <div class="parts">
    <h1>Parts Inventory</h1>
    <div class="filters">
      <input v-model="filterPartNumber" placeholder="Filter by Part Number" @input="applyFilters" />
      <select v-model="filterStatus" @change="applyFilters">
        <option value="">All Statuses</option>
        <option value="Available">Available</option>
        <option value="Active">Active</option>
        <option value="Inactive">Inactive</option>
      </select>
      <select v-model="filterSupplier" @change="applyFilters">
        <option value="">All Suppliers</option>
        <option v-for="vendor in vendorList" :key="vendor.id" :value="vendor.id">
          {{ vendor.name }}
        </option>
      </select>
    </div>
    <div class="form">
      <h2>{{ editingPart ? 'Edit Part' : 'Add New Part' }}</h2>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <form @submit.prevent="savePart">
        <input v-model="newPart.part_number" placeholder="Part Number" required />
        <input v-model="newPart.part_name" placeholder="Part Name" required />
        <textarea v-model="newPart.description" placeholder="Description"></textarea>
        <input v-model="newPart.status" placeholder="Status" required />
        <select v-model="newPart.equipment" multiple>
          <option v-for="equip in equipmentList" :key="equip.id" :value="equip.id">
            {{ equip.name }}
          </option>
        </select>
        <select v-model="newPart.suppliers" multiple>
          <option v-for="vendor in vendorList" :key="vendor.id" :value="vendor.id">
            {{ vendor.name }}
          </option>
        </select>
        <button type="submit">{{ editingPart ? 'Update' : 'Add' }}</button>
        <button v-if="editingPart" type="button" @click="cancelEdit">Cancel</button>
      </form>
    </div>
    <table v-if="filteredParts.length">
      <thead>
        <tr>
          <th>Part Number</th>
          <th>Part Name</th>
          <th>Description</th>
          <th>Status</th>
          <th>Equipment</th>
          <th>Suppliers</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="part in filteredParts" :key="part.id">
          <td>{{ part.part_number }}</td>
          <td>{{ part.part_name }}</td>
          <td>{{ part.description || 'N/A' }}</td>
          <td>{{ part.status }}</td>
          <td>{{ part.equipment_details && part.equipment_details.length ? part.equipment_details.map(e => e.name).join(', ') : 'None' }}</td>
          <td>{{ part.supplier_details && part.supplier_details.length ? part.supplier_details.map(v => v.name).join(', ') : 'None' }}</td>
          <td>
            <button @click="editPart(part)">Edit</button>
            <button @click="deletePart(part.id)" class="delete-btn">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No parts found</p>
  </div>
</template>

<style scoped>
  .parts {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  .filters {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
  }
  .filters input, .filters select {
    padding: 8px;
    width: 200px;
  }
  .form {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  input, select, textarea, button {
    margin: 5px 0;
    padding: 8px;
    width: 100%;
    box-sizing: border-box;
  }
  textarea {
    height: 100px;
  }
  select[multiple] {
    height: 100px;
  }
  button {
    background-color: #42b983;
    color: white;
    border: none;
    cursor: pointer;
  }
  button:hover {
    background-color: #2c3e50;
  }
  .delete-btn {
    background-color: #e74c3c;
    margin-left: 5px;
  }
  .delete-btn:hover {
    background-color: #c0392b;
  }
  .error {
    color: red;
    margin-bottom: 10px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #f2f2f2;
  }
  tr:nth-child(even) {
    background-color: #f9f9f9;
  }
</style>

<script>
import axios from 'axios'

export default {
  name: 'PartsPage',
  data() {
    return {
      parts: [],
      filteredParts: [],
      equipmentList: [],
      vendorList: [],
      csrfToken: null,
      filterPartNumber: '',
      filterStatus: '',
      filterSupplier: '',
      newPart: {
        part_number: '',
        part_name: '',
        description: '',
        status: '',
        equipment: [],
        suppliers: []
      },
      editingPart: null,
      errorMessage: ''
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => {
      this.fetchEquipment()
      this.fetchVendors()
      this.fetchParts()
    })
  },
  methods: {
    async fetchCsrfToken() {
      try {
        await axios.get('http://localhost:8000/api/parts/', { withCredentials: true })
        this.csrfToken = this.getCsrfToken()
      } catch (error) {
        console.error('Error fetching CSRF token:', error)
      }
    },
    fetchParts() {
      axios.get('http://localhost:8000/api/parts/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.parts = response.data
          this.applyFilters()
        })
        .catch(error => {
          console.error('Error fetching parts:', error)
        })
    },
    fetchEquipment() {
      axios.get('http://localhost:8000/api/equipment/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.equipmentList = response.data
        })
        .catch(error => {
          console.error('Error fetching equipment:', error)
        })
    },
    fetchVendors() {
      axios.get('http://localhost:8000/api/vendors/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.vendorList = response.data
        })
        .catch(error => {
          console.error('Error fetching vendors:', error)
        })
    },
    applyFilters() {
      this.filteredParts = this.parts.filter(part => {
        const matchesPartNumber = this.filterPartNumber ? 
          part.part_number.toLowerCase().includes(this.filterPartNumber.toLowerCase()) : true
        const matchesStatus = this.filterStatus ? 
          part.status === this.filterStatus : true
        const matchesSupplier = this.filterSupplier ? 
          part.supplier_details && part.supplier_details.some(v => v.id === parseInt(this.filterSupplier)) : true
        return matchesPartNumber && matchesStatus && matchesSupplier
      })
    },
    async savePart() {
      this.errorMessage = ''
      try {
        await this.fetchCsrfToken()
        const partData = { ...this.newPart }
        console.log('Sending part data:', partData)
        if (!partData.equipment.length) delete partData.equipment
        if (!partData.suppliers.length) delete partData.suppliers

        if (this.editingPart) {
          const response = await axios.put(`http://localhost:8000/api/parts/${this.editingPart.id}/`, partData, {
            withCredentials: true,
            headers: { 'X-CSRFToken': this.csrfToken }
          }).catch(error => {
            if (error.response && error.response.status === 400) {
              throw { response: error.response }
            }
            throw error
          })
          console.log('PUT response:', response.data)
        } else {
          await axios.post('http://localhost:8000/api/parts/', partData, {
            withCredentials: true,
            headers: { 'X-CSRFToken': this.csrfToken }
          })
        }
        this.fetchParts()
        this.resetForm()
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errorMessage = error.response.data.detail || 'Invalid part data.'
        } else {
          console.error('Error saving part:', error)
          this.errorMessage = 'Failed to save part. Please try again.'
        }
      }
    },
    async deletePart(partId) {
      if (confirm('Are you sure you want to delete this part?')) {
        try {
          await this.fetchCsrfToken()
          await axios.delete(`http://localhost:8000/api/parts/${partId}/`, {
            withCredentials: true,
            headers: { 'X-CSRFToken': this.csrfToken }
          })
          this.fetchParts()
        } catch (error) {
          console.error('Error deleting part:', error)
          this.errorMessage = 'Failed to delete part. Please try again.'
        }
      }
    },
    editPart(part) {
      this.editingPart = part
      this.newPart = {
        part_number: part.part_number,
        part_name: part.part_name,
        description: part.description || '',
        status: part.status,
        equipment: part.equipment_details ? part.equipment_details.map(e => e.id) : [],
        suppliers: part.supplier_details ? part.supplier_details.map(v => v.id) : []
      }
    },
    resetForm() {
      this.newPart = { part_number: '', part_name: '', description: '', status: '', equipment: [], suppliers: [] }
      this.editingPart = null
      this.errorMessage = ''
    },
    getCsrfToken() {
      const name = 'csrftoken'
      let cookieValue = null
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    }
  }
}
</script>