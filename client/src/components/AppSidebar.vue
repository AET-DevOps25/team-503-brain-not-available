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

const items = [
    {
        title: "Home",
        url: "#",
        icon: Home,
    },
    {
        title: "Inbox",
        url: "/settings",
        icon: Inbox,
    },
    {
        title: "Calendar",
        url: "/profile",
        icon: Calendar,
    },
    {
        title: "Search",
        url: "#",
        icon: Search,
    },
    {
        title: "Settings",
        url: "#",
        icon: Settings,
    },
];

// Seiten aus dem Page-Service laden
const pages = ref([])

onMounted(async () => {
    pages.value = await pageService.getAllPages()
})

async function deletePage(pageId: number) {
    if (confirm("Willst du diese Seite wirklich löschen?")) {
        await pageService.deletePage(pageId)
        pages.value = pages.value.filter((p: any) => p.pageId !== pageId)
    }
}
</script>

<template>
    <Sidebar>
        <SidebarHeader />
        <SidebarContent>
            <SidebarGroup>
                <SidebarGroupLabel>Application</SidebarGroupLabel>
                <SidebarGroupContent>
                    <SidebarMenu>
                        <SidebarMenuItem v-for="item in items" :key="item.title">
                            <SidebarMenuButton asChild>
                                <a :href="item.url">
                                    <component :is="item.icon" />
                                    <span>{{item.title}}</span>
                                </a>
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                    </SidebarMenu>
                </SidebarGroupContent>
            </SidebarGroup>
            <SidebarGroup>
                <SidebarGroupLabel>Seiten</SidebarGroupLabel>
                <SidebarGroupContent>
                    <SidebarMenu>
                        <SidebarMenuItem v-for="page in pages" :key="page.id" class="flex items-center justify-between">
                            <SidebarMenuButton asChild class="flex-1 min-w-0">
                                <router-link :to="`/pages/${page.pageId}`" class="flex items-center min-w-0">
                                    <FileText style="margin-right: 8px;" />
                                    <span class="truncate">{{ page.title }}</span>
                                </router-link>
                            </SidebarMenuButton>

                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <button class="ml-2 rounded hover:bg-gray-100 h-7 w-13 flex items-center justify-center">
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
                            <SidebarMenuButton>
                                <User2 /> Username
                                <ChevronUp class="ml-auto" />
                            </SidebarMenuButton>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent
                            side="top"
                            class="w-[--reka-popper-anchor-width]"
                        >
                            <DropdownMenuItem>
                                <span>Account</span>
                            </DropdownMenuItem>
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