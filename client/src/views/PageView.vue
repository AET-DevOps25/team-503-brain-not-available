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
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from '@/components/ui/drawer'
import { Input } from '@/components/ui/input'

import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { pageService, type Page } from '@/service/pageService'
import { aiService } from '@/service/aiService'

const route = useRoute()
const page = ref<Page | null>(null)

const aiAnswer = ref('')
const aiQuestionInput = ref('')

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

async function aiSummarize() {
  await aiService.sendAiChat("Schreibe eine Zusammenfassung der Seite: " + page.value?.content, page.value?.pageId)
    .then((response) => {
      if (editedPage.value) {
        editedPage.value.content = response.response
        //console.log(response)
      }
    })
    .catch((error) => {
      console.error('AI Zusammenfassung fehlgeschlagen:', error)
    })
}

async function aiQuestion() {
  await aiService.sendAiChat("Ich habe eine Frage: " + aiQuestionInput + ", das ist der Inhalt der Seite: " + page.value?.content, page.value?.pageId)
    .then((response) => {
      if (editedPage.value) {
        aiAnswer.value = response.response
        //console.log(response)
      }
    })
    .catch((error) => {
      aiAnswer.value = "Fehler bei der Anfrage..."
      console.error('AI Frage stellen fehlgeschlagen fehlgeschlagen:', error)
    })
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

                <Button v-if="isEditing" @click="aiSummarize()" class="ml-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">AI Zusammenfassen</Button>
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
              <p v-if="route.params.id">Lade Seite…</p>
              <p v-else>Willkommen im Wiki.<br><br>Erstelle deine erste Seite oben links!</p>
          </div>
        </div>
      </div>
      <Drawer>
        <DrawerTrigger>> Frage die KI etwas <</DrawerTrigger>
        <DrawerContent>
          <DrawerHeader>
            <DrawerTitle>Steller der KI eine Frage über diese Seite:</DrawerTitle>
            <div class="flex items-center gap-2">
              <Input v-model="aiQuestionInput" />
              <Button @click="aiQuestion">Senden</Button>
            </div>
          </DrawerHeader>
          <DrawerFooter>
            <div class="w-full min-h-[4rem] border rounded p-2 bg-gray-50" v-if="aiAnswer">
              {{ aiAnswer || '' }}
            </div>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </SidebarInset>
  </SidebarProvider>
</template>
