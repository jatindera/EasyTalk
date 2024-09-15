import React from 'react';
import { useMsal, useIsAuthenticated } from '@azure/msal-react';

function Home() {
  const { instance, accounts } = useMsal();
  const isAuthenticated = useIsAuthenticated();

  const handleLogout = () => {
    instance.logoutPopup().catch(e => {
      console.error(e);
    });
  };

  return (
    <div>
      {isAuthenticated ? (
        <div>
          <h2>Welcome, {accounts[0].name}</h2>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <p>Please log in to continue.</p>
      )}
    </div>
  );
}

export default Home;
