<template>
  <v-chart class="chart" :option="option" autoresize />
</template>

<script setup>
import { ref, watchEffect, provide, computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart } from 'echarts/charts';
import { TooltipComponent, LegendComponent } from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import { useTheme } from 'vuetify';

use([CanvasRenderer, PieChart, TooltipComponent, LegendComponent]);

const option = ref({});
const appTheme = useTheme();
const chartTheme = computed(() =>
  appTheme.global.current.value.dark ? 'dark' : 'light'
);
provide(THEME_KEY, chartTheme);

watchEffect(() => {
  updateChartOptions(chartTheme.value);
});

function updateChartOptions(theme) {
  option.value = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)',
    },
    backgroundColor: theme === 'dark' ? 'black' : null,
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: 'Customer Sources',
        type: 'pie',
        radius: '70%',
        center: ['60%', '40%'],
        data: [
          { value: 335, name: 'Direct' },
          { value: 310, name: 'Email' },
          { value: 234, name: 'Ad Networks' },
        ],
        color: [
          '#80BCBD', // Color for 'Direct'
          '#AAD9BB', // Color for 'Email'
          '#F9F7C9', // Color for 'Ad Networks'
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  };
}
</script>

<style scoped>
.chart {
  height: 30vh;
}
</style>
