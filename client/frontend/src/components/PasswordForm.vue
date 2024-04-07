<template>
  <v-avatar class="mx-auto mt-4" color="tertiary" size="65">
    <span class="text-h4">
      {{ initials }}
    </span>
  </v-avatar>
  <v-container style="max-width: 400px">
    <v-form @submit.prevent="submitForm">
      <v-text-field
        v-model="username"
        disabled
        label="Username"
        :readonly="true"
      ></v-text-field>
      <v-text-field
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :type="passwordVisible ? 'text' : 'password'"
        @click:append-inner="passwordVisible = !passwordVisible"
        v-model="data.old_password"
        label="Old Password"
        color="primary"
        :rules="rules.password1"
      ></v-text-field>
      <v-text-field
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :type="passwordVisible ? 'text' : 'password'"
        @click:append-inner="passwordVisible = !passwordVisible"
        v-model="data.new_password1"
        label="New Password"
        color="primary"
        :rules="rules.password1"
      ></v-text-field>
      <v-text-field
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :type="passwordVisible ? 'text' : 'password'"
        @click:append-inner="passwordVisible = !passwordVisible"
        v-model="data.new_password2"
        label="Repeat New Password"
        color="primary"
        :rules="rules.password2"
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
import { computed, ref } from "vue";
import axios from "axios";
import { basicRule, passwordRules, password2Rules } from "@/libs/form-rules";
import { useMainStore } from "@/stores/main";
import { getInitials } from "@/libs/utils";

const passwordVisible = ref(false);
const rules = computed(() => ({
  basic: basicRule,
  password1: passwordRules,
  password2: password2Rules(data.value.new_password1, data.value.new_password2),
}));

const props = defineProps({
  user: Object,
});
const username = ref(props.user.username);
const initials = getInitials(props.user.firstName, props.user.lastName);

const data = ref({
  old_password: "",
  new_password1: "",
  new_password2: "",
});
const mainStore = useMainStore();
const emit = defineEmits(["submit", "cancel"]);
async function submitForm() {
  await axios
    .post("/api/v1/auth/password/change/", data.value)
    .then(() => {
      mainStore.handleSuccess("Password has been changed");
      emit("submit");
    })
    .catch((error) => {
      mainStore.handleError(error.response.data);
    });
}
</script>
