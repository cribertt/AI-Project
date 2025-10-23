<template>
  <aside class="fixed top-0 left-0 h-screen w-64 bg-gray-900 text-gray-100 flex flex-col shadow-lg">
    <div class="p-6 border-b border-gray-700">
      <h1 class="text-xl font-bold">Predicciones</h1>
      <p class="text-sm text-gray-400">Modelos Kaggle</p>
    </div>

    <nav class="flex-1 mt-4">
      <NuxtLink
        to="/insurance"
        class="block px-6 py-3 hover:bg-gray-800 transition"
        :class="{ 'bg-gray-800': $route.path === '/insurance' }"
      >
        🩺 Costos Médicos
      </NuxtLink>

      <NuxtLink
        to="/diabetes"
        class="block px-6 py-3 hover:bg-gray-800 transition"
        :class="{ 'bg-gray-800': $route.path === '/diabetes' }"
      >
        💉 Predicción Diabetes
      </NuxtLink>
    </nav>

    <div class="p-4 border-t border-gray-700 text-xs text-gray-500 text-center">
      Kaggle Models © 2025
    </div>
  </aside>
</template>
