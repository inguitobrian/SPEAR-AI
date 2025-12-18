/**
 * Composable for managing content input across different tabs
 */
import { ref, computed } from 'vue';

export function useContentManagement() {
  const activeTab = ref("url");
  const urlContent = ref("");
  const emailContent = ref("");
  const smsContent = ref("");

  /**
   * Get current tab's content
   */
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

  /**
   * Get current content type
   */
  const currentContentType = computed(() => activeTab.value.toLowerCase());

  /**
   * Paste content from clipboard
   */
  const pasteFromClipboard = async (type) => {
    try {
      const text = await navigator.clipboard.readText();
      setContent(type, text);
      return { success: true };
    } catch (err) {
      console.error('Failed to read clipboard:', err);
      return { 
        success: false, 
        error: "Could not read clipboard. Please paste manually." 
      };
    }
  };

  /**
   * Set content for specific type
   */
  const setContent = (type, value) => {
    if (type === 'url') urlContent.value = value;
    else if (type === 'email') emailContent.value = value;
    else if (type === 'sms') smsContent.value = value;
  };

  /**
   * Clear content for specific type
   */
  const clearContent = (type) => {
    setContent(type, '');
  };

  /**
   * Clear all content
   */
  const clearAllContent = () => {
    urlContent.value = '';
    emailContent.value = '';
    smsContent.value = '';
  };

  /**
   * Load sample data
   */
  const loadSample = (type, sample) => {
    setContent(type, sample.content);
  };

  /**
   * Upload and read file content
   */
  const uploadFile = (type, acceptedTypes = '.eml,.txt,.msg') => {
    return new Promise((resolve, reject) => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = acceptedTypes;
      
      input.onchange = async (e) => {
        const file = e.target.files[0];
        if (file) {
          try {
            const text = await file.text();
            setContent(type, text);
            resolve({ success: true, fileName: file.name });
          } catch (error) {
            reject({ success: false, error: 'Failed to read file' });
          }
        }
      };

      input.oncancel = () => {
        resolve({ success: false, cancelled: true });
      };

      input.click();
    });
  };

  return {
    activeTab,
    urlContent,
    emailContent,
    smsContent,
    currentContent,
    currentContentType,
    pasteFromClipboard,
    setContent,
    clearContent,
    clearAllContent,
    loadSample,
    uploadFile,
  };
}
