<template>
  <v-container>
    <v-row justify="space-between" align="center">
      <h2>Ustalar ro'yxati</h2>
      <v-btn color="primary" @click="showAddDialog = true">+ Usta qo‘shish</v-btn>
    </v-row>

    <!-- Jadval -->
    <v-data-table
      :headers="headers"
      :items="workers"
      :items-per-page="10"
      class="mt-4"
    >
      <template #item.specialties="{ item }">
        {{ item.specialties?.split(',').join(', ') }}
      </template>

      <template #item.actions="{ item }">
        <v-icon small color="primary" class="me-2" @click="openEditDialog(item)">
          mdi-pencil
        </v-icon>
        <v-icon small color="red" @click="deleteWorker(item.id)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>

    <!-- Qo‘shish formasi -->
    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card>
        <v-card-title>Yangi usta qo‘shish</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submitForm">
            <v-text-field label="Ism" v-model="form.full_name" required />
            <v-text-field label="Mutaxassisliklar" v-model="form.specialties" required />
            <v-text-field label="Telefon" v-model="form.phone" required />
            <v-text-field label="Tug‘ilgan sana" type="date" v-model="form.birth_date" required />
            <v-text-field label="Tajriba (yil)" type="number" v-model="form.experience" required />
            <v-btn type="submit" color="success" class="mt-3">Saqlash</v-btn>
            <v-btn class="mt-3 ms-2" @click="showAddDialog = false">Bekor</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Tahrirlash formasi -->
    <v-dialog v-model="editDialog" max-width="500">
      <v-card>
        <v-card-title>Ustani tahrirlash</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="updateWorker">
            <v-text-field label="Ism" v-model="editForm.full_name" required />
            <v-text-field label="Mutaxassisliklar" v-model="editForm.specialties" required />
            <v-text-field label="Telefon" v-model="editForm.phone" required />
            <v-text-field label="Tug‘ilgan sana" type="date" v-model="editForm.birth_date" required />
            <v-text-field label="Tajriba (yil)" type="number" v-model="editForm.experience" required />
            <v-btn type="submit" color="primary" class="mt-3">Yangilash</v-btn>
            <v-btn class="mt-3 ms-2" @click="editDialog = false">Bekor</v-btn>
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
const showAddDialog = ref(false)
const editDialog = ref(false)

const form = ref({
  full_name: '',
  specialties: '',
  phone: '',
  birth_date: '',
  experience: 0
})

const editForm = ref({
  id: null,
  full_name: '',
  specialties: '',
  phone: '',
  birth_date: '',
  experience: 0
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Ism', key: 'full_name' },
  { title: 'Mutaxassisliklar', key: 'specialties' },
  { title: 'Yosh', key: 'age' },
  { title: 'Telefon', key: 'phone' },
  { title: 'Tajriba (yil)', key: 'experience' },
  { title: 'Reyting', key: 'rating' },
  { title: 'Balans', key: 'balance' },
  { title: 'Amallar', key: 'actions', sortable: false }
]

const fetchWorkers = async () => {
  try {
    const res = await axios.get('https://halboldi.uz/api/workers/')
    workers.value = res.data
  } catch (error) {
    console.error('Xatolik:', error)
  }
}

const submitForm = async () => {
  try {
    await axios.post('https://halboldi.uz/api/workers/', form.value)
    showAddDialog.value = false
    form.value = {
      full_name: '',
      specialties: '',
      phone: '',
      birth_date: '',
      experience: 0
    }
    fetchWorkers()
  } catch (error) {
    console.error('Usta qo‘shishda xatolik:', error)
  }
}

const openEditDialog = (item) => {
  editForm.value = { ...item }
  editDialog.value = true
}

const updateWorker = async () => {
  try {
    await axios.put(`https://halboldi.uz/api/workers/${editForm.value.id}/`, editForm.value)
    editDialog.value = false
    fetchWorkers()
  } catch (error) {
    console.error('Tahrirlashda xatolik:', error)
  }
}

const deleteWorker = async (id) => {
  if (confirm('Rostdan ham o‘chirmoqchimisiz?')) {
    try {
      await axios.delete(`https://halboldi.uz/api/workers/${id}/`)
      fetchWorkers()
    } catch (error) {
      console.error('O‘chirishda xatolik:', error)
    }
  }
}

onMounted(() => {
  fetchWorkers()
})
</script>
