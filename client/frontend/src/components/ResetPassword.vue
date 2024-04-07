<template>
  <v-form v-if="queryParamsOk" @submit.prevent="resetPassword" v-model="valid">
    <v-card class="mx-auto pa-12 pb-8" variant="text">
      <div class="text-subtitle-1 text-medium-emphasis">Account</div>

      <v-text-field
        v-model="user.username"
        density="compact"
        variant="outlined"
        color="primary"
        :disabled="true"
        :readonly="true"
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis">New Password</div>
      <v-text-field
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :type="passwordVisible ? 'text' : 'password'"
        density="compact"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        v-model="user.password1"
        color="primary"
        @click:append-inner="passwordVisible = !passwordVisible"
        :rules="rules.password1"
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis">
        Repeat New Password
      </div>
      <v-text-field
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :type="passwordVisible ? 'text' : 'password'"
        density="compact"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        v-model="user.password2"
        color="primary"
        @click:append-inner="passwordVisible = !passwordVisible"
        :rules="rules.password2"
      ></v-text-field>

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
        :to="{ name: 'home-page' }"
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
  <v-card v-else>
    <v-alert title="Problem with a password resetting link">
      The link by which you are attempting to reset your password is not valid.
      If you came here by accident, you can ignore this. If you are sure that
      you have the correct link, please get in contact with us.</v-alert
    >
    <v-btn
      :to="{ name: 'home-page' }"
      block
      class="mb-2 mt-4"
      color="secondary"
      size="large"
      variant="tonal"
    >
      Cancel
    </v-btn>
  </v-card>
</template>
<script>
import axios from "@/libs/axios";
import { passwordRules, password2Rules } from "@/libs/form-rules";
import { useMainStore } from "@/stores/main";

export default {
  data() {
    return {
      valid: false,
      passwordVisible: false,
      mainStore: null,
      user: {
        username: "",
        password1: "",
        password2: "",
        uid: "",
        token: "",
      },
    };
  },
  created() {
    this.mainStore = useMainStore();
    this.user.username = this.$route.query.username;
    this.user.uid = this.$route.query.uid;
    this.user.token = this.$route.query.token;
  },
  computed: {
    queryParamsOk() {
      return !!this.user.username && !!this.user.uid && !!this.user.token;
    },
    rules() {
      return {
        password1: passwordRules,
        password2: password2Rules(this.user.password1, this.user.password2),
      };
    },
  },
  methods: {
    resetPassword() {
      axios
        .post(`/api/v1/auth/reset-password/`, {
          uid: this.user.uid,
          token: this.user.token,
          new_password1: this.user.password1,
          new_password2: this.user.password2,
        })
        .then(() => {
          this.mainStore.handleSuccess("Password has been reset.");
          this.$router.push({ name: "home-page" });
        })
        .catch((error) => {
          this.mainStore.handleError(error.response.data);
        });
    },
  },
};
</script>
