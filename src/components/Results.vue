<template>
  <div v-if="results">
    <v-card class="mx-auto mt-6" elevation="3">
      <v-card-title class="text-h6 d-flex align-center">
        <v-icon start>mdi-shield-search</v-icon>
        Analysis Results
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

        <!-- Enhanced Analysis Cards -->
        <v-row class="mt-4" v-if="llmAnalysis?.parsed">
          <!-- Risk Assessment Card -->
          <v-col cols="12" md="4">
            <v-card variant="outlined" class="h-100">
              <v-card-title class="text-subtitle-2 d-flex align-center pb-2">
                <v-icon start color="error" size="small">mdi-shield-alert</v-icon>
                Risk Assessment
              </v-card-title>
              <v-card-text>
                <div class="text-center mb-3">
                  <v-chip 
                    :color="getRiskColor(llmAnalysis.parsed.riskAssessment.level)" 
                    size="large"
                    class="mb-2"
                  >
                    {{ llmAnalysis.parsed.riskAssessment.level }}
                  </v-chip>
                  <div class="text-h5 font-weight-bold">
                    {{ llmAnalysis.parsed.riskAssessment.score }}/100
                  </div>
                  <div class="text-caption text-grey">Risk Score</div>
                </div>
                <v-divider class="my-2"></v-divider>
                <div class="text-caption text-grey mb-1">Category:</div>
                <div class="text-body-2 mb-2">{{ llmAnalysis.parsed.riskAssessment.category }}</div>
                <div class="text-caption text-grey mb-1">Key Factors:</div>
                <ul class="text-caption risk-factors">
                  <li v-for="(factor, idx) in llmAnalysis.parsed.riskAssessment.factors.slice(0, 3)" :key="idx">
                    {{ factor }}
                  </li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Anomaly Detection Card -->
          <v-col cols="12" md="4">
            <v-card variant="outlined" class="h-100">
              <v-card-title class="text-subtitle-2 d-flex align-center pb-2">
                <v-icon start color="warning" size="small">mdi-radar</v-icon>
                Anomaly Detection
              </v-card-title>
              <v-card-text>
                <div class="text-center mb-3">
                  <v-icon 
                    :color="llmAnalysis.parsed.anomalyDetection.hasAnomalies ? 'warning' : 'success'" 
                    size="48"
                  >
                    {{ llmAnalysis.parsed.anomalyDetection.hasAnomalies ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                  </v-icon>
                  <div class="text-h5 font-weight-bold mt-2">
                    {{ llmAnalysis.parsed.anomalyDetection.anomalyScore }}/100
                  </div>
                  <div class="text-caption text-grey">Anomaly Score</div>
                </div>
                <v-divider class="my-2"></v-divider>
                <div class="text-caption text-grey mb-1">Detected:</div>
                <div v-if="llmAnalysis.parsed.anomalyDetection.anomalies.length > 0">
                  <v-chip 
                    v-for="(anomaly, idx) in llmAnalysis.parsed.anomalyDetection.anomalies.slice(0, 3)" 
                    :key="idx"
                    size="x-small"
                    color="warning"
                    variant="tonal"
                    class="ma-1"
                  >
                    {{ anomaly }}
                  </v-chip>
                </div>
                <div v-else class="text-caption">No anomalies detected</div>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Mitigation Recommendations Card -->
          <v-col cols="12" md="4">
            <v-card variant="outlined" class="h-100">
              <v-card-title class="text-subtitle-2 d-flex align-center pb-2">
                <v-icon start color="success" size="small">mdi-shield-check</v-icon>
                Mitigation
              </v-card-title>
              <v-card-text>
                <div class="text-caption text-grey mb-1">Security Strategies:</div>
                <ul class="text-caption mitigation-list">
                  <li v-for="(strategy, idx) in llmAnalysis.parsed.mitigationRecommendations.strategies.slice(0, 3)" :key="idx">
                    {{ strategy.split(':')[0] }}
                  </li>
                </ul>
                <v-divider class="my-2"></v-divider>
                <div class="text-caption text-grey mb-1">Policy Alignment:</div>
                <div class="d-flex flex-wrap gap-1">
                  <v-chip 
                    v-for="(policy, idx) in llmAnalysis.parsed.mitigationRecommendations.policyAlignment" 
                    :key="idx"
                    size="x-small"
                    color="primary"
                    variant="tonal"
                  >
                    {{ policy }}
                  </v-chip>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- LLM Analysis Section -->
        <v-card class="mt-4" variant="outlined">
          <v-card-title class="text-subtitle-1 d-flex align-center pb-0">
            <v-icon start color="deep-purple">mdi-robot-outline</v-icon>
            AI Security Analyst
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
  isLlmLoading: {
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
.v-card {
  border-radius: 12px;
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
