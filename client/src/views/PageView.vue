<script setup lang="ts">
import AppSidebar from '@/components/AppSidebar.vue'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from '@/components/ui/sidebar'

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
  <SidebarProvider>
    <AppSidebar />
    <SidebarInset>
      <header class="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <SidebarTrigger class="-ml-1" />
        <Separator orientation="vertical" class="mr-2 h-4" />
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem class="hidden md:block">
              <BreadcrumbLink href="#">
                Wiki
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator class="hidden md:block" />
            <BreadcrumbItem>
              <BreadcrumbPage v-if="page">{{ page.title }}</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </header>
      <div class="flex flex-1 flex-col gap-4 p-4">
        <div class="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min p-8">
          <div v-if="page">
              <h1>{{ page.title }}</h1>
              <p>{{ page.content }}</p>
          </div>
          <div v-else>
              <p>Lade Seite…</p>
          </div>
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
