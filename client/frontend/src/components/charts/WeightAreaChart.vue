<template>
  <v-skeleton-loader
    v-if="!epicData.length"
    class="mx-auto border"
    max-width="800"
    type="table-tbody"
  ></v-skeleton-loader>
  <v-chart v-else class="chart" :option="option" autoresize />
</template>

<script setup>
import { ref, onMounted, watchEffect, provide, computed } from 'vue';
import { useTheme } from 'vuetify';
import VChart, { THEME_KEY } from 'vue-echarts';
import { use } from 'echarts/core';
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

import axios from 'axios';
import Cookies from 'js-cookie';
use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition,
]);

const option = ref({});
const epicData = ref([]);
const appTheme = useTheme();
const chartTheme = computed(() =>
  appTheme.global.current.value.dark ? 'dark' : 'light'
);
provide(THEME_KEY, chartTheme);

watchEffect(() => {
  updateChartOptions(chartTheme.value);
});

const loadObservations = async () => {
  const epicAccessToken = Cookies.get('epic_access_token');
  if (epicAccessToken) {
    try {
      const response = await axios.get(
        `${
          import.meta.env.VITE_FHIR_BASE_URL
        }/Observation?category=vital-signs`,
        {
          headers: {
            Authorization: `Bearer ${epicAccessToken}`,
          },
        }
      );

      response.data.entry.forEach((vitalSign) => {
        const vitalSignTitle = vitalSign.resource.code?.text;
        const unit = vitalSign.resource.valueQuantity?.unit;

        if (vitalSignTitle && vitalSignTitle === 'Weight' && unit === 'kg') {
          const value = vitalSign.resource.valueQuantity?.value;
          epicData.value.push(value);
        }
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  } else {
    console.error('epicAccessToken not found');
  }
};

function updateChartOptions(theme) {
  option.value = {
    title: {
      // text: "Title of the chart",
    },
    backgroundColor: theme === 'dark' ? 'black' : null,
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985',
        },
      },
    },
    legend: {
      data: ['kg'],
    },
    toolbox: {
      feature: {
        saveAsImage: {},
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: [
      {
        type: 'category',
        boundaryGap: false,
      },
    ],
    yAxis: [
      {
        type: 'value',
      },
    ],
    series: [
      {
        name: 'kg',
        type: 'line',
        stack: 'Total',
        emphasis: {
          focus: 'series',
        },
        data: epicData.value,
        itemStyle: {
          color: '#ADD8E6', // Light blue color in hex (Light Blue)
        },
        lineStyle: {
          color: '#ADD8E6', // Light blue color in hex (Light Blue)
        },
        areaStyle: {
          color: 'rgba(173, 216, 230, 0.75)', // Light blue color with 75% opacity
        },
      },
    ],
  };
}

onMounted(() => {
  loadObservations();
});
</script>

<style scoped>
.chart {
  height: 30vh;
}
</style>
