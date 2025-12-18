<template>
  <v-app>
    <!-- Animated Background -->
    <div class="animated-bg"></div>
    <div class="bg-overlay"></div>
    
    <v-main>
      <v-container fluid class="main-container">
        <!-- Hero Section -->
        <div class="hero-section text-center">
          <div class="logo-container mb-4">
            <img src="./assets/logo.png" alt="SPEAR AI Logo" class="logo-img" />
          </div>
          <h1 class="hero-title">
            <span class="gradient-text">SPEAR AI</span>
          </h1>
          <p class="hero-subtitle mb-3">
            Security & Phishing Email Analysis Recognition
          </p>
          <p class="hero-description">
            Advanced AI-powered cybersecurity platform leveraging DeepSeek LLM and BERT models<br>
            for comprehensive threat detection and real-time phishing analysis
          </p>
          
          <!-- Feature Badges -->
          <div class="feature-badges">
            <v-chip class="glass-chip" size="small">
              <v-icon start size="small">mdi-shield-check</v-icon>
              Real-time Detection
            </v-chip>
            <v-chip class="glass-chip" size="small">
              <v-icon start size="small">mdi-robot</v-icon>
              AI-Powered
            </v-chip>
            <v-chip class="glass-chip" size="small">
              <v-icon start size="small">mdi-lightning-bolt</v-icon>
              Instant Analysis
            </v-chip>
          </div>
        </div>

        <!-- Features Section -->
        <v-row justify="center" class="mb-6">
          <v-col cols="12" lg="10" xl="8">
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <div class="feature-card">
                  <div class="feature-icon">
                    <v-icon size="32" color="primary">mdi-shield-alert</v-icon>
                  </div>
                  <h3 class="feature-title">Phishing Detection</h3>
                  <p class="feature-desc">Identifies malicious URLs, fake login pages, and credential theft attempts</p>
                </div>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <div class="feature-card">
                  <div class="feature-icon">
                    <v-icon size="32" color="warning">mdi-account-alert</v-icon>
                  </div>
                  <h3 class="feature-title">Social Engineering</h3>
                  <p class="feature-desc">Detects manipulation tactics, urgency triggers, and psychological attack patterns</p>
                </div>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <div class="feature-card">
                  <div class="feature-icon">
                    <v-icon size="32" color="error">mdi-email-alert</v-icon>
                  </div>
                  <h3 class="feature-title">Email Threats</h3>
                  <p class="feature-desc">Analyzes email headers, sender authenticity, and malicious attachments</p>
                </div>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <div class="feature-card">
                  <div class="feature-icon">
                    <v-icon size="32" color="success">mdi-message-badge</v-icon>
                  </div>
                  <h3 class="feature-title">SMS Scams</h3>
                  <p class="feature-desc">Identifies smishing attempts, fake delivery notices, and financial scams</p>
                </div>
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <!-- Main Content -->
        <v-row justify="center">
          <v-col cols="12" lg="10" xl="8">
            <AnalyzerTabs />
          </v-col>
        </v-row>
        
        <!-- Footer -->
        <div class="footer-text">
          <p class="text-caption text-grey-lighten-1">
            Powered by DeepSeek V3.1 &amp; BERT • Protecting digital communications since 2025
          </p>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import AnalyzerTabs from "./components/AnalyzerTabs.vue";
</script>

<style scoped>
/* Animated Background */
.animated-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('./assets/bg.gif');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 0;
  filter: brightness(1.1) contrast(1.1);
}

.bg-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    rgba(13, 27, 42, 0.65) 0%, 
    rgba(27, 38, 59, 0.55) 50%,
    rgba(13, 27, 42, 0.65) 100%);
  backdrop-filter: blur(2px);
  z-index: 1;
}

.main-container {
  position: relative;
  z-index: 2;
  min-height: 100vh;
  padding-top: 2rem;
  padding-bottom: 3rem;
}

/* Hero Section */
.hero-section {
  margin-bottom: 3rem;
  animation: fadeInDown 0.8s ease-out;
}

.logo-container {
  animation: float 3s ease-in-out infinite;
}

.logo-img {
  width: 80px;
  height: 80px;
  filter: drop-shadow(0 0 20px rgba(103, 58, 183, 0.6));
}

.hero-title {
  font-size: clamp(3rem, 8vw, 5rem);
  font-weight: 900;
  letter-spacing: -2px;
  margin-bottom: 1rem;
  text-shadow: 0 0 40px rgba(103, 58, 183, 0.5);
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 3s ease infinite;
  background-size: 200% auto;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.hero-subtitle {
  font-size: 1.1rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  text-transform: uppercase;
  letter-spacing: 3px;
}

.hero-description {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  max-width: 700px;
  margin: 0 auto 1.5rem;
  line-height: 1.6;
}

.feature-badges {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
}

.glass-chip {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white !important;
  font-weight: 500;
}

/* Footer */
.footer-text {
  text-align: center;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Animations */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Features Section */
.feature-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  height: 100%;
  animation: fadeInUp 0.6s ease-out;
}

.feature-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(103, 58, 183, 0.5);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(103, 58, 183, 0.3);
}

.feature-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(103, 58, 183, 0.15);
  border-radius: 50%;
  border: 2px solid rgba(103, 58, 183, 0.3);
}

.feature-title {
  font-size: 1rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.feature-desc {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.4;
  margin: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 960px) {
  .hero-title {
    font-size: 3rem;
  }
  
  .hero-description {
    font-size: 0.9rem;
  }
  
  .logo-img {
    width: 60px;
    height: 60px;
  }
  
  .feature-card {
    margin-bottom: 1rem;
  }
}
</style>
