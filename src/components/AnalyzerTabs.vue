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
            :loading="isAnalyzing"
            class="px-8"
          >
            <v-icon start>mdi-magnify-scan</v-icon>
            Analyze
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <!-- Results Component -->
    <Results :results="analysisResults" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import Results from "./Results.vue";

const activeTab = ref("url");
const textContent = ref("");
const analysisResults = ref(null);
const isAnalyzing = ref(false);

const analyzeContent = async () => {
  if (!textContent.value.trim()) return;

  isAnalyzing.value = true;

  // Simulate API call delay
  setTimeout(() => {
    const analysisType = activeTab.value.toLowerCase();

    // Generate realistic vulnerability assessment results
    const mockResults = generateMockResults(analysisType, textContent.value);
    analysisResults.value = mockResults;
    isAnalyzing.value = false;
  }, 2000);
};

const generateMockResults = (contentType, content) => {
  const riskLevels = ["low", "medium", "high"];
  const vulnerabilityTypes = {
    url: [
      {
        type: "Suspicious Domain",
        description: "Domain registered recently with anonymized WHOIS data",
        severity: "medium",
      },
      {
        type: "Phishing Indicators",
        description: "URL structure mimics legitimate banking website",
        severity: "high",
      },
      {
        type: "Malware Risk",
        description: "Site flagged for hosting malicious downloads",
        severity: "critical",
      },
    ],
    email: [
      {
        type: "Sender Spoofing",
        description: "Email header analysis shows potential spoofing",
        severity: "high",
      },
      {
        type: "Social Engineering",
        description: "Content contains urgency tactics and fear appeals",
        severity: "medium",
      },
      {
        type: "Credential Harvesting",
        description: "Contains suspicious login links",
        severity: "critical",
      },
    ],
    sms: [
      {
        type: "Smishing Attempt",
        description: "SMS contains shortened URLs and urgent language",
        severity: "high",
      },
      {
        type: "Fake Alert",
        description: "Impersonates legitimate service notifications",
        severity: "medium",
      },
      {
        type: "Data Collection",
        description: "Requests personal information via reply",
        severity: "medium",
      },
    ],
  };

  const randomRisk = riskLevels[Math.floor(Math.random() * riskLevels.length)];
  const vulnerabilities =
    vulnerabilityTypes[contentType] || vulnerabilityTypes.url;
  const selectedVulns = vulnerabilities.slice(
    0,
    Math.floor(Math.random() * 3) + 1
  );

  const riskScore = {
    low: Math.floor(Math.random() * 30) + 10,
    medium: Math.floor(Math.random() * 30) + 40,
    high: Math.floor(Math.random() * 30) + 70,
  }[randomRisk];

  const authenticity =
    riskScore > 70 ? "Malicious" : riskScore > 40 ? "Suspicious" : "Legitimate";
  const confidence = Math.floor(Math.random() * 20) + 80;

  return {
    riskLevel: randomRisk,
    riskScore: riskScore,
    vulnerabilities: selectedVulns,
    modelResults: {
      confidence: confidence,
      authenticity: authenticity,
    },
    recommendations: [
      "Verify sender identity through alternative communication channels",
      "Do not click on any links or download attachments",
      "Report this content to your organization's security team",
      "Enable two-factor authentication on all accounts",
    ],
    contentType: contentType.toUpperCase(),
    timestamp: new Date().toLocaleString(),
    processingTime: Math.floor(Math.random() * 1000) + 500,
  };
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
