<template>
  <div>
    <v-card class="mx-auto" elevation="3">
      <v-tabs v-model="activeTab" align-tabs="center" color="primary">
        <v-tab value="url">URL</v-tab>
        <v-tab value="email">Email</v-tab>
        <v-tab value="sms">SMS</v-tab>
      </v-tabs>

      <v-card-text class="pa-6">
        <v-window v-model="activeTab">
          <v-window-item value="url">
            <v-textarea
              v-model="textContent"
              label="Enter URL to analyze"
              placeholder="https://example.com"
              rows="8"
              variant="outlined"
              hide-details
              class="mb-4"
            ></v-textarea>
          </v-window-item>

          <v-window-item value="email">
            <v-textarea
              v-model="textContent"
              label="Enter email content to analyze"
              placeholder="Paste email content here..."
              rows="8"
              variant="outlined"
              hide-details
              class="mb-4"
            ></v-textarea>
          </v-window-item>

          <v-window-item value="sms">
            <v-textarea
              v-model="textContent"
              label="Enter SMS content to analyze"
              placeholder="Paste SMS text here..."
              rows="8"
              variant="outlined"
              hide-details
              class="mb-4"
            ></v-textarea>
          </v-window-item>
        </v-window>

        <div class="text-center">
          <v-btn
            color="primary"
            size="large"
            variant="elevated"
            @click="analyzeContent"
            :disabled="!textContent.trim()"
            class="px-8"
          >
            <v-icon start>mdi-magnify-scan</v-icon>
            Analyze
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <!-- Analysis Results -->
    <v-card v-if="analysisResult" class="mx-auto mt-6" elevation="3">
      <v-card-title class="text-h6">
        <v-icon start>mdi-chart-line</v-icon>
        Analysis Result
      </v-card-title>
      <v-card-text>
        <v-alert type="info" variant="tonal">
          {{ analysisResult }}
        </v-alert>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from "vue";

const activeTab = ref("url");
const textContent = ref("");
const analysisResult = ref("");

const analyzeContent = () => {
  if (!textContent.value.trim()) return;

  // Simulate analysis based on the active tab
  const analysisType = activeTab.value.toUpperCase();
  analysisResult.value = `${analysisType} analysis completed for the provided content. 
    Content length: ${textContent.value.length} characters.
    Analysis type: ${analysisType}
    Status: Analysis successful - Content appears to be legitimate.`;
};
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}

.v-btn {
  text-transform: none;
  font-weight: 600;
}
</style>
