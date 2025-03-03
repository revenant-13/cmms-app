<template>
  <div class="form">
    <h2>{{ editing ? 'Edit Equipment' : 'Add New Equipment' }}</h2>
    <p v-if="error" class="error">{{ error }}</p>
    <form @submit.prevent="$emit('save', equipmentData)">
      <input v-model="equipmentData.name" placeholder="Name" required id="name" name="name" />
      <input v-model="equipmentData.model" placeholder="Model" id="model" name="model" />
      <input v-model="equipmentData.serial" placeholder="Serial Number" id="serial" name="serial" />
      <textarea v-model="equipmentData.description" placeholder="Description"></textarea>
      <select v-model="equipmentData.location_status" required id="location_status" name="location_status">
        <option value="in-house">In-House</option>
        <option value="off-site">Off-Site</option>
      </select>
      <select v-model="equipmentData.parent" id="parent" name="parent">
        <option value="">No Parent</option>
        <option v-for="equip in equipmentList" :key="equip.id" :value="equip.id">
          {{ equip.name }}
        </option>
      </select>
      <select v-model="equipmentData.manufacturer" id="manufacturer" name="manufacturer">
        <option value="">No Manufacturer</option>
        <option v-for="vendor in vendorList" :key="vendor.id" :value="vendor.id">
          {{ vendor.name }}
        </option>
      </select>
      <button type="submit">{{ editing ? 'Update' : 'Add' }}</button>
      <button v-if="editing" type="button" @click="$emit('cancel')">Cancel</button>
    </form>
  </div>
</template>

<script>
import { ref, watch, computed } from 'vue'

export default {
  name: 'EquipmentForm',
  props: {
    equipment: Object,
    equipmentList: Array,
    vendorList: Array,
    error: String
  },
  setup(props) {
    const equipmentData = ref(
      props.equipment ? { ...props.equipment } : {
        name: '',
        model: '',
        serial: '',
        description: '',
        location_status: 'in-house',
        parent: '',
        manufacturer: ''
      }
    )

    const editing = computed(() => !!props.equipment)

    // Debug prop changes
    watch(() => props.equipment, (newVal) => {
      console.log('EquipmentForm: props.equipment changed to:', newVal)
      equipmentData.value = newVal ? { ...newVal } : {
        name: '',
        model: '',
        serial: '',
        description: '',
        location_status: 'in-house',
        parent: '',
        manufacturer: ''
      }
    }, { deep: true, immediate: true })

    return { equipmentData, editing }
  }
}
</script>

<style scoped>
.form {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
input, select, textarea, button {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  box-sizing: border-box;
}
textarea {
  height: 100px;
}
button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 8px 15px;
  margin: 5px 5px 0 0;
  cursor: pointer;
}
button:hover {
  background-color: #2c3e50;
}
.error {
  color: red;
  margin-bottom: 10px;
}
</style>