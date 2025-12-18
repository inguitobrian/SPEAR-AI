/**
 * UI Constants and Configuration
 */

// Content Types
export const CONTENT_TYPES = {
  URL: 'url',
  EMAIL: 'email',
  SMS: 'sms',
};

// Threat Levels
export const THREAT_LEVELS = {
  MALICIOUS: 'malicious',
  SUSPICIOUS: 'suspicious',
  SAFE: 'safe',
};

// Risk Levels
export const RISK_LEVELS = {
  CRITICAL: 'CRITICAL',
  HIGH: 'HIGH',
  MEDIUM: 'MEDIUM',
  LOW: 'LOW',
};

// Tab Configuration
export const TABS_CONFIG = [
  {
    value: CONTENT_TYPES.URL,
    label: 'URL',
    icon: 'mdi-link-variant',
  },
  {
    value: CONTENT_TYPES.EMAIL,
    label: 'Email',
    icon: 'mdi-email-outline',
  },
  {
    value: CONTENT_TYPES.SMS,
    label: 'SMS',
    icon: 'mdi-message-text-outline',
  },
];

// Input Placeholders
export const PLACEHOLDERS = {
  [CONTENT_TYPES.URL]: 'https://suspicious-example.com',
  [CONTENT_TYPES.EMAIL]: 'Paste the full email content here, including headers if available...',
  [CONTENT_TYPES.SMS]: 'Paste the SMS message content here...',
};

// Input Descriptions
export const DESCRIPTIONS = {
  [CONTENT_TYPES.URL]: 'Enter a suspicious URL to analyze for phishing threats',
  [CONTENT_TYPES.EMAIL]: 'Paste email content to detect social engineering attacks',
  [CONTENT_TYPES.SMS]: 'Analyze SMS messages for malicious content and scams',
};

// Color Mappings
export const THREAT_COLORS = {
  [THREAT_LEVELS.MALICIOUS]: 'error',
  [THREAT_LEVELS.SUSPICIOUS]: 'warning',
  [THREAT_LEVELS.SAFE]: 'success',
};

export const RISK_COLORS = {
  [RISK_LEVELS.CRITICAL]: 'error',
  [RISK_LEVELS.HIGH]: 'orange',
  [RISK_LEVELS.MEDIUM]: 'warning',
  [RISK_LEVELS.LOW]: 'success',
};

// Icon Mappings
export const THREAT_ICONS = {
  [THREAT_LEVELS.MALICIOUS]: 'mdi-alert-octagon',
  [THREAT_LEVELS.SUSPICIOUS]: 'mdi-alert-circle',
  [THREAT_LEVELS.SAFE]: 'mdi-check-circle',
};

// File Upload Settings
export const FILE_UPLOAD_CONFIG = {
  [CONTENT_TYPES.EMAIL]: {
    accept: '.eml,.txt,.msg',
    maxSize: 5 * 1024 * 1024, // 5MB
  },
};
