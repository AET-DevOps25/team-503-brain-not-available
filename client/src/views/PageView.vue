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
import { Button } from '@/components/ui/button'
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

const isEditing = ref(false)
const editedPage = ref<Page | null>(null)

function enableEdit() {
  if (page.value) {
    // copy page values to editedPage in order to not directly edit the original page
    editedPage.value = { ...page.value }
    isEditing.value = true
  }
}

async function savePage() {
  if (editedPage.value) {
    console.log('Speichere Seite:', editedPage.value)
    await pageService.updatePage(editedPage.value.pageId, editedPage.value)
    page.value = { ...editedPage.value } // refresh values
    isEditing.value = false
  }
}
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
              <div class="flex justify-between items-center mb-4">
                <h1 v-if="!isEditing">{{ page.title }}</h1>
                <input
                  v-else
                  v-model="editedPage.title"
                  class="text-2xl font-bold border p-2 w-full"
                />

                <Button
                  @click="isEditing ? savePage() : enableEdit()"
                  class="ml-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  {{ isEditing ? 'Speichern' : 'Bearbeiten' }}
              </Button>
              </div>

              <div v-if="!isEditing">
                <p class="whitespace-pre-line">{{ page.content }}</p>
              </div>
              <div v-else>
                <textarea
                  v-model="editedPage.content"
                  rows="15"
                  class="border p-2 w-full font-mono"
                />
              </div>
          </div>
          <div v-else>
              <p>Lade Seite…</p>
          </div>
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
