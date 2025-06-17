<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { pageService, type Page } from '@/service/pageService'

const route = useRoute()
const page = ref<Page | null>(null)

async function loadPage(id: number) {
  page.value = await pageService.getPage(id)
}

onMounted(() => {
  loadPage(parseInt(route.params.id as string, 10))
})

watch(
  () => route.params.id,
  (newId) => {
    loadPage(parseInt(newId as string, 10))
  }
)
</script>

<template>
  <div v-if="page">
    <h1>{{ page.title }}</h1>
    <p>{{ page.content }}</p>
  </div>
  <div v-else>
    <p>Lade Seite…</p>
  </div>
</template>

<style scoped>

</style>