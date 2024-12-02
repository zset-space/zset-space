import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider } from 'react-router-dom';
import './index.css'
import './App.css'
import App from './App.jsx'

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route index element={<App />} />
    </Route>,
  )
)

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router}/>
  </StrictMode>,
)
