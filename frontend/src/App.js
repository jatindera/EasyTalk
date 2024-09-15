import React from 'react';
import { useMsal } from '@azure/msal-react';
import { loginRequest } from './authConfig';
import Home from './Home';

function App() {
  const { instance } = useMsal();

  const handleLogin = () => {
    instance.loginPopup(loginRequest)
      .then(() => {
        // Acquire the access token after successful login
        instance.acquireTokenSilent(loginRequest)
          .then(response => {
            console.log("Access Token:", response.accessToken);
          })
          .catch(error => {
            console.error("Failed to acquire access token silently:", error);
            // Fallback to acquire token via popup if silent acquisition fails
            instance.acquireTokenPopup(loginRequest)
              .then(response => {
                console.log("Access Token:", response.accessToken);
              })
              .catch(error => {
                console.error("Failed to acquire access token:", error);
              });
          });
      })
      .catch(e => {
        console.error(e);
      });
  };

  return (
    <div>
      <h1>Azure AD Authentication with React</h1>
      <button onClick={handleLogin}>Login</button>
      <Home />
    </div>
  );
}

export default App;
