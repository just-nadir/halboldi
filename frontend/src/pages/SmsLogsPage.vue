<template>
    <v-container>
      <h2 class="text-h5 mb-4">📨 SMS yuborish loglari</h2>
  
      <v-data-table
        :headers="headers"
        :items="logs"
        :items-per-page="10"
        class="elevation-1"
      >
        <template #item.created_at="{ item }">
          {{ new Date(item.created_at).toLocaleString() }}
        </template>
  
        <template #item.success="{ item }">
          <v-chip :color="item.success ? 'green' : 'red'" dark small>
            {{ item.success ? 'Muvaffaqiyatli' : 'Xatolik' }}
          </v-chip>
        </template>
      </v-data-table>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const logs = ref([])
  
  const headers = [
    { title: 'Sana', key: 'created_at' },
    { title: 'Telefon', key: 'phone' },
    { title: 'Xabar', key: 'message' },
    { title: 'Holat', key: 'success' }
  ]
  
  const fetchLogs = async () => {
    try {
      const res = await axios.get('https://halboldi.uz/api/sms-logs/')
      logs.value = res.data
    } catch (err) {
      console.error('SMS loglarni olishda xatolik:', err)
    }
  }
  
  onMounted(() => {
    fetchLogs()
  })
  </script>
  