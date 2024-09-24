import React, { createContext, useState, useEffect } from 'react';
import { useMsal } from '@azure/msal-react';
import { loginRequest } from '../../services/auth/authConfig';  // Import your login request config

export const AppContext = createContext();

export const AppContextProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useState(null);
  const { instance } = useMsal();

  console.log("*****App Context*****")
  console.log(accessToken)
  console.log("*********************")

  useEffect(() => {
    const initializeMsal = async () => {
      try {
        const activeAccount = instance.getActiveAccount();

        if (activeAccount) {
          // Ensure MSAL is ready before trying to acquire a token silently
          await instance.initialize();  // Ensure MSAL instance is fully initialized

          // Try to acquire the token silently
          const response = await instance.acquireTokenSilent({
            ...loginRequest,
            account: activeAccount,
          });

          setAccessToken(response.accessToken);  // Store token in context
        }
      } catch (error) {
        console.error("Silent token acquisition failed:", error);
      }
    };

    initializeMsal();
  }, [instance]);

  return (
    <AppContext.Provider value={{ accessToken, setAccessToken }}>
      {children}
    </AppContext.Provider>
  );
};
