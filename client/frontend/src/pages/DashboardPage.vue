<template>
  <div>
    <h1>Dashboard</h1>
  </div>
  <v-row>
    <v-col col="6">
      <v-card class="pa-5" title="Vital Signs">
        <v-skeleton-loader
          v-if="!epicData.length"
          class="mx-auto border"
          max-width="300"
          type="image, article"
        ></v-skeleton-loader>
        <PieChart1 v-else></PieChart1>
      </v-card>
    </v-col>
    <v-col col="6">
      <v-card class="pa-5" title="Labs">
        <v-skeleton-loader
          v-if="!epicData.length"
          class="mx-auto border"
          max-width="300"
          type="image, article"
        ></v-skeleton-loader>
        <PieChart2 v-else></PieChart2>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Medications">
        <v-skeleton-loader
          v-if="!epicData.length"
          class="mx-auto border"
          max-width="300"
          type="image, article"
        ></v-skeleton-loader>
        <StackedAreaChart v-else></StackedAreaChart>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import Cookies from 'js-cookie';
import PieChart1 from '../components/charts/PieChart1.vue';
import PieChart2 from '../components/charts/PieChart2.vue';
import StackedAreaChart from '../components/charts/StackedAreaChart.vue';
import axios from '@/libs/axios';

export default {
  components: {
    PieChart1,
    PieChart2,
    StackedAreaChart,
  },
  data() {
    return {
      epicData: [],
    };
  },
  methods: {
    async fetchEpicData() {
      const epicAccessToken = Cookies.get('epic_access_token');
      console.log('fetchEpicData called');
      if (epicAccessToken) {
        axios
          .get(import.meta.env.VITE_FHIR_BASE_URL + '/Patient', {
            headers: {
              Authorization: `Bearer ${epicAccessToken}`,
            },
          })
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });
      } else {
        console.error('epicAccessToken not found');
      }
    },
  },
  mounted() {
    console.log('onMounted called');
    this.fetchEpicData();
  },
};
</script>
