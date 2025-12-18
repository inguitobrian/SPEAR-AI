/**
 * Sample threat data for testing and demonstration
 */

export const sampleUrls = [
  { 
    label: "Fake PayPal Login", 
    content: "https://paypaI-secure-login.com/verify" 
  },
  { 
    label: "Banking Phish", 
    content: "https://secure-bank-verify.net/account/confirm" 
  },
  { 
    label: "Package Scam", 
    content: "https://usps-delivery-track.com/package/claim" 
  },
  { 
    label: "Crypto Wallet", 
    content: "https://metamask-wallet-verify.net/unlock" 
  }
];

export const sampleEmails = [
  { 
    label: "Urgent Account Verification",
    content: `Subject: URGENT: Verify Your Account Now!

Dear Customer,

Your account has been locked due to suspicious activity. Click here immediately to verify your identity:
http://secure-verify-now.com

Failure to verify within 24 hours will result in permanent account closure.

Best regards,
Security Team`
  },
  { 
    label: "Prize Winner Notification",
    content: `Subject: Congratulations! You've Won $10,000!

Dear Lucky Winner,

You have been selected as our grand prize winner! To claim your prize, please provide your banking details at:
http://claim-prize-now.com

Act fast - offer expires soon!

Winner ID: #${Math.random().toString(36).substring(7).toUpperCase()}`
  },
  { 
    label: "CEO Impersonation",
    content: `Subject: Urgent Wire Transfer Needed

Hi,

I need you to process an urgent wire transfer of $50,000 to our new vendor. Please handle this immediately and discreetly.

Send to: account@newvendor-payments.com

Thanks,
CEO`
  },
  { 
    label: "Tax Document Scam",
    content: `Subject: Your Tax Refund is Ready

Dear Taxpayer,

Your tax refund of $2,847.00 is ready for processing. Please verify your bank details here:
http://irs-tax-refund-gov.com/verify

You must claim within 48 hours or the refund will be forfeited.

IRS Tax Division`
  }
];

export const sampleSMS = [
  { 
    label: "Delivery Scam",
    content: "USPS: Your package is waiting. Confirm delivery address: http://usps-track.net/confirm"
  },
  { 
    label: "Bank Alert",
    content: "ALERT: Suspicious activity on your account. Verify now: http://secure-bank.net/verify or your account will be locked."
  },
  { 
    label: "Tax Refund",
    content: "IRS: You're eligible for a $2,847 tax refund. Claim here: http://irs-refund-claim.com/process"
  },
  { 
    label: "Apple ID Locked",
    content: "Apple: Your Apple ID has been locked. Unlock immediately: http://appleid-unlock.com/restore"
  },
  { 
    label: "Netflix Expired",
    content: "Netflix: Your payment failed. Update payment info: http://netflix-billing.net/update to avoid suspension."
  }
];

/**
 * Get samples by type
 */
export function getSamplesByType(type) {
  switch(type) {
    case 'url':
      return sampleUrls;
    case 'email':
      return sampleEmails;
    case 'sms':
      return sampleSMS;
    default:
      return [];
  }
}
