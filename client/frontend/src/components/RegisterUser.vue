<template>
  <v-form @submit.prevent="register" v-model="valid">
    <v-card class="mx-auto pa-12 pb-8" variant="text" title="Register new user">
      <v-text-field
        v-model="user.email"
        label="Email"
        color="primary"
        variant="underlined"
        :rules="rules.email"
      ></v-text-field>

      <v-text-field
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :type="passwordVisible ? 'text' : 'password'"
        @click:append-inner="passwordVisible = !passwordVisible"
        v-model="user.password1"
        label="Password"
        color="primary"
        variant="underlined"
        :rules="rules.password1"
      ></v-text-field>

      <v-text-field
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :type="passwordVisible ? 'text' : 'password'"
        @click:append-inner="passwordVisible = !passwordVisible"
        v-model="user.password2"
        label="Repeat Password"
        color="primary"
        variant="underlined"
        :rules="rules.password2"
      ></v-text-field>

      <v-card class="mb-6" color="surface-variant" variant="tonal">
        <v-card-text class="text-medium-emphasis text-caption">
          We will send you an email with a link to confirm your email address.
        </v-card-text>
      </v-card>
      <v-checkbox
        v-model="user.terms"
        color="primary"
        active-color="primary"
        :rules="rules.terms"
      >
        <template #label>
          I agree to site&nbsp;
          <a href="http://www.example.com/" target="_blank">
            terms and conditions</a
          >
        </template>
      </v-checkbox>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          block
          type="submit"
          class="mb-8"
          color="tertiary"
          size="large"
          variant="tonal"
          :disabled="!valid"
        >
          Complete Registration
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import axios from "@/libs/axios";
import { emailRules, passwordRules, password2Rules } from "@/libs/form-rules";
import { useMainStore } from "@/stores/main";

export default {
  data() {
    return {
      valid: false,
      // When the user types into a field, Vuetify checks whether the input meets all the validation rules defined in `:rules`.
      // If all the fields are valid, Vuetify sets the value of `valid` to true.
      // If any field is invalid, Vuetify sets the value of `valid` to false.

      user: {
        email: "",
        password1: "",
        password2: "",
        terms: false,
      },
      passwordVisible: false,
      mainStore: null,
    };
  },
  created() {
    this.mainStore = useMainStore();
  },
  computed: {
    rules() {
      return {
        email: emailRules,
        password1: passwordRules,
        password2: password2Rules(this.user.password1, this.user.password2),
        terms: [
          (v) => !!v || "Agreeing to the terms and conditions is required",
        ],
      };
    },
  },

  methods: {
    async register() {
      this.mainStore.closeSnackbar();
      axios
        .post("/api/v1/auth/registration/", {
          email: this.user.email,
          username: this.user.email,
          password1: this.user.password1,
          password2: this.user.password2,
        })
        .then(() => {
          this.mainStore.handleSuccess(
            "Registration successful. Please confirm your email before you can log in."
          );
        })
        .catch((error) => {
          this.mainStore.handleError(error.response.data);
        });
    },
  },
};
</script>
