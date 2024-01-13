<script setup lang="ts">
import { useRoute } from 'vue-router';
import { Fetcher } from '../utils/fetcher'

import { ref, onMounted, type Ref } from 'vue'
import chunk from 'chunk'

type Metadata = {
  date: string
  ch: string
  total: number
  timestamps: string[]
}

type Player = {
  currentFrame: number
}

const BATCH_SIZE = 50
const fetcher = Fetcher(import.meta.env.VITE_API_HOST || "")

const { query } = useRoute()

const playerInterval: Ref = ref(0)

const player: Ref<Player> = ref({
  currentFrame: 0
})

const metadata: Ref<Metadata> = ref({
  date: '',
  ch: '',
  total: 0,
  timestamps: []
})

const images: Ref<string[]> = ref([])


const getMetadata = async () => {
  const res = await fetcher.get<Metadata>(`frames-metadata?date=${query.date}&ch=${query.ch}`)
  metadata.value = res
}

const createImageFetcher = () => {
  const timestampChunks = chunk(metadata.value.timestamps, BATCH_SIZE)

  const fetchers = timestampChunks.map((timestampChunk) => async () => {
    const res = await fetcher.post<{ images: string[] }>('frames', {
      date: query.date,
      ch: query.ch,
      timestamps: timestampChunk
    })

    const base64images = res?.images ?? []
    images.value = [...images.value, ...base64images]
  })

  return fetchers
}

const loadImages = async () => {
  const fetchers = createImageFetcher()
  for (const fetcher of fetchers) {
    await fetcher()
  }
}

const play = () => {
  playerInterval.value = setInterval(() => {
    if (player.value.currentFrame === metadata.value.total - 1) {
      player.value.currentFrame = 0
    }
    player.value.currentFrame++
  }, 500)
}

const pause = () => {
  clearInterval(playerInterval.value)
}

const stop = () => {
  clearInterval(playerInterval.value)
  player.value.currentFrame = 0
}

onMounted(async () => {
  await getMetadata()
  await loadImages()
})


</script>
<template>
  <div>
    <img :src="`data:image/jpeg;base64,${images[player.currentFrame]}`" width="800" height="600" />
    <div>
      <input type="range" min="0" :max="metadata.total - 1" step="1" v-model="player.currentFrame"
        @click.capture="pause" />
      <button @click="play">Play</button>
      <button @click="pause">Pause</button>
      <button @click="stop">Stop</button>
    </div>

  </div>
</template>
