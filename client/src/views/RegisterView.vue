<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
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
        <Input id="email" type="email" placeholder="m@example.com" required />
      </div>
      <div class="grid gap-2">
        <Label for="password">Password</Label>
        <Input id="password" type="password" required />
      </div>
    </CardContent>
    <CardFooter class="grid gap-4">
      <div class="grid gap-2">
        <Button class="w-full">
            Create an account
        </Button>
      </div>
      <div class="grid gap-2">
        <div class="mt-4 text-center text-sm">
            Already have an account?
            <a href="#" class="underline">
                Sign in
            </a>
        </div>
      </div>
    </CardFooter>
  </Card>
</div>
</template>