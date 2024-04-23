<template>
  <div class="text-center pa-4">
    <v-dialog v-model="syncEpicDialog" width="auto">
      <v-card
        max-width="400"
        prepend-icon="mdi-cloud-alert"
        text="In order to see your data here please give a consent to this application to fetch your data stored in Epic."
        title="Data not available"
      >
        <template v-slot:actions>
          <v-btn
            color="secondary"
            variant="flat"
            @click="syncEpicDialog = false"
            >No, thanks</v-btn
          >
          <v-spacer></v-spacer>
          <v-btn color="tertiary" variant="tonal" @click="redirectToUrl"
            >Lets do it!</v-btn
          >
        </template>
      </v-card>
    </v-dialog>

    <v-dialog v-model="waitDialog" width="auto" persistent>
      <v-card
        max-width="800"
        class="d-flex flex-column align-center justify-center"
        prepend-icon="mdi-cloud-alert"
        text="Please wait until the process finishes."
        title="Authorization in progress..."
      >
        <v-progress-circular
          :size="70"
          :width="7"
          color="secondary"
          indeterminate
          class="my-4"
        ></v-progress-circular>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import getPkce from 'oauth-pkce';
import axios from '@/libs/axios';
import { useMainStore } from '@/stores/main';
import { mapActions } from 'pinia';

export default {
  data() {
    return {
      waitDialog: false,
      syncEpicDialog: false,
    };
  },
  methods: {
    ...mapActions(useMainStore, ['loadEpicData']),
    decideWhatToDo() {
      let access_token = Cookies.get('epic_access_token');
      if (access_token) {
        this.$router.push({ name: 'home-page' });
      } else {
        if (this.$route.query.code) {
          this.waitDialog = true;
          this.exchangeCodeForToken(this.$route.query.code);
        } else {
          this.syncEpicDialog = true;
        }
      }
    },
    async exchangeCodeForToken(code) {
      // this token_endpoint has CORS policy set to allow any domain so I can call that enpoint from javascript and read the content.
      // Documentation: The app issues an HTTP POST to the EHR authorization server’s token endpoint URL using content-type application/x-www-form-urlencoded
      // my notes: When making an HTTP request with a content type of application/x-www-form-urlencoded, the body of the request must be a URL-encoded string. Axios by default sends JavaScript objects as JSON. So in this case because I need to send the data in application/x-www-form-urlencoded format, I must convert the URLSearchParams object to a string using .toString() and set the correct Content-Type header manually to application/x-www-form-urlencoded.
      try {
        // URLSearchParams is a utility provided by modern web browsers that makes it easier to construct URL query strings.
        const params = new URLSearchParams({
          code: code,
          client_id: import.meta.env.VITE_CLIENT_ID,
          redirect_uri: import.meta.env.VITE_REDIRECT_URI,
          grant_type: 'authorization_code',
          code_verifier: Cookies.get('code_verifier'),
        });
        let resp = await axios.post(
          import.meta.env.VITE_TOKEN_ENDPOINT,
          // The parameters are first converted to a URL-encoded string using params.toString() and then sent in the body of the request.
          params.toString(),
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          }
        );
        if (resp.status === 200) {
          Cookies.set('epic_access_token', resp.data.access_token, {
            // expires: 1 / 24 / 60, // expires in 1 minute for testing purposess
            expires: (1 / 24 / 60 / 60) * resp.data.expires_in,
            path: '/',
            SameSite: "Strict"
          });
          await this.loadEpicData();
          this.waitDialog = false;
          this.$router.push({ name: 'home-page' });
        } else {
          console.error('Failed to fetch token:', resp.status, resp.data);
        }
      } catch (error) {
        console.error('Error during token exchange:', error);
      }
    },
    getPkcePromise(length) {
      return new Promise((resolve, reject) => {
        getPkce(length, (error, data) => {
          if (error) {
            reject(error);
          } else {
            resolve(data);
          }
        });
      });
    },

    async buildUrl() {
      // needs to be async because of the promise getPkcePromise
      try {
        const { verifier, challenge } = await this.getPkcePromise(43);

        Cookies.set('code_verifier', verifier, {
          expires: 7,
          path: '/smart-auth',
          SameSite: "Strict"
        });

        // Create a URL object from the authorization endpoint
        const url = new URL(import.meta.env.VITE_AUTHORIZATION_ENDPOINT);

        // Set up URL parameters
        const params = new URLSearchParams({
          response_type: import.meta.env.VITE_RESPONSE_TYPE,
          client_id: import.meta.env.VITE_CLIENT_ID,
          redirect_uri: import.meta.env.VITE_REDIRECT_URI,
          state: import.meta.env.VITE_STATE,
          scope: import.meta.env.VITE_SCOPE,
          aud: import.meta.env.VITE_FHIR_BASE_URL,
          code_challenge: challenge,
          code_challenge_method: 'S256',
        });

        // Append the parameters to the URL (the `search` property of the URL object will become the query string in the url)
        url.search = params.toString();

        // Return the full URL
        return url.toString();
      } catch (error) {
        console.error('Failed to generate PKCE:', error);
      }
    },
    async redirectToUrl() {
      // Change the window's location to the URL
      const url = await this.buildUrl();
      window.location.href = url;
    },
  },
  mounted() {
    this.decideWhatToDo();
  },
};
</script>
