import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:5001/chat',
})

export const aiService = {
    async sendAiChat(prompt: string) {
        const response = await api.post<string>('/chat', { "prompt": prompt }, {
            params: { request: 'test' }
        })
        return response.data
    }
}
