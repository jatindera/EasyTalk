import { PublicClientApplication } from '@azure/msal-browser';

// MSAL Configuration
export const msalConfig = {
  auth: {
    clientId: process.env.NEXT_PUBLIC_AZURE_CLIENT_ID,  // Your Azure AD app client ID
    authority: `https://login.microsoftonline.com/${process.env.NEXT_PUBLIC_AZURE_TENANT_ID}`,  // Tenant or 'common'
    redirectUri: process.env.NEXT_PUBLIC_REDIRECT_URI,  // Redirect URI
    postLogoutRedirectUri: process.env.NEXT_PUBLIC_REDIRECT_URI,  // Post logout URI
  },
  cache: {
    cacheLocation: 'sessionStorage',  // Store tokens in sessionStorage (you can use localStorage if needed)
    storeAuthStateInCookie: false,  // Do not store in cookies
  },
  system: {
    loggerOptions: {
      logLevel: 'info',  // Logging level (verbose for more detailed logs)
      loggerCallback: (level, message, containsPii) => {
        if (!containsPii) {
          switch (level) {
            case 'error':
              console.error(message);
              break;
            case 'info':
              console.info(message);
              break;
            case 'verbose':
              console.debug(message);
              break;
            case 'warning':
              console.warn(message);
              break;
            default:
              break;
          }
        }
      },
    },
  },
};

// Initialize MSAL instance
export const msalInstance = new PublicClientApplication(msalConfig);
