<template>
  <v-avatar class="mx-auto mt-4" color="tertiary" size="65">
    <span class="text-h4">
      {{ initials }}
    </span>
  </v-avatar>

  <v-container style="max-width: 400px">
    <v-form @submit.prevent="submitForm">
      <v-text-field v-model="data.first_name" label="First name"></v-text-field>
      <v-text-field v-model="data.last_name" label="Last name"></v-text-field>
      <v-text-field
        v-model="username"
        :disabled="true"
        label="Username"
        :readonly="true"
      ></v-text-field>
      <v-text-field
        v-model="email"
        :disabled="true"
        label="Email"
        :readonly="true"
      ></v-text-field>
      <v-text-field
        v-if="userType"
        v-model="userType"
        label="User type"
        :disabled="true"
        :readonly="true"
      ></v-text-field>
      <div class="d-flex justify-between">
        <v-btn color="secondary" variant="tonal" @click="$emit('cancel')"
          >Cancel</v-btn
        >
        <v-spacer></v-spacer>
        <v-btn type="submit" color="tertiary">Submit</v-btn>
      </div>
    </v-form>
  </v-container>
</template>

<script setup>
import { useMainStore } from "@/stores/main";
import { computed, ref } from "vue";
import axios from "axios";
import { getInitials, getUserType } from "@/libs/utils";

const props = defineProps({
  user: Object,
});
const username = ref(props.user.username);
const email = ref(props.user.email);
const userType = ref(getUserType(props.user));

const data = ref({
  first_name: props.user.firstName,
  last_name: props.user.lastName,
});
const initials = computed(() => {
  return getInitials(data.value.first_name, data.value.last_name);
});
const mainStore = useMainStore();
const emit = defineEmits(["submit", "cancel"]);
async function submitForm() {
  const res = await axios.patch("/api/v1/user/", data.value);
  if (res.status === 200) {
    mainStore.user.firstName = res.data.first_name;
    mainStore.user.lastName = res.data.last_name;
    emit("submit");
  }
}
</script>
