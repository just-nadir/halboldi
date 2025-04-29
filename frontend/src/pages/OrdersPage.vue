<template>
  <v-container>
    <!-- 📋 Sarlavha + Excel tugmasi -->
    <v-row class="d-flex justify-space-between align-center mb-4">
      <v-col cols="auto">
        <h2 class="text-h5">Bajarilgan buyurtmalar</h2>
      </v-col>
      <v-col cols="auto">
        <v-btn color="success" @click="exportToExcel" prepend-icon="mdi-download">
          Excelga yuklash
        </v-btn>
      </v-col>
    </v-row>

    <!-- 📅 Sana filtri -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="4">
        <v-text-field
          v-model="startDate"
          label="Dan"
          type="date"
        />
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-text-field
          v-model="endDate"
          label="Gacha"
          type="date"
        />
      </v-col>
    </v-row>

    <!-- 📊 Statistika -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="3">
        <v-card color="blue-lighten-5" class="pa-4" variant="flat">
          <v-icon size="30" color="blue-darken-2">mdi-cart</v-icon>
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
    </v-row>

    <!-- 📋 Jadval -->
    <v-data-table
      :headers="headers"
      :items="filteredOrders"
      :items-per-page="10"
      class="elevation-1"
    >
      <template #item.created_at="{ item }">
        {{ new Date(item.created_at).toLocaleString() }}
      </template>

      <template #item.job_commission="{ item }">
        {{ item.job_commission ? item.job_commission + ' so‘m' : '-' }}
      </template>

      <template #item.worker_name="{ item }">
        {{ item.worker_name || '-' }}
      </template>

      <template #item.status="{ item }">
        <v-chip :color="statusColor(item.status)" dark>
          {{ statusLabel(item.status) }}
        </v-chip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'

const orders = ref([])

const today = new Date().toISOString().substr(0, 10)
const startDate = ref(today)
const endDate = ref(today)

const headers = [
  { title: 'Sana', key: 'created_at' },
  { title: 'Mijoz', key: 'customer_name' },
  { title: 'Telefon', key: 'phone' },
  { title: 'Manzil', key: 'address' },
  { title: 'Ish', key: 'job_title' },
  { title: 'Komissiya', key: 'job_commission' },
  { title: 'Usta', key: 'worker_name' },
  { title: 'Holat', key: 'status' }
]

const fetchOrders = async () => {
  const res = await axios.get('https://halboldi.uz/api/orders/')
  orders.value = res.data
}

const filteredOrders = computed(() => {
  const start = new Date(startDate.value)
  const end = new Date(endDate.value)
  end.setDate(end.getDate() + 1)

  return orders.value.filter(order => {
    const date = new Date(order.created_at)
    return (
      order.status === 'bajarildi' &&
      date >= start && date < end
    )
  })
})

const totalOrders = computed(() => filteredOrders.value.length)

const totalCommission = computed(() =>
  filteredOrders.value.reduce((sum, order) => sum + (order.job_commission || 0), 0)
)

const statusLabel = (status) => ({
  yangi: 'Yangi',
  qabul_qilindi: 'Qabul qilindi',
  bajarilmoqda: 'Bajarilmoqda',
  bajarildi: 'Bajarildi',
  bekor: 'Bekor qilindi'
}[status] || status)

const statusColor = (status) => ({
  yangi: 'blue',
  qabul_qilindi: 'cyan',
  bajarilmoqda: 'orange',
  bajarildi: 'green',
  bekor: 'red'
}[status] || 'grey')

const exportToExcel = () => {
  const data = filteredOrders.value.map(order => ({
    Sana: new Date(order.created_at).toLocaleString(),
    Mijoz: order.customer_name,
    Telefon: order.phone,
    Manzil: order.address,
    Ish: order.job_title,
    Komissiya: order.job_commission,
    Usta: order.worker_name,
    Holat: statusLabel(order.status)
  }))

  const worksheet = XLSX.utils.json_to_sheet(data)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Buyurtmalar')
  const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
  const blob = new Blob([excelBuffer], { type: 'application/octet-stream' })
  saveAs(blob, `buyurtmalar-${startDate.value}_to_${endDate.value}.xlsx`)
}

onMounted(() => {
  fetchOrders()
})
</script>
