<template>
  <div id="app">
    <nav>
      <router-link to="/">Dashboard</router-link>
      <router-link to="/equipment">Equipment</router-link>
      <router-link to="/parts">Parts</router-link>
      <router-link to="/tasks">Tasks</router-link>
      <router-link to="/schedules">Schedules</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}
nav {
  padding: 10px;
  background-color: #f4f4f4;
  border-bottom: 1px solid #ddd;
}
nav a {
  margin: 0 15px;
  text-decoration: none;
  color: #42b983;
  font-weight: 500;
}
nav a.router-link-exact-active {
  color: #2c3e50;
  font-weight: bold;
  border-bottom: 2px solid #2c3e50;
}
</style>

<script>
export default {
  name: 'App'
}
</script>