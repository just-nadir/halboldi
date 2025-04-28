<template>
  <v-app>
    <!-- Sidebar -->
    <v-navigation-drawer app width="220">
      <v-list nav dense>
        <v-list-item-title class="text-h6 text-center my-4">
          Ustalarni boshqarish
        </v-list-item-title>
        <v-divider class="mb-2" />

        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.route"
          link
        >
          <!-- <v-list-item-icon> o‘rniga ishlaydigan to‘g‘ri yechim -->
          <template #prepend>
            <v-icon>{{ item.icon }}</v-icon>
          </template>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Sahifa kontenti -->
    <v-main>
      <v-container class="mt-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
const menuItems = [
  { title: 'Asosiy', route: '/', icon: 'mdi-home' },
  { title: 'Buyurtmalar', route: '/orders', icon: 'mdi-format-list-bulleted' },
  { title: 'Ustalar', route: '/workers', icon: 'mdi-account-group' },
  { title: 'Ishlar', route: '/jobs', icon: 'mdi-hammer-wrench' },
  { title: 'Balans tarixi', route: '/balance', icon: 'mdi-cash' },
  { title: 'SMS loglari', route: '/sms-logs', icon: 'mdi-message' },
  { title: 'Bekor qilinganlar', route: '/cancelled-orders', icon: 'mdi-cancel' },
  { title: 'Hisobotlar', route: '/reports', icon: 'mdi-chart-line' }
]
</script>
