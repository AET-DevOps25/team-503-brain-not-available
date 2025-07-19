import axios from 'axios'

const api = axios.create({
    baseURL: '/ai',
})

export const aiService = {
    async sendAiChat(prompt: string, pageId: number) {
        const response = await api.post<string>('/chat', { "prompt": prompt, "page_id": pageId })
        return response.data
    }
}
