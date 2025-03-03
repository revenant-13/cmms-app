<template>
  <div class="schedules">
    <h1>Schedules</h1>
    <table v-if="schedules.length">
      <thead>
        <tr>
          <th>Task</th>
          <th>Due Date</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="schedule in schedules" :key="schedule.id">
          <td>{{ schedule.task.description }}</td>
          <td>{{ schedule.due_date }}</td>
          <td>{{ schedule.status }}</td>
          <td>
            <button v-if="schedule.status === 'pending'" @click="completeSchedule(schedule.id)">Complete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading schedules...</p>
  </div>
</template>

<style scoped>
  .schedules {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
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
  button {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
  }
  button:hover {
    background-color: #2c3e50;
  }
</style>

<script>
import axios from 'axios'

export default {
  name: 'SchedulesPage',
  data() {
    return {
      schedules: [],
      csrfToken: null
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => this.fetchSchedules())
  },
  methods: {
    async fetchCsrfToken() {
      try {
        await axios.get('http://localhost:8000/api/schedules/', { withCredentials: true })
        this.csrfToken = this.getCsrfToken()
      } catch (error) {
        console.error('Error fetching CSRF token:', error)
      }
    },
    fetchSchedules() {
      axios.get('http://localhost:8000/api/schedules/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.schedules = response.data
        })
        .catch(error => {
          console.error('Error fetching schedules:', error)
        })
    },
    async completeSchedule(scheduleId) {
      try {
        await this.fetchCsrfToken() // Refresh CSRF before PUT
        const schedule = this.schedules.find(s => s.id === scheduleId)
        const updatedSchedule = { ...schedule, status: 'completed' }
        await axios.put(`http://localhost:8000/api/schedules/${scheduleId}/`, updatedSchedule, {
          withCredentials: true,
          headers: { 'X-CSRFToken': this.csrfToken }
        })
        this.fetchSchedules() // Refresh list
      } catch (error) {
        console.error('Error completing schedule:', error)
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