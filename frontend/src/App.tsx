import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

// ✅ 環境変数をインポート
import { API_BASE_URL, APP_NAME } from "./config";

function App() {
  const [message, setMessage] = useState<string>('Loading...')

  useEffect(() => {
    // API Gatewayのエンドポイントを呼び出し
    fetch(`${API_BASE_URL}/api/v1/devices`)
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data)
        setMessage('API call successful! ' + JSON.stringify(data))
      })
      .catch(error => {
        console.error('Error:', error)
        setMessage('Error calling API: ' + error.message)
      })
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      
      <h1>{APP_NAME}</h1>
      <p>API Base URL: {API_BASE_URL}</p>

      <div>
        <h2>CORS Test Results:</h2>
        <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
          {message}
        </pre>
      </div>
    </>
  )
}

export default App