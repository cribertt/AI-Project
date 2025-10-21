<script setup>
import { ref, onMounted } from 'vue'
import RocChart from '~/components/RocChart.vue'
import FeatureImportance from '~/components/FeatureImportance.vue'

const rocData = ref(null)
const features = ref([])
const importance = ref([])

onMounted(async () => {
  try {
    const rocRes = await $fetch('https://ai-project-cllh.onrender.com/api/diabetes/roc-data/')
    rocData.value = rocRes

    const featRes = await $fetch('https://ai-project-cllh.onrender.com/api/insurance/data/')

    // 🔥 Si el backend devuelve una lista de pares [feature, importance]
    if (Array.isArray(featRes)) {
      features.value = featRes.map(item => item[0])
      importance.value = featRes.map(item => item[1])
    } else {
      // 🔁 Si el backend ya tiene .features y .importance
      features.value = featRes.features || []
      importance.value = featRes.importance || []
    }

    console.log('Features:', features.value)
    console.log('Importance:', importance.value)
  } catch (error) {
    console.error('Error cargando datos:', error)
  }
})


</script>

<template>
  <div class="min-h-screen bg-gray-100 p-6 grid md:grid-cols-2 gap-6">
    <RocChart
      v-if="rocData"
      :fpr="rocData.fpr"
      :tpr="rocData.tpr"
      :auc="rocData.auc"
    />
      <FeatureImportance
        v-if="features.length"
        :key="i"
        :features="features"
        :importance="importance"
      />  </div>
</template>
