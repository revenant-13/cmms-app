<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="filter">
      <label>Filter by Date Range:</label>
      <input type="date" v-model="startDate" @change="applyFilter" />
      <input type="date" v-model="endDate" @change="applyFilter" />
    </div>
    <div class="summary">
      <div class="card">
        <h2>Planned Tasks</h2>
        <p>{{ filteredPlannedTasks.length }}</p>
        <ul>
          <li v-for="task in filteredPlannedTasks" :key="task.id">{{ task.description }}</li>
        </ul>
      </div>
      <div class="card">
        <h2>Due Schedules</h2>
        <p>{{ filteredDueSchedules.length }}</p>
        <ul>
          <li v-for="schedule in filteredDueSchedules" :key="schedule.id">
            {{ schedule.task.description }} (Due: {{ schedule.due_date }})
          </li>
        </ul>
      </div>
      <div class="card">
        <h2>Completed Tasks</h2>
        <p>{{ filteredCompletedSchedules.length }}</p>
        <ul>
          <li v-for="schedule in filteredCompletedSchedules" :key="schedule.id">
            {{ schedule.task.description }} (Completed: {{ schedule.completion_date }})
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .dashboard {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  .filter {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  .filter label {
    margin-right: 10px;
  }
  .filter input {
    margin-right: 10px;
    padding: 5px;
  }
  .summary {
    display: flex;
    justify-content: space-between;
    gap: 20px;
  }
  .card {
    flex: 1;
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 5px;
    background-color: #fff;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    margin: 5px 0;
  }
</style>

<script>
import axios from 'axios'

export default {
  name: 'DashboardPage',
  data() {
    return {
      tasks: [],
      schedules: [],
      csrfToken: null,
      startDate: '',
      endDate: ''
    }
  },
  computed: {
    filteredPlannedTasks() {
      return this.tasks.filter(task => {
        const hasSchedule = this.schedules.some(s => s.task.id === task.id && s.status === 'completed')
        if (!hasSchedule) {
          return this.isWithinDateRange(task.start_date)
        }
        return false
      })
    },
    filteredDueSchedules() {
      return this.schedules.filter(schedule => {
        return schedule.status === 'pending' && this.isWithinDateRange(schedule.due_date)
      })
    },
    filteredCompletedSchedules() {
      return this.schedules.filter(schedule => {
        return schedule.status === 'completed' && this.isWithinDateRange(schedule.completion_date || schedule.due_date)
      })
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => {
      this.fetchTasks()
      this.fetchSchedules()
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
    },
    isWithinDateRange(date) {
      if (!this.startDate && !this.endDate) return true
      const taskDate = new Date(date)
      const start = this.startDate ? new Date(this.startDate) : null
      const end = this.endDate ? new Date(this.endDate) : null
      if (start && end) return taskDate >= start && taskDate <= end
      if (start) return taskDate >= start
      if (end) return taskDate <= end
      return true
    },
    applyFilter() {
      // Trigger re-computation of filtered lists
      this.$forceUpdate()
    }
  }
}
</script>