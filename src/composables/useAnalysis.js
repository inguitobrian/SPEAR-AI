/**
 * Composable for handling security analysis logic
 */
import { ref } from 'vue';
import { getEndpointURL, createRequestOptions } from '../config/api.config';

export function useAnalysis() {
  const analysisResults = ref(null);
  const llmAnalysis = ref(null);
  const geminiAnalysis = ref(null);
  const isAnalyzing = ref(false);
  const isLLMLoading = ref(false);
  const isGeminiLoading = ref(false);
  const errorMessage = ref(null);

  /**
   * Perform BERT-based threat detection
   */
  const performBertDetection = async (content, contentType) => {
    const url = getEndpointURL('detect');
    const options = createRequestOptions('POST', {
      content: content,
      content_type: contentType,
    });

    const response = await fetch(url, options);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Detection failed");
    }

    return await response.json();
  };

  /**
   * Perform LLM-based security analysis
   */
  const performLLMAnalysis = async (content, contentType, threatLevel, confidence) => {
    const url = getEndpointURL('analyzeLLM');
    const options = createRequestOptions('POST', {
      content: content,
      content_type: contentType,
      threat_level: threatLevel,
      confidence: confidence,
    });

    const response = await fetch(url, options);

    if (response.ok) {
      return await response.json();
    } else {
      return {
        success: false,
        analysis: "LLM analysis failed",
        error: "Could not get LLM response"
      };
    }
  };

  /**
   * Main analysis function
   */
  const analyzeContent = async (content, contentType) => {
    if (!content.trim()) return;

    isAnalyzing.value = true;
    errorMessage.value = null;
    analysisResults.value = null;
    llmAnalysis.value = null;

    try {
      // Step 1: Fast BERT detection
      const detectResult = await performBertDetection(content, contentType);
      analysisResults.value = detectResult;
      isAnalyzing.value = false;

      // Step 2: Start LLM analysis in background
      isLLMLoading.value = true;
      const llmResult = await performLLMAnalysis(
        content, 
        contentType, 
        detectResult.threatLevel, 
        detectResult.confidenceScore
      );
      llmAnalysis.value = llmResult;

    } catch (error) {
      console.error("Analysis error:", error);
      const { baseURL } = await import('../config/api.config').then(m => m.API_CONFIG);
      errorMessage.value = error.message === "Failed to fetch"
        ? `Cannot connect to the analysis server. Make sure the backend is running on ${baseURL}`
        : error.message;
    } finally {
      isAnalyzing.value = false;
      isLLMLoading.value = false;
    }
  };

  /**
   * Clear all results
   */
  const clearResults = () => {
    analysisResults.value = null;
    llmAnalysis.value = null;
    geminiAnalysis.value = null;
    errorMessage.value = null;
  };

  return {
    analysisResults,
    llmAnalysis,
    geminiAnalysis,
    isAnalyzing,
    isLLMLoading,
    isGeminiLoading,
    errorMessage,
    analyzeContent,
    clearResults,
  };
}
