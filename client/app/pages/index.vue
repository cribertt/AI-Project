<script setup>
import { ref, onMounted } from 'vue'
import RocChart from '~/components/RocChart.vue'
import FeatureImportance from '~/components/FeatureImportance.vue'

const rocData = ref(null)
const features = ref([])
const importance = ref([])

onMounted(async () => {
  const rocRes = await $fetch('https://ai-project-cllh.onrender.com/api/diabetes/roc-data/')
  rocData.value = rocRes

  const featRes = await $fetch('https://ai-project-cllh.onrender.com/api/insurance/features/')
  features.value = featRes.features
  importance.value = featRes.importance
})
</script>

<template>
    <h1>adsasdsa</h1>
  <div class="min-h-screen bg-gray-100 p-6 grid md:grid-cols-2 gap-6">
    <RocChart
      v-if="rocData"
      :fpr="rocData.fpr"
      :tpr="rocData.tpr"
      :auc="rocData.auc"
    />

    <FeatureImportance
      v-if="features.length"
      :features="features"
      :importance="importance"
    />
  </div>
</template>
