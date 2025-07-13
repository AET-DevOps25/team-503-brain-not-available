import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:1111',
})

export interface User {
    id?: string
    email: string
    name?: string
    passwordHash?: string
}

export const authService = {
    async createUser(user: User) {
        const response = await api.post<User>('/user', user)
        return response.data
    },

    async authenticateUser(email: string, password: string) {
        const response = await api.post<boolean>('/authenticateUser', null, {
            params: { email, password }
        })
        return response.data
    },
}
