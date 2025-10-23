<template>
  <div class="max-w-2xl mx-auto py-10">
    <!-- Header -->
    <header class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Predicción de Costos Médicos</h1>
      <p class="text-gray-500 leading-relaxed">
        Modelo predictivo basado en <span class="font-semibold text-gray-700">Random Forest Regressor</span>,
        entrenado con el dataset <span class="font-medium">Medical Insurance Cost</span> de Kaggle.
      </p>
      <a
        href="https://www.kaggle.com/code/mariapushkareva/medical-insurance-cost-with-linear-regression"
        target="_blank"
        class="inline-block mt-3 text-sm text-blue-600 hover:text-blue-700 transition"
      >
        📘 Ver notebook original en Kaggle
      </a>
    </header>

    <!-- Contenedor -->
    <section class="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 space-y-8">
      <!-- Formulario -->
      <form @submit.prevent="handlePredict" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Edad -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Edad</label>
          <input
            type="range"
            min="18"
            max="80"
            v-model="edad"
            class="w-full accent-blue-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ edad }}</p>
        </div>

        <!-- Sexo -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Sexo</label>
          <select v-model="sexo" class="w-full border rounded-md p-2">
            <option value="male">Masculino</option>
            <option value="female">Femenino</option>
          </select>
        </div>

        <!-- BMI -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Índice de Masa Corporal (BMI)</label>
          <input
            type="range"
            min="15"
            max="45"
            step="0.1"
            v-model="bmi"
            class="w-full accent-blue-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ bmi }}</p>
        </div>

        <!-- Hijos -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Cantidad de Hijos</label>
          <input
            type="range"
            min="0"
            max="5"
            step="1"
            v-model="children"
            class="w-full accent-blue-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ children }}</p>
        </div>

        <!-- Fumador -->
        <div class="flex items-center space-x-3 md:col-span-2">
          <input id="smoker" type="checkbox" v-model="smoker" class="w-5 h-5 accent-blue-600" />
          <label for="smoker" class="text-sm font-medium text-gray-700">¿Es fumador?</label>
        </div>

        <!-- Región -->
        <div class="md:col-span-2">
          <label class="block text-sm font-semibold text-gray-700 mb-1">Región</label>
          <select v-model="region" class="w-full border rounded-md p-2">
            <option value="northeast">Noreste</option>
            <option value="northwest">Noroeste</option>
            <option value="southeast">Sureste</option>
            <option value="southwest">Suroeste</option>
          </select>
        </div>

        <!-- Botón -->
        <div class="md:col-span-2">
          <button
            type="submit"
            class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Predecir
          </button>
        </div>
      </form>

      <!-- Resultado -->
      <transition name="fade">
        <div v-if="prediccion" class="space-y-8">
          <!-- Resultado -->
          <div class="p-5 rounded-lg border bg-blue-50 border-blue-200 text-blue-800">
            <p class="text-xl font-semibold mb-1">
              💰 Costo estimado del seguro: 
              <span class="text-blue-700">${{ prediccion.toLocaleString() }}</span>
            </p>
            <p class="text-sm text-gray-600">
              Según el modelo <strong>Random Forest</strong>, basado en tus características personales.
            </p>
          </div>

          <!-- Gráfico comparativo -->
          <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
            <Bar :data="chartData" :options="chartOptions" />
          </div>

          <!-- Interpretación -->
          <div
            class="p-5 rounded-lg border"
            :class="hasRisk
              ? 'bg-red-50 border-red-200 text-red-700'
              : 'bg-green-50 border-green-200 text-green-700'"
          >
            <h3 class="font-semibold text-lg mb-2">
              {{ hasRisk
                ? '📋 Factores que incrementan el costo:'
                : '💡 Perfil saludable y de bajo costo:' }}
            </h3>

            <ul v-if="hasRisk" class="text-sm list-disc pl-5 space-y-1">
              <li v-if="edad > 50">Edad superior a 50 años incrementa el costo base.</li>
              <li v-if="bmi > 30">IMC elevado ({{ bmi }}) sugiere mayor riesgo de salud.</li>
              <li v-if="smoker">El hábito de fumar tiene el mayor impacto en el costo total.</li>
              <li v-if="children > 2">Tener más de 2 hijos puede aumentar la prima familiar.</li>
              <li>Región seleccionada: {{ region }}</li>
            </ul>

            <p v-else class="text-sm">
              Todos los factores ingresados corresponden a un perfil de bajo riesgo. 
              Es probable que obtengas primas más bajas en tu seguro médico 🎉.
            </p>
          </div>
        </div>
      </transition>

      <!-- Error -->
      <div v-if="error" class="mt-4 bg-red-100 text-red-800 p-4 rounded-md">
        ❌ {{ error }}
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const edad = ref(30)
const sexo = ref('male')
const bmi = ref(25)
const children = ref(0)
const smoker = ref(false)
const region = ref('northeast')
const prediccion = ref(null)
const error = ref(null)

const hasRisk = computed(() =>
  edad.value > 50 || bmi.value > 30 || smoker.value || children.value > 2
)

const chartData = ref(null)
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Comparación del costo estimado' },
  },
}

const handlePredict = async () => {
  prediccion.value = null
  error.value = null
  try {
    const response = await $fetch('https://ai-project-cllh.onrender.com/api/insurance/predict/', {
      method: 'POST',
      body: {
        age: edad.value,
        sex: sexo.value,
        bmi: bmi.value,
        children: children.value,
        smoker: smoker.value ? 'yes' : 'no',
        region: region.value,
      },
    })
    prediccion.value = response.predicted_cost

    // Gráfico comparativo
    const promedio = 12000
    chartData.value = {
      labels: ['Promedio Nacional', 'Tu Predicción'],
      datasets: [
        {
          label: 'Costo ($)',
          data: [promedio, response.predicted_cost],
          backgroundColor: ['#9ca3af', '#2563eb'],
        },
      ],
    }
  } catch (err) {
    error.value = err?.data?.error || 'Error en la predicción'
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
