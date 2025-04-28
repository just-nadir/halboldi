<template>
    <v-container>
      <h2 class="text-h5 mb-4">Hisobotlar</h2>
  
      <!-- 📅 Sana filtri -->
      <v-row class="mb-4">
        <v-col cols="12" sm="6" md="3">
          <v-text-field v-model="startDate" label="Dan" type="date" />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-text-field v-model="endDate" label="Gacha" type="date" />
        </v-col>
      </v-row>
  
      <!-- 📊 Statistik kartalar -->
      <v-row class="mb-4">
        <v-col cols="12" sm="6" md="3">
          <v-card color="blue-lighten-5" class="pa-4" variant="flat">
            <v-icon size="30" color="blue-darken-2">mdi-format-list-bulleted</v-icon>
            <h3 class="text-h6 mt-2">Jami buyurtmalar</h3>
            <div class="text-h5 font-weight-bold">{{ totalOrders }} ta</div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card color="green-lighten-5" class="pa-4" variant="flat">
            <v-icon size="30" color="green-darken-2">mdi-cash</v-icon>
            <h3 class="text-h6 mt-2">Jami komissiya</h3>
            <div class="text-h5 font-weight-bold">{{ totalCommission.toLocaleString() }} so‘m</div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card color="orange-lighten-5" class="pa-4" variant="flat">
            <v-icon size="30" color="orange-darken-2">mdi-star</v-icon>
            <h3 class="text-h6 mt-2">Ko‘p ishlagan usta</h3>
            <div class="text-h6">{{ topWorker?.name || '-' }} ({{ topWorker?.count || 0 }} ta)</div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card color="red-lighten-5" class="pa-4" variant="flat">
            <v-icon size="30" color="red-darken-2">mdi-wallet</v-icon>
            <h3 class="text-h6 mt-2">Ko‘p komissiya to‘lagan</h3>
            <div class="text-h6">{{ topCommissionWorker?.name || '-' }} ({{ topCommissionWorker?.sum.toLocaleString() || 0 }} so‘m)</div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import axios from 'axios'
  
  const orders = ref([])
  
  const today = new Date().toISOString().substr(0, 10)
  const startDate = ref(today)
  const endDate = ref(today)
  
  const fetchOrders = async () => {
    const res = await axios.get('http://127.0.0.1:8000/api/orders/')
    orders.value = res.data
  }
  
  const filteredOrders = computed(() => {
    const start = new Date(startDate.value)
    const end = new Date(endDate.value)
    end.setDate(end.getDate() + 1)
  
    return orders.value.filter(o => {
      const d = new Date(o.created_at)
      return o.status === 'bajarildi' && d >= start && d < end
    })
  })
  
  const totalOrders = computed(() => filteredOrders.value.length)
  
  const totalCommission = computed(() =>
    filteredOrders.value.reduce((sum, o) => sum + (o.job_commission || 0), 0)
  )
  
  // 🧑‍🔧 Eng ko‘p ishlagan usta
  const topWorker = computed(() => {
    const map = {}
    filteredOrders.value.forEach(o => {
      if (o.worker_name) {
        map[o.worker_name] = (map[o.worker_name] || 0) + 1
      }
    })
    const sorted = Object.entries(map).sort((a, b) => b[1] - a[1])
    if (sorted.length === 0) return null
    return { name: sorted[0][0], count: sorted[0][1] }
  })
  
  // 💵 Eng ko‘p komissiya to‘lagan usta
  const topCommissionWorker = computed(() => {
    const map = {}
    filteredOrders.value.forEach(o => {
      if (o.worker_name) {
        map[o.worker_name] = (map[o.worker_name] || 0) + (o.job_commission || 0)
      }
    })
    const sorted = Object.entries(map).sort((a, b) => b[1] - a[1])
    if (sorted.length === 0) return null
    return { name: sorted[0][0], sum: sorted[0][1] }
  })
  
  onMounted(() => {
    fetchOrders()
  })
  </script>
  