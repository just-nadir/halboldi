<template>
  <v-container>
    <!-- Snackbar xabarlari -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>

    <h2 class="text-h5 mb-4">Faol buyurtmalar</h2>

    <v-btn color="primary" class="mb-4" @click="showDialog = true">
      + Yangi buyurtma
    </v-btn>

    <v-data-table
      :headers="headers"
      :items="filteredOrders"
      :items-per-page="10"
      class="elevation-1"
    >
      <template #item.status="{ item }">
        <v-progress-linear
          :model-value="statusValue(item.status)"
          height="12"
          rounded
          :color="statusColor(item.status)"
          class="mb-1"
        />
        <div class="text-caption text-center mt-1">
          {{ statusLabel(item.status) }}
        </div>
      </template>

      <template #item.job_commission="{ item }">
        {{ item.job_commission ? item.job_commission + ' so‘m' : '-' }}
      </template>

      <template #item.created_at="{ item }">
        {{ new Date(item.created_at).toLocaleString() }}
      </template>

      <!-- ✅ Usta ko‘rinadigan qism -->
      <template #item.worker_name="{ item }">
        {{ item.worker_name || '-' }}
      </template>

      <template #item.actions="{ item }">
        <v-icon small color="green" class="me-2" @click="openAssignDialog(item)" v-if="canChangeStatus(item.status)">
          mdi-account-plus
        </v-icon>
        <v-icon small color="blue" class="me-2" @click="changeStatus(item)" v-if="canChangeStatus(item.status)">
          mdi-skip-next
        </v-icon>
        <v-icon small color="orange" class="me-2" @click="openCancelDialog(item)" v-if="canChangeStatus(item.status)">
          mdi-cancel
        </v-icon>
      </template>
    </v-data-table>

    <!-- ✅ Usta biriktirish MODAL -->
    <v-dialog v-model="assignDialog" max-width="400">
      <v-card>
        <v-card-title>Usta biriktirish</v-card-title>
        <v-card-text>
          <v-autocomplete
            v-model="selectedWorkerId"
            :items="workers"
            item-title="full_name"
            item-value="id"
            label="Ustani tanlang"
            :search-input.sync="workerSearch"
            dense
            clearable
          />
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="submitAssignWorker">Biriktirish</v-btn>
          <v-btn @click="assignDialog = false">Bekor</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ❌ Bekor qilish -->
    <v-dialog v-model="cancelDialog" max-width="500">
      <v-card>
        <v-card-title>Buyurtmani bekor qilish</v-card-title>
        <v-card-text>
          <v-textarea v-model="cancelReason" label="Bekor qilish sababi" auto-grow required />
          <v-btn color="error" class="mt-2" @click="submitCancel">Bekor qilish</v-btn>
          <v-btn class="mt-2 ms-2" @click="cancelDialog = false">Bekor</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- ➕ Buyurtma qo‘shish -->
    <v-dialog v-model="showDialog" max-width="600">
      <v-card>
        <v-card-title>Yangi buyurtma</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submitForm">
            <v-text-field v-model="form.customer_name" label="Mijoz ismi" required />
            <v-text-field v-model="form.phone" label="Telefon" required />
            <v-text-field v-model="form.address" label="Manzil" required />
            <v-autocomplete
              v-model="form.job"
              :items="filteredJobs"
              item-title="title"
              item-value="id"
              label="Ish turi"
              :search-input.sync="jobSearch"
              return-object
              required
            />
            <v-btn type="submit" color="success" class="mt-3">Saqlash</v-btn>
            <v-btn class="mt-3 ms-2" @click="showDialog = false">Bekor</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios, { all } from 'axios'

const orders = ref([])
const jobs = ref([])
const workers = ref([])

const jobSearch = ref('')
const showDialog = ref(false)
const cancelDialog = ref(false)
const assignDialog = ref(false)

const cancelReason = ref('')
const selectedOrder = ref(null)
const selectedOrderId = ref(null)
const selectedWorkerId = ref(null)

const form = ref({
  customer_name: '',
  phone: '',
  address: '',
  job: null
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Sana', key: 'created_at' },
  { title: 'Mijoz', key: 'customer_name' },
  { title: 'Telefon', key: 'phone' },
  { title: 'Manzil', key: 'address' },
  { title: 'Ish', key: 'job_title' },
  { title: 'Komissiya', key: 'job_commission' },
  { title: 'Usta', key: 'worker_name' },
  { title: 'Holat', key: 'status' },
  { title: 'Amallar', key: 'actions', sortable: false }
]

const fetchAll = async () => {
  const [o, j] = await Promise.all([
    axios.get('http://127.0.0.1:8000/api/orders/'),
    axios.get('http://127.0.0.1:8000/api/jobs/')
  ])
  orders.value = o.data
  jobs.value = j.data
}

const fetchWorkers = async () => {
  const res = await axios.get('http://127.0.0.1:8000/api/workers/')
  workers.value = res.data
}

const openAssignDialog = (order) => {
  selectedOrderId.value = order.id
  selectedWorkerId.value = order.assigned_worker || null
  assignDialog.value = true
}

const submitAssignWorker = async () => {
  if (!selectedWorkerId.value) return
  try {
    await axios.patch(`http://127.0.0.1:8000/api/orders/${selectedOrderId.value}/`, {
      assigned_worker: selectedWorkerId.value
    })
    assignDialog.value = false
      showSnackbar('Usta muvaffaqiyatli biriktirildi!', 'primary')
    fetchAll()
  } catch (err) {
    console.error("Ustani biriktirishda xatolik:", err)
  }
}

const filteredOrders = computed(() =>
  orders.value.filter(o => o.status !== 'bajarildi' && o.status !== 'bekor')
)

const filteredJobs = computed(() => {
  if (!jobSearch.value) return jobs.value
  return jobs.value.filter(job =>
    job.title.toLowerCase().includes(jobSearch.value.toLowerCase())
  )
  }
)

const submitForm = async () => {
  if (!form.value.job) {
    alert('Iltimos, ish turini tanlang.')
    return
  }

  const payload = {
    customer_name: form.value.customer_name,
    phone: form.value.phone,
    address: form.value.address,
    job: form.value.job.id
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/orders/', payload)
    form.value = { customer_name: '', phone: '', address: '', job: null }
    showDialog.value = false
      showSnackbar('Buyurtma saqlandi!', 'success')
    fetchAll()
  } catch (error) {
    console.error('Buyurtma qo‘shishda xatolik:', error)
    showSnackbar('Buyurtmani saqlab bo‘lmadi!', 'red')
  }
}


const changeStatus = async (order) => {
  const statusFlow = ['yangi', 'qabul_qilindi', 'bajarilmoqda', 'bajarildi']
  const currentIndex = statusFlow.indexOf(order.status)
  if (currentIndex === -1 || currentIndex === statusFlow.length - 1) return
  const nextStatus = statusFlow[currentIndex + 1]

  // ✅ Usta tekshiruvi: yangi → qabul_qilindi holatida
  if (order.status === 'yangi' && nextStatus === 'qabul_qilindi' && !order.assigned_worker) {
    showSnackbar('Oldin ustani biriktiring!', 'warning')
    return
  }

  try {
    await axios.patch(`http://127.0.0.1:8000/api/orders/${order.id}/`, {
      status: nextStatus
    })
    fetchAll()
    showSnackbar('Buyurtma holati yangilandi!', 'info')
  } catch (err) {
    console.error('Status o‘zgartirishda xatolik:', err)
  }
}


const canChangeStatus = (status) => {
  return status !== 'bajarildi' && status !== 'bekor'
}

const openCancelDialog = (order) => {
  selectedOrder.value = order
  cancelReason.value = ''
  cancelDialog.value = true
}

const submitCancel = async () => {
  if (!cancelReason.value.trim()) return
  try {
    await axios.patch(`http://127.0.0.1:8000/api/orders/${selectedOrder.value.id}/`, {
      status: 'bekor',
      cancel_reason: cancelReason.value
    })
    cancelDialog.value = false
      showSnackbar('Buyurtma bekor qilindi.', 'error')
    fetchAll()
  } catch (err) {
    console.error('Bekor qilishda xatolik:', err)
  }
}

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


const statusValue = (status) => ({
yangi: 10,
qabul_qilindi: 30,
bajarilmoqda: 60,
bajarildi: 100,
bekor: 100
}[status] || 0)


const snackbar = ref({
  show: false,
  text: '',
  color: ''
})

function showSnackbar(text, color = 'success') {
  snackbar.value.text = text
  snackbar.value.color = color
  snackbar.value.show = true
}

onMounted(() => {
  fetchAll()
  fetchWorkers()
})
</script>
