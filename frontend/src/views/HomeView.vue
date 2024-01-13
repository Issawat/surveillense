<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Fetcher } from '../utils/fetcher'
import { ref, onMounted, type Ref } from 'vue'

type RecordData = {
  date: string
  availableChannels: number[]
}

const records: Ref<RecordData[]> = ref([])

const fetcher = Fetcher(import.meta.env.VITE_API_HOST || "")

const getRecords = async () => {
  const recordData = await fetcher.get<RecordData[]>('records')
  records.value = recordData
}

onMounted(() => {
  getRecords()
})

</script>

<template>
  <main class="container">
    <h1>CCTV object detection viewer</h1>
    <div v-for="record in records" :key="record.date">
      <h3>{{ record.date }}</h3>
      <RouterLink class="button outline dark p-3" style="margin: 10px;" v-for="ch in record.availableChannels" :key="ch"
        :to="`/viewer?date=${record.date}&ch=${ch}`" target="_blank">
        Channel {{ ch }}
      </RouterLink>

    </div>
  </main>
</template>
