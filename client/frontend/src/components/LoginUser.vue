<template>
  <v-form @submit.prevent="logIn" v-model="valid">
    <v-card class="mx-auto pa-12 pb-8" variant="text">
      <div class="text-subtitle-1 text-medium-emphasis">Account</div>

      <v-text-field
        v-model="user.email"
        density="compact"
        placeholder="Email address"
        prepend-inner-icon="mdi-email-outline"
        variant="outlined"
        color="primary"
        :rules="rules.email"
      ></v-text-field>

      <div
        class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between"
      >
        Password
      </div>

      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye' : 'mdi-eye-off'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="Enter your password"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        v-model="user.password"
        color="primary"
        @click:append-inner="visible = !visible"
        :rules="rules.basic"
      ></v-text-field>

      <v-card class="mb-12" color="surface-variant" variant="tonal">
        <v-card-text class="text-medium-emphasis text-caption">
          <span>
            If you have forgotten your password, you can reset your password
          </span>
          <a href="#" @click="$emit('reset-password')">here</a>
          <span>.</span>
        </v-card-text>
      </v-card>

      <v-btn
        block
        type="submit"
        class="mb-8"
        color="tertiary"
        size="large"
        variant="tonal"
        :disabled="!valid"
      >
        Log In
      </v-btn>
    </v-card>
  </v-form>
</template>
<script>
import axios from "@/libs/axios";
import { useMainStore } from "@/stores/main";
import { basicRule, emailRules } from "@/libs/form-rules";

export default {
  data: function () {
    return {
      visible: false,
      valid: false,
      user: {
        email: "",
        password: "",
      },
      mainStore: null,
      rules: {
        basic: basicRule,
        email: emailRules,
      },
    };
  },
  created() {
    this.mainStore = useMainStore();
  },

  methods: {
    logIn() {
      this.mainStore.closeSnackbar();
      axios
        .post("/api/v1/auth/login/", {
          email: this.user.email,
          password: this.user.password,
        })
        .then(() => {
          this.mainStore.authenticate();
          this.mainStore.loadData();
        })
        .catch((error) => {
          this.mainStore.handleError(error.response.data);
        });
    },
  },
};
</script>
