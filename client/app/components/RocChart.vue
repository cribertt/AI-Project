<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

// 🔥 Registro obligatorio de escalas y elementos
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
)

const props = defineProps({
  fpr: Array, // false positive rate
  tpr: Array, // true positive rate
  auc: Number
})
</script>

<template>
  <div class="bg-white shadow rounded-2xl p-6" style="height: 400px;">
    <Line
      :data="{
        labels: fpr,
        datasets: [{
          label: 'ROC Curve',
          data: tpr,
          borderColor: '#16a34a',
          tension: 0.3,
          fill: false
        }]
      }"
      :options="{
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { type: 'linear', min: 0, max: 1 },
          y: { type: 'linear', min: 0, max: 1 }
        }
      }"
    />
  </div>
</template>
