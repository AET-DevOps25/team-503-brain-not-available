import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8080',
})

export interface Page {
    pageId?: number
    title: string
    content: string
}

export const pageService = {
    async getAllPages() {
        const response = await api.get<Page[]>('/pages')
        return response.data
    },

    async getPage(id: number) {
        const response = await api.get<Page>(`/page/${id}`)
        return response.data
    },

    async createPage(page: Page) {
        const response = await api.post<Page>('/page', page)
        return response.data
    },

    async updatePage(id: number, page: Page) {
        const response = await api.put<Page>(`/page/${id}`, page)
        return response.data
    },

    async deletePage(id: number) {
        const response = await api.delete<Page>(`/page/${id}`)
        return response.data
    },
}
