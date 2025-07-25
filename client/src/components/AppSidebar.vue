<script setup lang="ts">
import {
    Sidebar,
    SidebarHeader,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarFooter
} from "@/components/ui/sidebar"

import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuItem,
} from "@/components/ui/dropdown-menu"

import { Calendar, Home, Inbox, Search, Settings, FileText, User2, ChevronUp, Ellipsis } from "lucide-vue-next"
import { ref, onMounted } from "vue"
import { pageService } from "@/service/pageService"
import type { Page } from "@/service/pageService"

// Seiten aus dem Page-Service laden
const pages = ref([])

onMounted(async () => {
    pages.value = await pageService.getAllPages()
})

async function deletePage(pageId: number) {
    if (confirm("Willst du diese Seite wirklich löschen?")) {
        await pageService.deletePage(pageId)
        pages.value = pages.value.filter((p: Page) => p.pageId !== pageId)
    }
}

async function createPage() {
    const title = prompt("Titel der neuen Seite:")
    if (title && title.trim().length > 0) {
        const newPage = await pageService.createPage({ title, content: "" })
        pages.value.push(newPage)
    }
}
</script>

<template>
    <Sidebar>
        <SidebarHeader />
        <SidebarContent>
            <SidebarGroup>
                <div class="flex items-center justify-between px-4 py-2">
                    <SidebarGroupLabel>Seiten</SidebarGroupLabel>
                    <Button
                        @click="createPage"
                        class="ml-2 p-1 rounded hover:bg-gray-100 text-blue-600 text-base h-7 w-7 flex items-center justify-center"
                        title="Neue Seite erstellen"
                        variant="primary"
                    >
                        <span class="leading-none">+</span>
                    </button>
                </div>
                <SidebarGroupContent>
                    <SidebarMenu>
                        <SidebarMenuItem v-for="page in pages" :key="page.id" class="flex items-center justify-between">
                            <SidebarMenuButton asChild class="flex-1 min-w-0" variant="ghost">
                                <router-link :to="`/pages/${page.pageId}`" class="flex items-center min-w-0">
                                    <FileText style="margin-right: 8px;" />
                                    <span class="truncate">{{ page.title }}</span>
                                </router-link>
                            </SidebarMenuButton>
                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <button class="ml-2 rounded hover:bg-gray-100 h-7 w-13 flex items-center justify-center" variants="secondary">
                                        <Ellipsis />
                                    </button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent side="right">
                                    <DropdownMenuItem @click="deletePage(page.pageId)">
                                        <span class="text-red-600">Löschen</span>
                                    </DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </SidebarMenuItem>
                    </SidebarMenu>
                </SidebarGroupContent>
            </SidebarGroup>
        </SidebarContent>
        <SidebarFooter>
            <SidebarMenu>
                <SidebarMenuItem>
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <SidebarMenuButton variants="secondary">
                                <User2 /> Username
                                <ChevronUp class="ml-auto" />
                            </SidebarMenuButton>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent
                            side="top"
                            class="w-[--reka-popper-anchor-width]"
                        >
                            <DropdownMenuItem>
                                <span>Sign out</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </SidebarMenuItem>
            </SidebarMenu>
        </SidebarFooter>
    </Sidebar>
</template>