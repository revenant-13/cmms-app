<template>
  <div class="equipment">
    <div class="header">
      <h1>Equipment Hierarchy</h1>
      <div class="header-buttons">
        <button @click="toggleForm" class="toggle-btn">
          {{ showForm ? 'Hide Form' : 'Add Equipment' }}
        </button>
        <button @click="toggleView" class="view-btn">
          {{ showHierarchy ? 'View Table' : 'View Hierarchy' }}
        </button>
      </div>
    </div>
    <equipment-form
      v-if="showForm"
      :equipment="editingEquipment"
      :equipment-list="flattenedEquipment"
      :vendor-list="vendorList"
      :error="errorMessage"
      @save="saveEquipment"
      @cancel="cancelEdit"
    />
    <div class="controls">
      <filter-controls
        v-model:search-query="searchQuery"
        v-model:filter-location="filterLocation"
        v-model:filter-manufacturer="filterManufacturer"
        :vendors="vendorList"
        @update:search-query="filterEquipment"
        @update:filter-location="filterEquipment"
        @update:filter-manufacturer="filterEquipment"
      />
    </div>
    <div v-if="filteredEquipment.length" class="equipment-container">
      <table v-if="!showHierarchy" class="equipment-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Model</th>
            <th>Serial</th>
            <th>Location</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredEquipment" :key="item.id" @mouseenter="hoverItem = item.id" @mouseleave="hoverItem = null" :class="{ 'hover': hoverItem === item.id }">
            <td>{{ item.name }}</td>
            <td>{{ item.model }}</td>
            <td>{{ item.serial }}</td>
            <td>{{ item.location_status }}</td>
            <td>
              <button @click="editEquipment(item)">Edit</button>
              <button @click="deleteEquipment(item.id)" class="delete-btn">Delete</button>
              <button @click="showDetails(item)">Details</button>
            </td>
          </tr>
        </tbody>
      </table>
      <ul v-else class="hierarchy-list">
        <equipment-node v-for="item in filteredEquipment" :key="item.id" :item="item" @edit="editEquipment" @delete="deleteEquipment" />
      </ul>
    </div>
    <p v-else>No equipment found</p>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click="hideDetails">
      <div class="modal-content" @click.stop>
        <h2>{{ selectedEquipment.name }} Details</h2>
        <p><strong>ID:</strong> {{ selectedEquipment.id }}</p>
        <p><strong>Name:</strong> {{ selectedEquipment.name }}</p>
        <p><strong>Model:</strong> {{ selectedEquipment.model }}</p>
        <p><strong>Serial:</strong> {{ selectedEquipment.serial }}</p>
        <p><strong>Location:</strong> {{ selectedEquipment.location_status }}</p>
        <p><strong>Description:</strong> {{ selectedEquipment.description || 'N/A' }}</p>
        <p><strong>Manufacturer:</strong> {{ selectedEquipment.manufacturer_details ? selectedEquipment.manufacturer_details.name : 'N/A' }}</p>
        <p><strong>Parent:</strong> {{ selectedEquipment.parent ? selectedEquipment.parent : 'None' }}</p>
        <button @click="hideDetails" class="close-btn">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.equipment {
  max-width: 1000px;
  margin: 0 auto;
  padding: 10px;
}
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  position: relative;
}
.header h1 {
  margin: 0;
  font-size: 1.5em;
  text-align: center;
}
.header-buttons {
  position: absolute;
  right: 0;
  display: flex;
  gap: 10px;
}
.toggle-btn, .view-btn {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 4px;
}
.toggle-btn:hover, .view-btn:hover {
  background-color: #2c3e50;
}
.controls {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}
.equipment-container {
  margin-top: 10px;
}
.equipment-table {
  width: 100%;
  border-collapse: collapse;
}
.equipment-table th, .equipment-table td {
  padding: 6px 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
.equipment-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}
.equipment-table tr:nth-child(even) {
  background-color: #f9f9f9;
}
.equipment-table tr.hover {
  background-color: #f1f1f1;
}
.equipment-table button {
  padding: 4px 8px;
  margin-right: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.equipment-table button:first-child {
  background-color: #42b983;
  color: white;
}
.equipment-table button:first-child:hover {
  background-color: #2c3e50;
}
.equipment-table .delete-btn {
  background-color: #e74c3c;
  color: white;
}
.equipment-table .delete-btn:hover {
  background-color: #c0392b;
}
.hierarchy-list {
  list-style-type: none;
  padding-left: 0;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.modal-content h2 {
  margin-top: 0;
}
.modal-content p {
  margin: 5px 0;
}
.close-btn {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 4px;
  margin-top: 10px;
}
.close-btn:hover {
  background-color: #2c3e50;
}
</style>

<script>
import { reactive } from 'vue'
import EquipmentNode from './EquipmentNode.vue'
import FilterControls from './FilterControls.vue'
import EquipmentForm from './EquipmentForm.vue'
import { fetchCsrfToken, fetchData, saveData, deleteData } from '../utils/api.js'

export default {
  name: 'EquipmentPage',
  components: {
    EquipmentNode,
    FilterControls,
    EquipmentForm
  },
  setup() {
    const state = reactive({
      equipment: [],
      filteredEquipment: [],
      vendorList: [],
      csrfToken: null,
      searchQuery: '',
      filterLocation: '',
      filterManufacturer: '',
      newEquipment: {
        name: '',
        model: '',
        serial: '',
        description: '',
        location_status: 'in-house',
        parent: '',
        manufacturer: ''
      },
      editingEquipment: null,
      errorMessage: '',
      showForm: false,
      showDetailsModal: false,
      selectedEquipment: null,
      hoverItem: null,
      showHierarchy: false // New toggle for view mode
    })

    return state
  },
  computed: {
    flattenedEquipment() {
      const seenIds = new Set()
      const flatten = (items) => {
        let flat = []
        items.forEach(item => {
          if (!seenIds.has(item.id) && (!this.editingEquipment || item.id !== this.editingEquipment.id)) {
            seenIds.add(item.id)
            flat.push({ id: item.id, name: item.name })
          }
          if (item.children && item.children.length) {
            flat = flat.concat(flatten(item.children))
          }
        })
        return flat
      }
      return flatten(this.equipment)
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => {
      this.fetchVendors()
      this.fetchEquipment()
    })
  },
  methods: {
    async fetchCsrfToken() {
      this.csrfToken = await fetchCsrfToken()
    },
    async fetchEquipment() {
      try {
        const data = await fetchData('equipment', this.csrfToken)
        this.equipment = data.filter(item => item.is_active)
        this.filteredEquipment = this.equipment.filter(item => !item.parent)
        console.log('Fetched equipment:', this.equipment)
        console.log('Initial filteredEquipment:', this.filteredEquipment)
        console.log('Initial filteredEquipment children check:', this.filteredEquipment.map(item => ({
          id: item.id,
          name: item.name,
          children: item.children ? item.children.map(child => ({
            id: child.id,
            name: child.name,
            parent: child.parent,
            children: child.children ? child.children.length : 0
          })) : []
        })))
        this.filterEquipment()
      } catch (error) {
        // Error logged in fetchData
      }
    },
    async fetchVendors() {
      try {
        this.vendorList = await fetchData('vendors', this.csrfToken)
      } catch (error) {
        // Error logged in fetchData
      }
    },
    filterEquipment() {
      const query = this.searchQuery.toLowerCase()
      const filterRecursive = (items) => {
        return items.map(item => {
          const matchesName = query ? item.name.toLowerCase().includes(query) : true
          const matchesLocation = this.filterLocation ? item.location_status === this.filterLocation : true
          const matchesManufacturer = this.filterManufacturer ? 
            (item.manufacturer && item.manufacturer.id === parseInt(this.filterManufacturer)) : true
          const itemMatches = matchesName && matchesLocation && matchesManufacturer
          let filteredChildren = []
          if (item.children && item.children.length) {
            filteredChildren = filterRecursive(item.children)
            item.children = filteredChildren
          }
          if (itemMatches || filteredChildren.length > 0) {
            return { ...item }
          }
          return null
        }).filter(item => item !== null)
      }
      this.filteredEquipment = filterRecursive(this.equipment.filter(item => !item.parent))
      console.log('Filtered equipment after filter:', this.filteredEquipment)
    },
    async saveEquipment(equipmentData) {
      try {
        await this.fetchCsrfToken()
        console.log('saveEquipment called, editingEquipment:', this.editingEquipment)
        const isEdit = !!this.editingEquipment && this.editingEquipment.id
        console.log('isEdit:', isEdit)
        const dataToSend = isEdit ? { ...equipmentData, id: this.editingEquipment.id } : { ...equipmentData, id: undefined }
        console.log('Sending equipment data:', JSON.stringify(dataToSend))
        const response = await saveData('equipment', dataToSend, this.csrfToken, isEdit)
        console.log('Response:', response)
        this.fetchEquipment()
        this.showForm = false
        this.resetForm()
      } catch (error) {
        console.error('Save equipment failed:', error)
        this.errorMessage = 'Failed to save equipment. Please try again.'
      }
    },
    async deleteEquipment(equipmentId) {
      if (confirm('Are you sure you want to delete this equipment? This will also delete its children.')) {
        try {
          await this.fetchCsrfToken()
          await deleteData('equipment', equipmentId, this.csrfToken)
          this.fetchEquipment()
        } catch (error) {
          this.errorMessage = 'Failed to delete equipment. Please try again.'
        }
      }
    },
    editEquipment(item) {
      console.log('Editing item:', item)
      this.editingEquipment = { ...item }
      console.log('After editEquipment, editingEquipment set to:', this.editingEquipment)
      this.showForm = true
    },
    cancelEdit() {
      this.resetForm()
      this.showForm = false
    },
    resetForm() {
      console.log('Resetting form')
      this.newEquipment = { 
        name: '', 
        model: '', 
        serial: '', 
        description: '', 
        location_status: 'in-house', 
        parent: '', 
        manufacturer: '' 
      }
      this.editingEquipment = null
      this.errorMessage = ''
    },
    toggleForm() {
      this.showForm = !this.showForm
      if (!this.showForm) {
        this.resetForm()
      } else if (!this.editingEquipment) {
        this.resetForm()
      }
    },
    showDetails(item) {
      this.selectedEquipment = item
      this.showDetailsModal = true
    },
    hideDetails() {
      this.showDetailsModal = false
      this.selectedEquipment = null
    },
    toggleView() {
      this.showHierarchy = !this.showHierarchy
    }
  }
}
</script>