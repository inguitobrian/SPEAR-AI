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
            <v-text-field
              v-model="urlContent"
              label="Enter URL to analyze"
              placeholder="https://example.com"
              variant="solo-filled"
              hide-details
              prepend-inner-icon="mdi-link"
              class="mb-4"
            ></v-text-field>
          </v-window-item>

          <v-window-item value="email">
            <v-textarea
              v-model="emailContent"
              label="Enter email content to analyze"
              placeholder="Paste email content here..."
              rows="8"
              variant="solo-filled"
              hide-details
              class="mb-4"
            ></v-textarea>
          </v-window-item>

          <v-window-item value="sms">
            <v-textarea
              v-model="smsContent"
              label="Enter SMS content to analyze"
              placeholder="Paste SMS text here..."
              rows="8"
              variant="solo-filled"
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
            :disabled="!currentContent.trim()"
            :loading="isAnalyzing"
            class="px-8"
          >
            <v-icon start>mdi-magnify-scan</v-icon>
            Analyze with BERT AI
          </v-btn>
        </div>

        <!-- Error Alert -->
        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          closable
          class="mt-4"
          @click:close="errorMessage = null"
        >
          <v-alert-title>Analysis Failed</v-alert-title>
          {{ errorMessage }}
        </v-alert>
      </v-card-text>
    </v-card>

    <!-- Results Component -->
    <Results 
      :results="analysisResults" 
      :llm-analysis="llmAnalysis"
      :is-llm-loading="isLLMLoading"
    />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import Results from "./Results.vue";

// Backend API URL - change this to your production URL when deploying
const API_URL = "http://localhost:8000";

const activeTab = ref("url");

// Separate content for each tab
const urlContent = ref("");
const emailContent = ref("");
const smsContent = ref("");

const analysisResults = ref(null);
const llmAnalysis = ref(null);
const isAnalyzing = ref(false);
const isLLMLoading = ref(false);
const errorMessage = ref(null);

// Get current tab's content
const currentContent = computed(() => {
  switch (activeTab.value) {
    case "url":
      return urlContent.value;
    case "email":
      return emailContent.value;
    case "sms":
      return smsContent.value;
    default:
      return "";
  }
});

const analyzeContent = async () => {
  if (!currentContent.value.trim()) return;

  isAnalyzing.value = true;
  errorMessage.value = null;
  analysisResults.value = null;
  llmAnalysis.value = null;

  const content = currentContent.value;
  const contentType = activeTab.value.toLowerCase();

  try {
    // Step 1: Fast BERT detection
    const detectResponse = await fetch(`${API_URL}/detect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content: content,
        content_type: contentType,
      }),
    });

    if (!detectResponse.ok) {
      const error = await detectResponse.json();
      throw new Error(error.detail || "Detection failed");
    }

    const detectResult = await detectResponse.json();
    
    // Show BERT results immediately
    analysisResults.value = detectResult;
    isAnalyzing.value = false;

    // Step 2: Start LLM analysis in background
    isLLMLoading.value = true;
    
    const llmResponse = await fetch(`${API_URL}/analyze-llm`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content: content,
        content_type: contentType,
        threat_level: detectResult.threatLevel,
        confidence: detectResult.confidenceScore,
      }),
    });

    if (llmResponse.ok) {
      const llmResult = await llmResponse.json();
      llmAnalysis.value = llmResult;
    } else {
      llmAnalysis.value = {
        success: false,
        analysis: "LLM analysis failed",
        error: "Could not get LLM response"
      };
    }
  } catch (error) {
    console.error("Analysis error:", error);
    errorMessage.value =
      error.message === "Failed to fetch"
        ? "Cannot connect to the analysis server. Make sure the backend is running on " + API_URL
        : error.message;
  } finally {
    isAnalyzing.value = false;
    isLLMLoading.value = false;
  }
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
