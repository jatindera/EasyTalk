// pages/_app.js
import { MsalProvider } from '@azure/msal-react';
import { msalInstance } from '../services/auth/msal';
import { AuthProvider } from '../services/auth/authContext'; // Import AuthProvider
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return (
    <MsalProvider instance={msalInstance}>
      {/* Wrap AuthProvider around your component */}
      <AuthProvider>
        <Component {...pageProps} />
      </AuthProvider>
    </MsalProvider>
  );
}

export default MyApp;
