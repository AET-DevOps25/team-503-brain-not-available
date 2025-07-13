<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService, type User } from '@/service/authService'
import { toast } from 'vue-sonner'

let email = ref('')
let password = ref('')
const router = useRouter()

const loginAccount = async () => {
    try {
        await authService.authenticateUser(email.value, password.value)
        toast('Login successfully!')
        router.push('/pages')
    } catch (error) {
        // handle error (e.g., show notification)
        console.error('Login failed:', error)
        toast('Login failed!')
    }
}
</script>

<template>
<div class="flex h-screen w-full items-center justify-center px-4 bg-gray-100">
  <Card class="w-full max-w-sm">
    <CardHeader>
      <CardTitle class="text-2xl">
        Login
      </CardTitle>
      <CardDescription>
        Enter your email below to login to your account.
      </CardDescription>
    </CardHeader>
    <CardContent class="grid gap-4">
      <div class="grid gap-2">
        <Label for="email">Email</Label>
        <Input id="email" type="email" placeholder="john.doe@tum.com" v-model="email" required />
      </div>
      <div class="grid gap-2">
        <Label for="password">Password</Label>
        <Input id="password" type="password" v-model="password" required />
      </div>
    </CardContent>
    <CardFooter class="grid gap-4">
      <div class="grid gap-2">
        <Button class="w-full" @click="loginAccount">
            Sign in
        </Button>
      </div>
      <div class="grid gap-2">
        <div class="mt-4 text-center text-sm">
            You need an account?
            <router-link to="/register">
                <a href="#" class="underline">Sign up</a>
            </router-link>
        </div>
      </div>
    </CardFooter>
  </Card>
</div>
</template>