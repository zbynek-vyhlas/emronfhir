<template>
  <v-avatar class="mx-auto mt-4" color="tertiary" size="65">
    <span class="text-h4">
      {{ initials }}
    </span>
  </v-avatar>
  <v-container>
    <div class="text-h5 mt-6 name">
      {{ user.firstName }} {{ user.lastName }}
    </div>

    <div class="text-h7 email">{{ user.email }}</div>
    <div class="text-h6 mt-3">{{ getUserType(user) }}</div>

    <v-divider class="mt-8"></v-divider>

    <div class="d-flex justify-end">
      <v-btn @click="$emit('edit', 'password')" variant="text" color="secondary"
        >Change Password</v-btn
      >
      <v-spacer> </v-spacer>
      <v-btn @click="$emit('edit', 'profile')" variant="text" color="tertiary"
        >Edit Account</v-btn
      >
    </div>
  </v-container>
</template>
<script setup>
import { computed } from 'vue';
import { getInitials, getUserType } from '@/libs/utils';

const props = defineProps({
  user: Object,
});
defineEmits(['edit']);

const initials = computed(() => {
  return getInitials(props.user.firstName, props.user.lastName);
});
</script>
