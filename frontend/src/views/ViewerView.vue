<script setup lang="ts">
import { useRoute } from 'vue-router';
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
const HOST = `http://${window.location.hostname}:3000`

const { query } = useRoute()

const playerInterval = ref(0)

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
  const response = await fetch(`${HOST}/frames-metadata?date=${query.date}&ch=${query.ch}`)
  metadata.value = (await response.json()) ?? {}
}

const createImageFetcher = () => {
  const timestampChunks = chunk(metadata.value.timestamps, BATCH_SIZE)

  const fetchers = timestampChunks.map((timestampChunk) => async () => {
    console.log('fetching', timestampChunk)
    const res = await fetch(`${HOST}/frames`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        date: query.date,
        ch: query.ch,
        timestamps: timestampChunk
      })
    })
    const base64images = (await res.json())?.images ?? []
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
    if(player.value.currentFrame === metadata.value.total - 1) {
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
      <input type="range" min="0" :max="metadata.total - 1" step="1" v-model="player.currentFrame" @click.capture="pause"/>
      <button @click="play">Play</button>
      <button @click="pause">Pause</button>
      <button @click="stop">Stop</button>
    </div>

  </div>
</template>
