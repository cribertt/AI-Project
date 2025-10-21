<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  features: Array,
  importance: Array
})
</script>

<template>
  <div class="p-4 bg-white shadow rounded-2xl">
    <h2 class="text-lg font-semibold mb-2 text-gray-700">
      Importancia de variables (RandomForest)
    </h2>
    <Bar
      :data="{
        labels: features,
        datasets: [
          {
            label: 'Importancia',
            data: importance,
            backgroundColor: '#3b82f6'
          }
        ]
      }"
      :options="{
        responsive: true,
        indexAxis: 'y',
        scales: {
          x: { title: { display: true, text: 'Relevancia' } },
          y: { title: { display: true, text: 'Variable' } }
        }
      }"
    />
  </div>
</template>
