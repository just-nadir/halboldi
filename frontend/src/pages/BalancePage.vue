<template>
  <v-container>
    <h2 class="text-h5 mb-4">Ustalar balanslari</h2>

    <v-data-table
      :headers="headers"
      :items="workers"
      :items-per-page="10"
      class="elevation-1"
    >
      <template #item.balance="{ item }">
        {{ item.balance.toLocaleString() }} so‘m
      </template>

      <template #item.actions="{ item }">
        <v-btn size="small" color="primary" @click="openTopup(item)">
          To‘ldirish
        </v-btn>
        <v-btn size="small" @click="openHistory(item)">
          Tarix
        </v-btn>
      </template>
    </v-data-table>

    <!-- 🔍 Tarixni ko‘rish modali -->
    <v-dialog v-model="historyDialog" max-width="800">
      <v-card>
        <v-card-title>
          {{ selectedWorker?.full_name }} – Balans tarixi
        </v-card-title>
        <v-card-text>
          <v-data-table
            :headers="historyHeaders"
            :items="transactions"
            :items-per-page="10"
          >
            <template #item.amount="{ item }">
              <span :class="item.amount >= 0 ? 'text-success' : 'text-error'">
                {{ item.amount.toLocaleString() }} so‘m
              </span>
            </template>
            <template #item.created_at="{ item }">
              {{ new Date(item.created_at).toLocaleString() }}
            </template>
          </v-data-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="historyDialog = false">Yopish</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 💸 To‘ldirish modali -->
    <v-dialog v-model="topupDialog" max-width="500">
      <v-card>
        <v-card-title>
          {{ selectedWorker?.full_name }} – Balans to‘ldirish
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submitTopup">
            <v-text-field v-model="topupAmount" label="Miqdor (so‘m)" type="number" required />
            <v-text-field v-model="topupDescription" label="Izoh" required />
            <v-btn type="submit" color="success" class="mt-3">Saqlash</v-btn>
            <v-btn class="mt-3 ms-2" @click="topupDialog = false">Bekor</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const workers = ref([])
const transactions = ref([])

const historyDialog = ref(false)
const topupDialog = ref(false)

const selectedWorker = ref(null)

const topupAmount = ref(null)
const topupDescription = ref('')

const headers = [
  { title: 'Usta', key: 'full_name' },
  { title: 'Balans', key: 'balance' },
  { title: 'Amallar', key: 'actions', sortable: false }
]

const historyHeaders = [
  { title: 'Sana', key: 'created_at' },
  { title: 'Izoh', key: 'description' },
  { title: 'Miqdor', key: 'amount' }
]

const fetchWorkers = async () => {
  const res = await axios.get('https://halboldi.uz/api/workers/')
  workers.value = res.data
}

const openHistory = async (worker) => {
  selectedWorker.value = worker
  const res = await axios.get(`https://halboldi.uz/api/balance-transactions/?worker=${worker.id}`)
  transactions.value = res.data
  historyDialog.value = true
}

const openTopup = (worker) => {
  selectedWorker.value = worker
  topupAmount.value = null
  topupDescription.value = ''
  topupDialog.value = true
}

const submitTopup = async () => {
  if (!topupAmount.value || !topupDescription.value || !selectedWorker.value) return

  try {
    await axios.post('https://halboldi.uz/api/balance-transactions/', {
      worker: selectedWorker.value.id,
      amount: parseFloat(topupAmount.value),
      description: topupDescription.value
    })

    topupDialog.value = false
    fetchWorkers()
  } catch (err) {
    console.error("To‘ldirishda xatolik:", err)
  }
}

onMounted(() => {
  fetchWorkers()
})
</script>

<style scoped>
.text-success {
  color: green;
}
.text-error {
  color: red;
}
</style>
