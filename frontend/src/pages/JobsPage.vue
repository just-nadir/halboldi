<template>
    <v-container>
      <h2 class="text-h5 mb-4">Ishlar ro'yxati</h2>
  
      <v-btn color="primary" class="mb-4" @click="showDialog = true">
        + Yangi ish qo‘shish
      </v-btn>
  
      <v-data-table
        :headers="headers"
        :items="jobs"
        class="elevation-1"
      >
        <template #item.commission="{ item }">
          {{ item.commission ? item.commission + ' so‘m' : '-' }}
        </template>
  
        <template #item.actions="{ item }">
          <v-icon color="red" @click="deleteJob(item.id)">mdi-delete</v-icon>
        </template>
      </v-data-table>
  
      <!-- Modal: Yangi ish qo‘shish -->
      <v-dialog v-model="showDialog" max-width="500">
        <v-card>
          <v-card-title>Yangi ish qo‘shish</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="addJob">
              <v-text-field v-model="newJob.title" label="Ish nomi" required />
              <v-text-field v-model="newJob.commission" label="Komissiya (so‘m)" type="number" required />
              <v-btn type="submit" color="success" class="mt-3">Saqlash</v-btn>
              <v-btn class="mt-3 ms-2" @click="showDialog = false">Bekor</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const jobs = ref([])
  const showDialog = ref(false)
  
  const newJob = ref({
    title: '',
    commission: ''
  })
  
  const headers = [
    { title: 'ID', key: 'id' },
    { title: 'Ish nomi', key: 'title' },
    { title: 'Komissiya', key: 'commission' },
    { title: 'Amallar', key: 'actions', sortable: false }
  ]
  
  const fetchJobs = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/jobs/')
      jobs.value = res.data
    } catch (err) {
      console.error('Ishlarni olishda xatolik:', err)
    }
  }
  
  const addJob = async () => {
    const title = newJob.value.title.trim()
    const commission = parseFloat(newJob.value.commission)
  
    if (!title || isNaN(commission)) {
      alert("Iltimos, ish nomi va komissiyani kiriting.")
      return
    }
  
    try {
      await axios.post('http://127.0.0.1:8000/api/jobs/', {
        title,
        commission
      })
      newJob.value = { title: '', commission: '' }
      showDialog.value = false
      fetchJobs()
    } catch (err) {
      console.error('Yangi ishni qo‘shishda xatolik:', err.response?.data || err)
      alert("Komissiya bilan yangi ishni qo‘shishda xatolik.")
    }
  }
  
  const deleteJob = async (id) => {
    if (confirm('Bu ishni o‘chirmoqchimisiz?')) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/jobs/${id}/`)
        fetchJobs()
      } catch (err) {
        console.error('O‘chirishda xatolik:', err)
      }
    }
  }
  
  onMounted(() => {
    fetchJobs()
  })
  </script>
  