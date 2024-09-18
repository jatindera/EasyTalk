import { PublicClientApplication } from '@azure/msal-browser';

// MSAL Configuration
const msalConfig = {
    auth: {
        clientId: '343b6df9-9170-4484-88e7-795cf82c1fbd',
        authority: 'https://login.microsoftonline.com/9dfe9b83-837e-41d5-981b-004de9791fec', // Use 'common' for multi-tenant apps
        redirectUri: 'http://localhost:3000', // The redirect URI you registered in Azure AD
    },
};

const msalInstance = new PublicClientApplication(msalConfig);

export { msalInstance }