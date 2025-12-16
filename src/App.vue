<template>
  <v-app>
    <v-main>
      <v-container fluid class="fill-height">
        <v-row justify="center" align="center" class="fill-height">
          <v-col cols="12" md="8" lg="6">
            <div class="text-center mb-6">
              <h1 class="text-h2 text-primary mb-4">SPEAR AI</h1>
              <p class="text-h6 text-grey-darken-1">AI-Powered Analysis Tool</p>
            </div>

            <AnalyzerTabs />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import AnalyzerTabs from "./components/AnalyzerTabs.vue";
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>
