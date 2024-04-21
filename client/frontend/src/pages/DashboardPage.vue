<template>
  <div>
    <h1>Vital Signs</h1>
  </div>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Pulse">
        <PulseAreaChart></PulseAreaChart>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Blood Pressure">
        <BloodPressureAreaChart></BloodPressureAreaChart>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Weight">
        <WeightAreaChart></WeightAreaChart>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Temperature">
        <TemperatureAreaChart></TemperatureAreaChart>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col col="6">
      <v-card class="pa-5" title="Vital Signs">
        <PieChart1></PieChart1>
      </v-card>
    </v-col>
    <v-col col="6">
      <v-card class="pa-5" title="Labs">
        <PieChart2></PieChart2>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import PieChart1 from '../components/charts/PieChart1.vue';
import PieChart2 from '../components/charts/PieChart2.vue';
import PulseAreaChart from '../components/charts/PulseAreaChart.vue';
import BloodPressureAreaChart from '../components/charts/BloodPressureAreaChart.vue';
import WeightAreaChart from '../components/charts/WeightAreaChart.vue';
import TemperatureAreaChart from '../components/charts/TemperatureAreaChart.vue';

export default {
  components: {
    PieChart1,
    PieChart2,
    PulseAreaChart,
    BloodPressureAreaChart,
    WeightAreaChart,
    TemperatureAreaChart,
  },
  data() {
    return {
      epicData: [],
    };
  },
};
</script>
