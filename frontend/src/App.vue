<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { http } from './api/http'

const status = ref('正在检查后端服务...')

onMounted(async () => {
  try {
    const response = await http.get('/health')
    status.value = `后端状态：${response.data.data.status}`
  } catch {
    status.value = '后端连接失败'
  }
})
</script>

<template>
  <main>
    <h1>智能健康饮食助手</h1>
    <p>{{ status }}</p>
  </main>
</template>