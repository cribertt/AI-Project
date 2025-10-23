<template>
  <div class="max-w-2xl mx-auto py-10">
    <!-- Header -->
    <header class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Predicción de Diabetes</h1>
      <p class="text-gray-500 leading-relaxed">
        Modelo predictivo basado en <span class="font-semibold text-gray-700">Random Forest Classifier</span>, 
        entrenado con el dataset <span class="font-medium">Diabetes Logistic Regression</span> de Kaggle.
      </p>
      <a
        href="https://www.kaggle.com/code/arezalo/diabetes-logistic-regression"
        target="_blank"
        class="inline-block mt-3 text-sm text-green-600 hover:text-green-700 transition"
      >
        📘 Ver notebook original en Kaggle
      </a>
    </header>

    <!-- Contenedor -->
    <section class="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 space-y-8">
      <!-- Formulario -->
      <form
        @submit.prevent="handlePredict"
        class="grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <!-- Embarazos -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Embarazos</label>
          <input
            type="range"
            min="0"
            max="15"
            v-model="pregnancies"
            class="w-full accent-green-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ pregnancies }}</p>
        </div>

        <!-- Glucosa -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Glucosa (mg/dL)</label>
          <input
            type="range"
            min="50"
            max="250"
            step="1"
            v-model="glucose"
            class="w-full accent-green-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ glucose }}</p>
        </div>

        <!-- Presión -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Presión Sanguínea (mm Hg)</label>
          <input
            type="range"
            min="40"
            max="130"
            step="1"
            v-model="bloodPressure"
            class="w-full accent-green-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ bloodPressure }}</p>
        </div>

        <!-- Grosor de piel -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Grosor de Piel (mm)</label>
          <input
            type="range"
            min="0"
            max="99"
            step="1"
            v-model="skinThickness"
            class="w-full accent-green-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ skinThickness }}</p>
        </div>

        <!-- Insulina -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Insulina</label>
          <input
            type="range"
            min="0"
            max="900"
            step="5"
            v-model="insulin"
            class="w-full accent-green-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ insulin }}</p>
        </div>

        <!-- BMI -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Índice de Masa Corporal (BMI)</label>
          <input
            type="range"
            min="10"
            max="60"
            step="0.1"
            v-model="bmi"
            class="w-full accent-green-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ bmi }}</p>
        </div>

        <!-- DPF -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Diabetes Pedigree Function</label>
          <input
            type="range"
            min="0"
            max="2.5"
            step="0.01"
            v-model="dpf"
            class="w-full accent-green-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ dpf }}</p>
        </div>

        <!-- Edad -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Edad</label>
          <input
            type="range"
            min="18"
            max="90"
            step="1"
            v-model="age"
            class="w-full accent-green-600"
          />
          <p class="text-xs text-gray-500 mt-1">Valor: {{ age }}</p>
        </div>

        <!-- Botón -->
        <div class="md:col-span-2">
          <button
            type="submit"
            class="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition"
          >
            Predecir
          </button>
        </div>
      </form>

      <!-- Resultado -->
      <transition name="fade">
        <div v-if="result !== null" class="space-y-8">
          <!-- Tarjeta de resultado -->
          <div
            class="p-5 rounded-lg border"
            :class="result === 1
              ? 'bg-red-50 border-red-200 text-red-700'
              : 'bg-green-50 border-green-200 text-green-700'"
          >
            <p class="text-xl font-semibold mb-1">
              {{ result === 1 ? '⚠️ Alta probabilidad de diabetes' : '✅ Bajo riesgo de diabetes' }}
            </p>
            
            <p class="text-sm">
              Probabilidad: <strong>{{ (probability * 100).toFixed(1) }}%</strong>
              (umbral: {{ (threshold * 100).toFixed(1) }}%)
            </p>
            <div class="bg-gray-200 h-3 rounded-full mt-3 overflow-hidden">
              <div
                class="h-full transition-all duration-500"
                :class="probability >= threshold ? 'bg-red-500' : 'bg-green-500'"
                :style="{ width: (probability * 100).toFixed(1) + '%' }"
              ></div>
            </div>
          </div>

          <!-- Gráfico -->
          <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
            <Doughnut :data="chartData" :options="chartOptions" />
          </div>

          <!-- Interpretación -->
          <div
            class="p-5 rounded-lg border"
            :class="hasRisk
              ? 'bg-red-50 border-red-200 text-red-700'
              : 'bg-green-50 border-green-200 text-green-700'"
          >
            <h3 class="font-semibold text-lg mb-2">
              {{ hasRisk ? '📋 Factores de riesgo detectados:' : '💡 Todos los valores están dentro del rango saludable:' }}
            </h3>

            <ul v-if="hasRisk" class="text-sm list-disc pl-5 space-y-1">
              <li v-if="glucose > 140">Glucosa alta ({{ glucose }} mg/dL)</li>
              <li v-if="bmi > 30">IMC elevado ({{ bmi }})</li>
              <li v-if="age > 50">Edad avanzada ({{ age }} años)</li>
              <li v-if="bloodPressure > 90">Presión alta ({{ bloodPressure }} mmHg)</li>
              <li v-if="insulin > 150">Insulina alta ({{ insulin }} μU/mL)</li>
            </ul>

            <p v-else class="text-sm">
              Todos los indicadores analizados están dentro de parámetros normales 🎉.
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
import { ref } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, ArcElement)

import { computed } from 'vue'

const hasRisk = computed(() =>
  glucose.value > 140 ||
  bmi.value > 30 ||
  age.value > 50 ||
  bloodPressure.value > 90 ||
  insulin.value > 150
)


const pregnancies = ref(1)
const glucose = ref(120)
const bloodPressure = ref(70)
const skinThickness = ref(20)
const insulin = ref(80)
const bmi = ref(25)
const dpf = ref(0.4)
const age = ref(30)
const result = ref(null)
const probability = ref(0)
const error = ref(null)

const threshold = ref('')

const chartData = ref(null)
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
    title: { display: true, text: 'Probabilidad de Diabetes' },
  },
}

const handlePredict = async () => {
  result.value = null
  error.value = null
  try {
    const response = await $fetch('https://ai-project-cllh.onrender.com/api/diabetes/predict/', {
      method: 'POST',
      body: {
        Pregnancies: pregnancies.value,
        Glucose: glucose.value,
        BloodPressure: bloodPressure.value,
        SkinThickness: skinThickness.value,
        Insulin: insulin.value,
        BMI: bmi.value,
        DiabetesPedigreeFunction: dpf.value,
        Age: age.value,
      },
    })

    probability.value = response.probability
    result.value = response.prediction
    threshold.value = response.threshold

    // Configurar gráfico
    chartData.value = {
      labels: ['Riesgo de Diabetes', 'Sin riesgo'],
      datasets: [
        {
          data: [response.probability * 100, (1 - response.probability) * 100],
          backgroundColor: ['#dc2626', '#16a34a'],
          hoverBackgroundColor: ['#b91c1c', '#15803d'],
        },
      ],
    }
  } catch (err) {
    error.value = err?.data?.error || 'Error en la predicción'
  }
}
</script>
