<template>
  <div class="glass rounded-2xl p-6">
    <h3 class="text-lg font-semibold">Category Momentum</h3>
    <Radar v-if="chartData" :data="chartData" :options="chartOptions" class="mt-4" />
    <p v-else class="mt-4 text-sm text-fog/60">Not enough data for chart yet.</p>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { Radar } from "vue-chartjs";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const props = defineProps({
  stats: {
    type: Array,
    default: () => [],
  },
});

const chartData = computed(() => {
  if (!props.stats.length) return null;

  const categories = [...new Set(props.stats.map((stat) => stat.category))];
  const playerA = categories.map((category) =>
    averageMetric(props.stats.filter((stat) => stat.category === category), "playerAValue")
  );
  const playerB = categories.map((category) =>
    averageMetric(props.stats.filter((stat) => stat.category === category), "playerBValue")
  );

  return {
    labels: categories,
    datasets: [
      {
        label: "Player A",
        data: playerA,
        backgroundColor: "rgba(249, 115, 22, 0.25)",
        borderColor: "rgba(249, 115, 22, 0.8)",
        pointBackgroundColor: "rgba(249, 115, 22, 1)",
      },
      {
        label: "Player B",
        data: playerB,
        backgroundColor: "rgba(14, 165, 164, 0.25)",
        borderColor: "rgba(14, 165, 164, 0.8)",
        pointBackgroundColor: "rgba(14, 165, 164, 1)",
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      labels: {
        color: "#e2e8f0",
      },
    },
  },
  scales: {
    r: {
      angleLines: { color: "rgba(226, 232, 240, 0.2)" },
      grid: { color: "rgba(226, 232, 240, 0.15)" },
      pointLabels: { color: "#e2e8f0" },
      ticks: { display: false },
    },
  },
};

function averageMetric(list, key) {
  if (!list.length) return 0;
  const sum = list.reduce((acc, stat) => acc + Number(stat[key] || 0), 0);
  return Number((sum / list.length).toFixed(2));
}
</script>
