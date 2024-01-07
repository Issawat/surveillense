<script setup lang="ts">
import { ref, onMounted } from 'vue'
const sampleData = ref({})

const getSampleData = async () => {
  const response = await fetch('http://localhost:3000/ups')
  sampleData.value = await response.json()
}

onMounted(() => {
  getSampleData()
})

</script>

<template>
  <main>
    {{ sampleData }}
  </main>
</template>
