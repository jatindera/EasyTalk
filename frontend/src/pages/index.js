import Head from 'next/head';
import { useContext, useEffect } from 'react';
import { AuthenticatedTemplate, UnauthenticatedTemplate, useMsal } from '@azure/msal-react';
import { loginRequest } from '../services/auth/authConfig';
import { AppContext } from '../services/context/appContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FaUser, FaInstagram, FaFacebook } from 'react-icons/fa';
import ChatSection from '../components/chat/ChatSection';
import Link from 'next/link'; // Import Next.js Link component

const Home = () => {
  const { instance } = useMsal();
  const { setAccessToken } = useContext(AppContext);

  const handleLogin = () => {
    instance.loginPopup(loginRequest)
      .then(response => {
        const account = response.account;
        instance.setActiveAccount(account);

        instance.acquireTokenSilent({
          ...loginRequest,
          account: account
        })
          .then(response => {
            // console.log("Access Token:", response.accessToken);
            // Store the access token using context
            setAccessToken(response.accessToken);
          })
          .catch(error => {
            console.error("Failed to acquire access token silently:", error);
            instance.acquireTokenPopup({
              ...loginRequest,
              account: account
            })
              .then(response => {
                // console.log("Access Token:", response.accessToken);
                // Store the access token using context
                setAccessToken(response.accessToken);
              })
              .catch(error => {
                console.error("Failed to acquire access token:", error);
              });
          });
      })
      .catch(e => {
        console.error("Login failed:", e);
      });
  };

  return (
    <div className="d-flex flex-column vh-100" style={{ backgroundColor: '#1c1c1c' }}>
      <Head>
        <title>Easy Talk</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Header Section */}
      <header className="navbar navbar-expand-lg" style={{ backgroundColor: '#343a40', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)' }}>
        <a className="navbar-brand text-white" href="#">Easy Talk</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <a className="nav-link text-white" href="#">Home</a>
            </li>
            <li className="nav-item">
              <a className="nav-link text-white" href="#">Features</a>
            </li>
            <UnauthenticatedTemplate>
              <li className="nav-item">
                <button className="btn btn-primary" onClick={handleLogin}>Login</button>
              </li>
            </UnauthenticatedTemplate>
            <AuthenticatedTemplate>
              <li className="nav-item">
                <a className="nav-link text-white" href="#" aria-label="User">
                  <FaUser size={20} className="ms-2" />
                </a>
              </li>
            </AuthenticatedTemplate>
          </ul>
        </div>
      </header>

      {/* Chat Section */}
      <ChatSection />

      {/* Footer Section */}
      <footer className="bg-dark py-3">
        <div className="container">
          <div className="d-flex justify-content-between">
            <div>
              <Link href="/privacy-policy" className="text-white">Privacy Policy</Link> |
              <Link href="/terms-of-service" className="text-white">Terms of Service</Link>
            </div>
            <div>
              <Link href="/contact" className="text-white">Contact</Link> |
              <Link href="/feedback" className="text-white">Feedback</Link> |
              <a href="#" className="text-white">Follow Us</a> |
              <a href="#" className="text-white">Subscribe</a>
            </div>
            <div>
              <span className="text-white">Follow us:</span>
              <a href="#" className="ms-2 text-white" aria-label="Instagram"><FaInstagram /></a>
              <a href="#" className="ms-2 text-white" aria-label="Facebook"><FaFacebook /></a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
