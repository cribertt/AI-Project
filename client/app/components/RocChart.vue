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

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps({
  fpr: Array,
  tpr: Array,
  auc: Number
})
</script>

<template>
  <div class="p-4 bg-white shadow rounded-2xl">
    <h2 class="text-lg font-semibold mb-2 text-gray-700">
      Curva ROC (AUC: {{ auc.toFixed(3) }})
    </h2>
    <Line
      :data="{
        labels: fpr,
        datasets: [
          {
            label: 'ROC Curve',
            data: tpr,
            borderColor: '#16a34a',
            fill: false,
            tension: 0.3,
          },
        ],
      }"
      :options="{
        responsive: true,
        scales: {
          x: { title: { display: true, text: 'False Positive Rate' } },
          y: { title: { display: true, text: 'True Positive Rate' } },
        },
      }"
    />
  </div>
</template>
