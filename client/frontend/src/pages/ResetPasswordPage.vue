<template>
  <v-main class="d-flex flex-column align-center">
    <h1>reset password page</h1>
    <v-card width="450">
      <v-tabs v-model="tab" color="tertiary" bg-color="primary">
        <v-tab value="reset-password">Reset Password</v-tab>
      </v-tabs>
      <v-card-text>
        <v-window v-model="tab">
          <v-window-item value="reset-password">
            <ResetPassword />
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </v-main>
</template>

<script>
import ResetPassword from "@/components/ResetPassword.vue";

export default {
  components: { ResetPassword },
  data: () => ({
    tab: "reset-password",
  }),
};
</script>
