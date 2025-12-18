<template>
  <div v-if="results" class="results-container">
    <v-card class="glass-card results-card" elevation="0">
      <v-card-title class="text-h5 d-flex align-center results-header">
        <v-icon start size="large" class="pulse-icon">mdi-shield-check-outline</v-icon>
        <span class="gradient-text-results">Security Analysis Results</span>
      </v-card-title>

      <v-card-text>
        <!-- Threat Level & Confidence -->
        <v-row>
          <v-col cols="12" md="6">
            <v-card 
              :color="getThreatColor(results.threatLevel)" 
              variant="tonal" 
              class="pa-4"
            >
              <div class="text-center">
                <v-icon 
                  size="48" 
                  :color="getThreatColor(results.threatLevel)"
                  class="mb-2"
                >
                  {{ getThreatIcon(results.threatLevel) }}
                </v-icon>
                <div class="text-body-2 text-grey-darken-1 mb-1">Threat Level</div>
                <div 
                  class="text-h4 font-weight-bold text-uppercase"
                  :class="getThreatTextColor(results.threatLevel)"
                >
                  {{ results.threatLevel }}
                </div>
              </div>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card variant="outlined" class="pa-4">
              <div class="text-center">
                <v-icon size="48" color="primary" class="mb-2">mdi-brain</v-icon>
                <div class="text-body-2 text-grey-darken-1 mb-1">
                  BERT Confidence
                </div>
                <div class="text-h4 font-weight-bold text-primary">
                  {{ results.confidenceScore }}%
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>

        <!-- Dual LLM Analysis Section -->
        <v-row class="mt-4">
          <!-- DeepSeek Analysis -->
          <v-col cols="12" :md="geminiAnalysis?.success ? 6 : 12">
            <v-card variant="outlined">
              <v-card-title class="text-subtitle-1 d-flex align-center pb-0">
                <v-icon start color="deep-purple">mdi-robot-outline</v-icon>
                AI Analysis
                <v-spacer></v-spacer>
            
            <!-- Loading State -->
            <v-chip 
              v-if="isLlmLoading" 
              size="small" 
              color="primary" 
              variant="tonal"
            >
              <v-progress-circular 
                indeterminate 
                size="14" 
                width="2" 
                class="mr-2"
              ></v-progress-circular>
              Analyzing...
            </v-chip>
            
            <!-- Success State -->
            <v-chip 
              v-else-if="llmAnalysis?.success" 
              size="small" 
              color="success" 
              variant="tonal"
            >
              <v-icon start size="small">mdi-check</v-icon>
              Analysis Complete
            </v-chip>
            
            <!-- Error/Unavailable State -->
            <v-chip 
              v-else-if="llmAnalysis" 
              size="small" 
              color="warning" 
              variant="tonal"
            >
              <v-icon start size="small">mdi-alert</v-icon>
              Unavailable
            </v-chip>
            
            <!-- Waiting State -->
            <v-chip 
              v-else 
              size="small" 
              color="grey" 
              variant="tonal"
            >
              <v-icon start size="small">mdi-clock-outline</v-icon>
              Pending
            </v-chip>
          </v-card-title>
          
          <v-card-text>
            <!-- Loading Skeleton -->
            <div v-if="isLlmLoading" class="llm-loading">
              <v-skeleton-loader type="paragraph" class="mb-2"></v-skeleton-loader>
              <v-skeleton-loader type="paragraph"></v-skeleton-loader>
              <div class="typing-indicator mt-3">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            
            <!-- LLM Analysis Content with Typing Effect -->
            <div 
              v-else-if="llmAnalysis?.success" 
              class="llm-analysis-content"
              v-html="formatAnalysis(displayedAnalysis)"
            ></div>
            
            <!-- Error/Unavailable Message -->
            <v-alert 
              v-else-if="llmAnalysis" 
              type="info" 
              variant="tonal" 
              density="compact"
            >
              {{ llmAnalysis?.analysis || 'LLM analysis not available' }}
              <template v-if="llmAnalysis?.error">
                <br>
                <span class="text-caption">Error: {{ llmAnalysis.error }}</span>
              </template>
            </v-alert>
            
            <!-- Waiting Message -->
            <div v-else class="text-grey text-body-2">
              Waiting for AI analysis to start...
            </div>

                <!-- Model Info -->
                <div 
                  v-if="llmAnalysis?.model && !isLlmLoading" 
                  class="text-caption text-grey mt-3"
                >
                  Model: {{ llmAnalysis.model }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Gemini Validation -->
          <v-col cols="12" md="6" v-if="geminiAnalysis || isGeminiLoading">
            <v-card variant="outlined">
              <v-card-title class="text-subtitle-1 d-flex align-center pb-0">
                <v-icon start color="success">mdi-shield-check</v-icon>
                Gemini Validation
                <v-spacer></v-spacer>
                
                <!-- Loading State -->
                <v-chip 
                  v-if="isGeminiLoading" 
                  size="small" 
                  color="primary" 
                  variant="tonal"
                >
                  <v-progress-circular 
                    indeterminate 
                    size="14" 
                    width="2" 
                    class="mr-2"
                  ></v-progress-circular>
                  Validating...
                </v-chip>
                
                <!-- Success State -->
                <v-chip 
                  v-else-if="geminiAnalysis?.success" 
                  size="small" 
                  color="success" 
                  variant="tonal"
                >
                  <v-icon start size="small">mdi-check</v-icon>
                  Validated
                </v-chip>
                
                <!-- Error State -->
                <v-chip 
                  v-else-if="geminiAnalysis" 
                  size="small" 
                  color="warning" 
                  variant="tonal"
                >
                  <v-icon start size="small">mdi-alert</v-icon>
                  Unavailable
                </v-chip>
              </v-card-title>
              
              <v-card-text>
                <!-- Loading Skeleton -->
                <div v-if="isGeminiLoading" class="llm-loading">
                  <v-skeleton-loader type="paragraph" class="mb-2"></v-skeleton-loader>
                  <v-skeleton-loader type="paragraph"></v-skeleton-loader>
                  <div class="typing-indicator mt-3">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
                
                <!-- Gemini Analysis Content -->
                <div 
                  v-else-if="geminiAnalysis?.success" 
                  class="llm-analysis-content"
                  v-html="formatAnalysis(geminiAnalysis.analysis)"
                ></div>
                
                <!-- Error Message -->
                <v-alert 
                  v-else-if="geminiAnalysis" 
                  type="info" 
                  variant="tonal" 
                  density="compact"
                >
                  {{ geminiAnalysis?.analysis || 'Gemini validation not available' }}
                </v-alert>

                <!-- Model Info -->
                <div 
                  v-if="geminiAnalysis?.model && !isGeminiLoading" 
                  class="text-caption text-grey mt-3"
                >
                  Model: {{ geminiAnalysis.model }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Analysis Metadata -->
        <v-divider class="my-4"></v-divider>
        <div class="text-caption text-grey-darken-1">
          Detection completed at {{ results.timestamp }} • Content type:
          {{ results.contentType }} • BERT processing time:
          {{ results.processingTime }}ms
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  results: {
    type: Object,
    default: null,
  },
  llmAnalysis: {
    type: Object,
    default: null,
  },
  geminiAnalysis: {
    type: Object,
    default: null,
  },
  isLlmLoading: {
    type: Boolean,
    default: false,
  },
  isGeminiLoading: {
    type: Boolean,
    default: false,
  },
});

// Typing effect state
const displayedAnalysis = ref("");
let typingInterval = null;

// Watch for LLM analysis changes and trigger typing effect
watch(() => props.llmAnalysis, (newAnalysis) => {
  if (newAnalysis?.success && newAnalysis?.analysis) {
    startTypingEffect(newAnalysis.analysis);
  } else {
    displayedAnalysis.value = "";
  }
}, { immediate: true });

// Clear typing when results change
watch(() => props.results, () => {
  clearInterval(typingInterval);
  displayedAnalysis.value = "";
});

const startTypingEffect = (fullText) => {
  clearInterval(typingInterval);
  displayedAnalysis.value = "";
  
  let index = 0;
  const charsPerTick = 3; // Characters to add per interval
  const speed = 10; // Milliseconds between ticks
  
  typingInterval = setInterval(() => {
    if (index < fullText.length) {
      displayedAnalysis.value = fullText.substring(0, index + charsPerTick);
      index += charsPerTick;
    } else {
      displayedAnalysis.value = fullText;
      clearInterval(typingInterval);
    }
  }, speed);
};

const getThreatColor = (threatLevel) => {
  switch (threatLevel?.toLowerCase()) {
    case "malicious":
      return "error";
    case "suspicious":
      return "warning";
    case "safe":
      return "success";
    default:
      return "grey";
  }
};

const getRiskColor = (riskLevel) => {
  switch (riskLevel?.toUpperCase()) {
    case "CRITICAL":
      return "error";
    case "HIGH":
      return "orange";
    case "MEDIUM":
      return "warning";
    case "LOW":
      return "success";
    default:
      return "grey";
  }
};

const getThreatTextColor = (threatLevel) => {
  switch (threatLevel?.toLowerCase()) {
    case "malicious":
      return "text-error";
    case "suspicious":
      return "text-warning";
    case "safe":
      return "text-success";
    default:
      return "text-grey";
  }
};

const getThreatIcon = (threatLevel) => {
  switch (threatLevel?.toLowerCase()) {
    case "malicious":
      return "mdi-alert-octagon";
    case "suspicious":
      return "mdi-alert-circle";
    case "safe":
      return "mdi-check-circle";
    default:
      return "mdi-help-circle";
  }
};

// Simple markdown-like formatting for LLM analysis
const formatAnalysis = (text) => {
  if (!text) return '';
  
  return text
    // Escape HTML
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // Bold text **text**
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Headers (lines starting with #)
    .replace(/^### (.*$)/gm, '<h4 class="text-subtitle-2 mt-3 mb-1">$1</h4>')
    .replace(/^## (.*$)/gm, '<h3 class="text-subtitle-1 mt-3 mb-1">$1</h3>')
    .replace(/^# (.*$)/gm, '<h2 class="text-h6 mt-3 mb-1">$1</h2>')
    // Bullet points
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    // Numbered lists
    .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
    // Line breaks
    .replace(/\n\n/g, '</p><p class="mb-2">')
    .replace(/\n/g, '<br>')
    ;
};
</script>

<style scoped>
.results-container {
  animation: slideInUp 0.5s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
}

.results-card {
  border-radius: 20px !important;
  overflow: hidden;
}

.results-header {
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem !important;
}

.gradient-text-results {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.pulse-icon {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

.v-card {
  border-radius: 16px;
}

.llm-analysis-content {
  line-height: 1.6;
}

.llm-analysis-content :deep(h2),
.llm-analysis-content :deep(h3),
.llm-analysis-content :deep(h4) {
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.llm-analysis-content :deep(li) {
  margin-left: 1.5rem;
  margin-bottom: 0.25rem;
}

.llm-analysis-content :deep(strong) {
  color: rgb(var(--v-theme-primary));
}

/* Typing indicator animation */
.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: rgb(var(--v-theme-primary));
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Risk and Mitigation Lists */
.risk-factors,
.mitigation-list {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.risk-factors li,
.mitigation-list li {
  margin-bottom: 0.5rem;
  padding-left: 1rem;
  position: relative;
}

.risk-factors li:before {
  content: "⚠️";
  position: absolute;
  left: 0;
}

.mitigation-list li:before {
  content: "✓";
  position: absolute;
  left: 0;
  color: rgb(var(--v-theme-success));
  font-weight: bold;
}

.h-100 {
  height: 100%;
}

.gap-1 {
  gap: 0.25rem;
}
</style>
