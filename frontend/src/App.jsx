import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [context, setContext] = useState('')
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setAnswer(null)

    try {
      const response = await fetch('http://localhost:8000/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, context }),
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to get answer')
      }
      setAnswer(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Question Answering</h1>
      <form onSubmit={handleSubmit}>
        <div className="field">
          <label>Question</label>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your question"
            required
          />
        </div>
        <div className="field">
          <label>Context</label>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Enter the context text"
            rows={5}
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Getting Answer...' : 'Get Answer'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {answer && (
        <div className="result">
          <h2>Answer</h2>
          <p className="answer-text">{answer.answer}</p>
          <p className="score">Confidence: {(answer.score * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  )
}

export default App
