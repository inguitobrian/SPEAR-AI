<template>
  <div>
    <v-card class="glass-card analyzer-card" elevation="0">
      <v-tabs 
        v-model="activeTab" 
        align-tabs="center" 
        color="primary"
        class="glass-tabs"
        slider-color="primary"
      >
        <v-tab value="url" class="tab-item">
          <v-icon start>mdi-link-variant</v-icon>
          URL
        </v-tab>
        <v-tab value="email" class="tab-item">
          <v-icon start>mdi-email-outline</v-icon>
          Email
        </v-tab>
        <v-tab value="sms" class="tab-item">
          <v-icon start>mdi-message-text-outline</v-icon>
          SMS
        </v-tab>
      </v-tabs>

      <v-card-text class="pa-6">
        <v-window v-model="activeTab">
          <!-- URL Tab -->
          <v-window-item value="url">
            <InputSection description="Enter a suspicious URL to analyze for phishing threats">
              <v-text-field
                v-model="urlContent"
                label="URL to analyze"
                placeholder="https://suspicious-example.com"
                variant="solo"
                hide-details
                prepend-inner-icon="mdi-link"
                class="glass-input mb-4"
                density="comfortable"
              ></v-text-field>
            </InputSection>
          </v-window-item>

          <!-- Email Tab -->
          <v-window-item value="email">
            <InputSection description="Paste email content to detect social engineering attacks">
              <v-textarea
                v-model="emailContent"
                label="Email content to analyze"
                placeholder="Paste the full email content here, including headers if available..."
                rows="8"
                variant="solo"
                hide-details
                class="glass-input mb-4"
              ></v-textarea>
            </InputSection>
          </v-window-item>

          <!-- SMS Tab -->
          <v-window-item value="sms">
            <InputSection description="Analyze SMS messages for malicious content and scams">
              <v-textarea
                v-model="smsContent"
                label="SMS content to analyze"
                placeholder="Paste the SMS message content here..."
                rows="8"
                variant="solo"
                hide-details
                class="glass-input mb-4"
              ></v-textarea>
            </InputSection>
          </v-window-item>
        </v-window>

        <!-- Analysis Button -->
        <div class="text-center mt-4">
          <v-btn
            color="primary"
            size="x-large"
            variant="elevated"
            @click="handleAnalyze"
            :disabled="!currentContent.trim()"
            :loading="isAnalyzing"
            class="analyze-btn"
            rounded="lg"
          >
            <v-icon start size="large">mdi-shield-search</v-icon>
            {{ isAnalyzing ? 'Analyzing...' : 'Start Security Analysis' }}
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
      :gemini-analysis="geminiAnalysis"
      :is-llm-loading="isLLMLoading"
      :is-gemini-loading="isGeminiLoading"
    />
  </div>
</template>

<script setup>
import Results from "./Results.vue";
import InputSection from "./InputSection.vue";
import { useAnalysis } from "../composables/useAnalysis";
import { useContentManagement } from "../composables/useContentManagement";

// Use composables for modular state management
const {
  analysisResults,
  llmAnalysis,
  geminiAnalysis,
  isAnalyzing,
  isLLMLoading,
  isGeminiLoading,
  errorMessage,
  analyzeContent: performAnalysis,
} = useAnalysis();

const {
  activeTab,
  urlContent,
  emailContent,
  smsContent,
  currentContent,
  currentContentType,
} = useContentManagement();

// Handler functions
const handleAnalyze = async () => {
  await performAnalysis(currentContent.value, currentContentType.value);
};
</script>

<style scoped>
/* Glassmorphism Card */
.glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.analyzer-card {
  overflow: hidden;
}

/* Tabs */
.glass-tabs {
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-item {
  text-transform: none;
  font-weight: 600;
  font-size: 0.95rem;
  letter-spacing: 0.5px;
}

/* Input Label */
.input-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
  display: flex;
  align-items: center;
}

/* Glass Inputs */
.glass-input :deep(.v-field) {
  background: rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.glass-input :deep(.v-field:hover) {
  background: rgba(255, 255, 255, 0.12) !important;
  border-color: rgba(103, 58, 183, 0.5);
}

.glass-input :deep(.v-field--focused) {
  background: rgba(255, 255, 255, 0.15) !important;
  border-color: rgb(103, 58, 183);
  box-shadow: 0 0 20px rgba(103, 58, 183, 0.3);
}

.glass-input :deep(input),
.glass-input :deep(textarea) {
  color: white !important;
}

.glass-input :deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

.glass-input :deep(.v-field__prepend-inner) {
  color: rgba(255, 255, 255, 0.5);
}

/* Analyze Button */
.analyze-btn {
  text-transform: none;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.5px;
  padding: 28px 48px !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  box-shadow: 0 10px 30px rgba(103, 58, 183, 0.4) !important;
  transition: all 0.3s ease;
}

.analyze-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(103, 58, 183, 0.5) !important;
}

.analyze-btn:active {
  transform: translateY(0);
}

/* Error Alert */
:deep(.v-alert) {
  background: rgba(211, 47, 47, 0.15) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(211, 47, 47, 0.3);
  border-radius: 12px;
}
</style>
