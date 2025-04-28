<template>
    <v-container>
      <h2 class="text-h5 mb-4">❌ Bekor qilingan buyurtmalar</h2>
  
      <v-data-table
        :headers="headers"
        :items="orders"
        class="elevation-1"
      >
        <template #item.created_at="{ item }">
          {{ new Date(item.created_at).toLocaleString() }}
        </template>
        <template #item.job_commission="{ item }">
          {{ item.job_commission ? item.job_commission + ' so‘m' : '-' }}
        </template>
        <template #item.status="{ item }">
          <v-chip color="red" dark>Bekor qilindi</v-chip>
        </template>
      </v-data-table>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const orders = ref([])
  
  const headers = [
    { title: 'Sana', key: 'created_at' },
    { title: 'Mijoz', key: 'customer_name' },
    { title: 'Telefon', key: 'phone' },
    { title: 'Manzil', key: 'address' },
    { title: 'Ish turi', key: 'job_title' },
    { title: 'Komissiya', key: 'job_commission' },
    { title: 'Usta', key: 'worker_name' },
    { title: 'Sabab', key: 'cancel_reason' },
    { title: 'Status', key: 'status' }
  ]
  
  const fetchOrders = async () => {
    const res = await axios.get('http://127.0.0.1:8000/api/orders/')
    orders.value = res.data.filter(order => order.status === 'bekor')
  }
  
  onMounted(fetchOrders)
  </script>
  