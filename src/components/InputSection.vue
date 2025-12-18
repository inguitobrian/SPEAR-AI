<template>
  <div class="input-section">
    <div class="input-label mb-3">
      <v-icon size="small" class="mr-1">mdi-information-outline</v-icon>
      {{ description }}
    </div>
    
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  description: {
    type: String,
    required: true
  }
});
</script>

<style scoped>
.input-section {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.input-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
  display: flex;
  align-items: center;
}
</style>
 