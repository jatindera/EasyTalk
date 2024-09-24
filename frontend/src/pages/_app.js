// pages/_app.js
import { MsalProvider } from '@azure/msal-react';
import { msalInstance } from '../services/auth/msal';
import { AppContextProvider } from '../services/context/appContext';
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return (
    <MsalProvider instance={msalInstance}>
      <AppContextProvider>
        <Component {...pageProps} />
      </AppContextProvider>
    </MsalProvider>
  );
}

export default MyApp;
