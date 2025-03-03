<template>
  <div class="tasks">
    <h1>Tasks</h1>
    <div class="form">
      <h2>Add New Task</h2>
      <form @submit.prevent="addTask">
        <input v-model="newTask.description" placeholder="Description" required />
        <select v-model="newTask.frequency">
          <option value="">One-Time</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="yearly">Yearly</option>
        </select>
        <select v-model="newTask.equipment" required>
          <option value="" disabled>Select Equipment</option>
          <option v-for="equip in equipment" :key="equip.id" :value="equip.id">
            {{ equip.name }}
          </option>
        </select>
        <select v-model="newTask.assigned_to">
          <option value="">Unassigned</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>
        <input v-model="newTask.start_date" type="date" required />
        <select v-model="newTask.task_type" required>
          <option value="" disabled>Select Type</option>
          <option value="maintenance">Maintenance</option>
          <option value="calibration">Calibration</option>
        </select>
        <select v-model="newTask.priority">
          <option value="medium">Medium</option>
          <option value="low">Low</option>
          <option value="high">High</option>
        </select>
        <button type="submit">Add Task</button>
      </form>
    </div>
    <table v-if="tasks.length">
      <thead>
        <tr>
          <th>Description</th>
          <th>Frequency</th>
          <th>Equipment</th>
          <th>Assigned To</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id">
          <td>{{ task.description }}</td>
          <td>{{ task.frequency || 'One-Time' }}</td>
          <td>{{ task.equipment.name }}</td>
          <td>{{ task.assigned_to ? task.assigned_to.username : 'Unassigned' }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading tasks...</p>
  </div>
</template>

<style scoped>
  .tasks {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  .form {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  input, select, button {
    margin: 5px 0;
    padding: 8px;
    width: 100%;
    box-sizing: border-box;
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
  name: 'TasksPage',
  data() {
    return {
      tasks: [],
      equipment: [],
      users: [],
      csrfToken: null,
      newTask: {
        description: '',
        frequency: '',
        equipment: '',
        assigned_to: '',
        start_date: '',
        task_type: '',
        priority: 'medium'
      }
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => {
      this.fetchEquipment()
      this.fetchUsers()
      this.fetchTasks()
    })
  },
  methods: {
    async fetchCsrfToken() {
      try {
        await axios.get('http://localhost:8000/api/tasks/', { withCredentials: true })
        this.csrfToken = this.getCsrfToken()
      } catch (error) {
        console.error('Error fetching CSRF token:', error)
      }
    },
    fetchTasks() {
      axios.get('http://localhost:8000/api/tasks/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.tasks = response.data
        })
        .catch(error => {
          console.error('Error fetching tasks:', error)
        })
    },
    fetchEquipment() {
      axios.get('http://localhost:8000/api/equipment/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.equipment = response.data
        })
        .catch(error => {
          console.error('Error fetching equipment:', error)
        })
    },
    fetchUsers() {
      axios.get('http://localhost:8000/api/users/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.users = response.data
        })
        .catch(error => {
          console.error('Error fetching users:', error)
        })
    },
    async addTask() {
      try {
        await this.fetchCsrfToken() // Refresh CSRF before POST
        const taskData = { ...this.newTask }
        if (!taskData.assigned_to) delete taskData.assigned_to // Remove if empty
        const response = await axios.post('http://localhost:8000/api/tasks/', taskData, {
          withCredentials: true,
          headers: { 'X-CSRFToken': this.csrfToken }
        })
        this.tasks.push(response.data)
        this.newTask = { description: '', frequency: '', equipment: '', assigned_to: '', start_date: '', task_type: '', priority: 'medium' }
      } catch (error) {
        console.error('Error adding task:', error)
        if (error.response) {
          console.log('Response data:', error.response.data)
        }
      }
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