<template>
  <li class="equipment-item">
    <div class="equipment-info">
      <span>{{ item.name }} (Model: {{ item.model }})</span>
      <div class="actions">
        <button @click="$emit('edit', item)">Edit</button>
        <button @click="$emit('delete', item.id)" class="delete-btn">Delete</button>
        <button v-if="item.parts && item.parts.length" @click="toggleParts">
          {{ showParts ? 'Hide Parts' : 'View Parts' }}
        </button>
      </div>
    </div>
    <ul v-if="showParts && item.parts && item.parts.length" class="parts-list">
      <li v-for="part in item.parts" :key="part.id" class="part-item">
        {{ part.name }} (Qty: {{ part.quantity || 'N/A' }}) - {{ part.description || 'No description' }}
      </li>
    </ul>
    <ul v-if="item.children && item.children.length" class="children-list">
      <equipment-node
        v-for="child in item.children"
        :key="child.id"
        :item="child"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
      />
    </ul>
  </li>
</template>

<style scoped>
.equipment-item {
  margin: 5px 0;
  padding: 5px;
  border-left: 2px solid #42b983;
}
.equipment-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.actions button {
  padding: 4px 8px;
  margin-left: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.actions button:first-child {
  background-color: #42b983;
  color: white;
}
.actions button:first-child:hover {
  background-color: #2c3e50;
}
.actions .delete-btn {
  background-color: #e74c3c;
  color: white;
}
.actions .delete-btn:hover {
  background-color: #c0392b;
}
.parts-list {
  list-style-type: disc;
  padding-left: 20px;
  margin: 5px 0 0 10px;
}
.part-item {
  font-size: 0.9em;
  color: #555;
}
.children-list {
  list-style-type: none;
  padding-left: 20px;
  margin: 5px 0 0 0;
}
</style>

<script>
import { ref } from 'vue'

export default {
  name: 'EquipmentNode',
  props: {
    item: Object
  },
  setup() {
    const showParts = ref(false)

    const toggleParts = () => {
      showParts.value = !showParts.value
    }

    return { showParts, toggleParts }
  }
}
</script>