<template>
  <v-app>
    <router-view v-if="$route.meta.isPublic"></router-view>
    <StandardLayout v-else-if="mainStore.isAuthenticated" />
    <DefaultPublicPage v-else-if="mainStore.appInitialized" />
    <v-snackbar
      multi-line
      v-model="mainStore.snackbar.show"
      :color="mainStore.snackbar.color"
      variant="tonal"
      rounded="pill"
      :timeout="mainStore.snackbar.timeout"
    >
      <div class="d-flex flex-row align-center">
        <v-icon class="mr-2"> {{ mainStore.snackbar.icon }}</v-icon>
        <!-- using innerHTML so <br> inside snackbar.message creates new line -->
        <p :innerHTML="mainStore.snackbar.message"></p>
      </div>
      <template v-slot:actions>
        <v-btn :color="mainStore.snackbar.color" variant="text" @click="mainStore.closeSnackbar()">
          <v-icon class="mr-2">mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { useMainStore } from '@/stores/main'
import DefaultPublicPage from '@/pages/DefaultPublicPage.vue'
import StandardLayout from '@/pages/StandardLayout.vue'
import { onBeforeMount, onMounted } from 'vue'
const mainStore = useMainStore()

onBeforeMount(() => {
  mainStore.initializeApp()
})
onMounted(() => {
  setInterval(() => {
    if (mainStore.isAuthenticated) {
      mainStore.refreshAccessToken()
    }
  }, 1000 * 60 * 4)
  setInterval(() => {
    mainStore.setCsrfToken()
  }, 1000 * 60 * 25)
})
</script>
