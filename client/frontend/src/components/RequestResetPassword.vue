<template>
  <v-form @submit.prevent="requestPasswordReset" v-model="valid">
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

      <v-card class="mb-12" color="surface-variant" variant="tonal">
        <v-card-text class="text-medium-emphasis text-caption">
          We will send you an email containing a link with which you can reset
          your password.
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
        Reset Password
      </v-btn>
      <v-btn
        @click="$emit('cancel')"
        block
        class="mb-8"
        color="secondary"
        size="large"
        variant="tonal"
      >
        Cancel
      </v-btn>
    </v-card>
  </v-form>
</template>
<script>
import axios from "@/libs/axios";
import { emailRules } from "@/libs/form-rules";
import { useMainStore } from "@/stores/main";

export default {
  data() {
    return {
      valid: false,
      rules: {
        email: emailRules,
      },
      user: {
        email: "",
      },
      mainStore: null,
    };
  },
  created() {
    this.mainStore = useMainStore();
  },
  methods: {
    requestPasswordReset() {
      axios
        .post("/api/v1/auth/request-password-reset/", {
          email: this.user.email,
        })
        .then(() => {
          this.mainStore.handleSuccess(
            "Email with the reset link has been sent."
          );
        })
        .catch((error) => {
          this.mainStore.handleError(error.response.data);
        });
    },
  },
};
</script>
