/**
 * Application entry point.
 *
 * Mounts the React application inside the ``#root`` DOM element with
 * StrictMode enabled and the Redux store provider wrapping the App.
 */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { Provider } from 'react-redux'
import { store } from './app/store.js'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}> 
      <App />
    </Provider>
  </StrictMode>,
)
