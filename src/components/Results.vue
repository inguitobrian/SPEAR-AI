<template>
  <div v-if="results">
    <v-card class="mx-auto mt-6" elevation="3">
      <v-card-title class="text-h6 d-flex align-center">
        <v-icon start>mdi-shield-search</v-icon>
        Vulnerability Assessment Results
      </v-card-title>

      <v-card-text>
        <!-- Overall Risk Score -->
        <div class="mb-4">
          <h3 class="text-h6 mb-2">Risk Assessment</h3>
          <v-chip
            :color="getRiskColor(results.riskLevel)"
            size="large"
            variant="elevated"
            class="mb-3"
          >
            <v-icon start>mdi-shield-alert</v-icon>
            {{ results.riskLevel.toUpperCase() }} RISK
          </v-chip>
          <div class="text-body-2 text-grey-darken-1">
            Risk Score: {{ results.riskScore }}/100
          </div>
        </div>

        <!-- Vulnerability Findings -->
        <div class="mb-4">
          <h3 class="text-h6 mb-3">Detected Threats</h3>
          <v-list class="bg-grey-lighten-5" density="compact">
            <v-list-item
              v-for="(finding, index) in results.vulnerabilities"
              :key="index"
              class="mb-2"
            >
              <template v-slot:prepend>
                <v-icon :color="getSeverityColor(finding.severity)">
                  {{ getSeverityIcon(finding.severity) }}
                </v-icon>
              </template>

              <v-list-item-title class="font-weight-medium">
                {{ finding.type }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ finding.description }}
              </v-list-item-subtitle>

              <template v-slot:append>
                <v-chip
                  :color="getSeverityColor(finding.severity)"
                  size="small"
                  variant="outlined"
                >
                  {{ finding.severity }}
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </div>

        <!-- Model Analysis Results -->
        <div class="mb-4">
          <h3 class="text-h6 mb-3">AI Model Analysis</h3>
          <v-row>
            <v-col cols="12" md="6">
              <v-card variant="outlined" class="pa-3">
                <div class="text-center">
                  <v-icon size="32" color="primary" class="mb-2"
                    >mdi-brain</v-icon
                  >
                  <div class="text-body-2 text-grey-darken-1">
                    Confidence Score
                  </div>
                  <div class="text-h5 font-weight-bold text-primary">
                    {{ results.modelResults.confidence }}%
                  </div>
                </div>
              </v-card>
            </v-col>

            <v-col cols="12" md="6">
              <v-card variant="outlined" class="pa-3">
                <div class="text-center">
                  <v-icon size="32" color="success" class="mb-2"
                    >mdi-check-circle</v-icon
                  >
                  <div class="text-body-2 text-grey-darken-1">Authenticity</div>
                  <div
                    class="text-h5 font-weight-bold"
                    :class="
                      getAuthenticityColor(results.modelResults.authenticity)
                    "
                  >
                    {{ results.modelResults.authenticity }}
                  </div>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </div>

        <!-- Recommendations -->
        <div>
          <h3 class="text-h6 mb-3">Security Recommendations</h3>
          <v-list density="compact">
            <v-list-item
              v-for="(recommendation, index) in results.recommendations"
              :key="index"
              class="mb-1"
            >
              <template v-slot:prepend>
                <v-icon color="info">mdi-lightbulb-outline</v-icon>
              </template>
              <v-list-item-title class="text-body-2">
                {{ recommendation }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </div>

        <!-- Analysis Metadata -->
        <v-divider class="my-4"></v-divider>
        <div class="text-caption text-grey-darken-1">
          Analysis completed at {{ results.timestamp }} • Content type:
          {{ results.contentType }} • Processing time:
          {{ results.processingTime }}ms
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  results: {
    type: Object,
    default: null,
  },
});

const getRiskColor = (riskLevel) => {
  switch (riskLevel.toLowerCase()) {
    case "high":
      return "error";
    case "medium":
      return "warning";
    case "low":
      return "success";
    default:
      return "grey";
  }
};

const getSeverityColor = (severity) => {
  switch (severity.toLowerCase()) {
    case "critical":
      return "error";
    case "high":
      return "deep-orange";
    case "medium":
      return "warning";
    case "low":
      return "info";
    default:
      return "grey";
  }
};

const getSeverityIcon = (severity) => {
  switch (severity.toLowerCase()) {
    case "critical":
      return "mdi-alert-octagon";
    case "high":
      return "mdi-alert";
    case "medium":
      return "mdi-alert-triangle";
    case "low":
      return "mdi-information";
    default:
      return "mdi-circle";
  }
};

const getAuthenticityColor = (authenticity) => {
  switch (authenticity.toLowerCase()) {
    case "legitimate":
      return "text-success";
    case "suspicious":
      return "text-warning";
    case "malicious":
      return "text-error";
    default:
      return "text-grey";
  }
};
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}

.v-list {
  border-radius: 8px;
}
</style>
