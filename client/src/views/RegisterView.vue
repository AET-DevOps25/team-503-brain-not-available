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

const createAccount = async () => {
    try {
        await authService.createUser({email: email.value, name: email.value, passwordHash: password.value})
        toast('Created new account successfully')
        router.push('/login')
    } catch (error) {
        // handle error (e.g., show notification)
        console.error('Registration failed:', error)
        toast('Failed to create account')
    }
}
</script>

<template>
<div class="flex h-screen w-full items-center justify-center px-4 bg-gray-100">
  <Card class="w-full max-w-sm">
    <CardHeader>
      <CardTitle class="text-2xl">
        Sign Up
      </CardTitle>
      <CardDescription>
        Enter your information to create an account.
      </CardDescription>
    </CardHeader>
    <CardContent class="grid gap-4">
      <div class="grid gap-2">
        <Label for="email">Email</Label>
        <Input id="email" type="email" placeholder="john.doe@tum.de" v-model="email" required />
      </div>
      <div class="grid gap-2">
        <Label for="password">Password</Label>
        <Input id="password" type="password" v-model="password" required />
      </div>
    </CardContent>
    <CardFooter class="grid gap-4">
      <div class="grid gap-2">
        <Button class="w-full" @click="createAccount">
            Create an account
        </Button>
      </div>
      <div class="grid gap-2">
        <div class="mt-4 text-center text-sm">
            Already have an account?
            <router-link to="/login">
                <a href="#" class="underline">Sign in</a>
            </router-link>
        </div>
      </div>
    </CardFooter>
  </Card>
</div>
</template>