import axios from 'axios'

export async function fetchCsrfToken() {
  try {
    await axios.get('http://localhost:8000/api/equipment/', { withCredentials: true })
    return getCsrfToken()
  } catch (error) {
    console.error('Error fetching CSRF token:', error)
    throw error
  }
}

export function getCsrfToken() {
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

export async function fetchData(endpoint, csrfToken) {
  try {
    const response = await axios.get(`http://localhost:8000/api/${endpoint}/`, {
      withCredentials: true,
      headers: { 'X-CSRFToken': csrfToken }
    })
    return response.data
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error)
    throw error
  }
}

export async function saveData(endpoint, data, csrfToken, isEdit = false) {
  try {
    const method = isEdit ? 'put' : 'post'
    const url = isEdit && data.id ? `${endpoint}/${data.id}/` : `${endpoint}/` // Added slash before id
    console.log(`Saving to ${method.toUpperCase()} http://localhost:8000/api/${url}`)
    const response = await axios[method](`http://localhost:8000/api/${url}`, data, {
      withCredentials: true,
      headers: { 'X-CSRFToken': csrfToken }
    })
    return response.data
  } catch (error) {
    console.error(`Error ${isEdit ? 'updating' : 'saving'} ${endpoint}:`, error)
    throw error
  }
}

export async function deleteData(endpoint, id, csrfToken) {
  try {
    await axios.delete(`http://localhost:8000/api/${endpoint}/${id}/`, { // Added slash before id
      withCredentials: true,
      headers: { 'X-CSRFToken': csrfToken }
    })
  } catch (error) {
    console.error(`Error deleting ${endpoint}:`, error)
    throw error
  }
}