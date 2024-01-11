<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ref, onMounted } from 'vue'
const HOST = `http://${window.location.hostname}:3000`
const CHANNELS = ['1', '2', '3', '4', '5', '6', '7', '8']
const records = ref([])

const getRecords = async () => {
  const response = await fetch(`${HOST}/records`)
  records.value = (await response.json())?.records ?? []
}

onMounted(() => {
  getRecords()
})

</script>

<template>
  <main>
    <div v-for="recordDate in records" :key="recordDate">
      <RouterLink v-for="ch in CHANNELS" :key="ch" :to="`/viewer?date=${recordDate}&ch=${ch}`" target="_blank">
        {{ recordDate }} CH{{ ch }}
      </RouterLink>
    </div>
  </main>
</template>
