import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [sessionKey] = useState(() => {
    const storedSessionKey = sessionStorage.getItem(
      'chatbot_session_key',
    )

    if (storedSessionKey) {
      return storedSessionKey
    }

    const newSessionKey = `frontend-${crypto.randomUUID()}`

    sessionStorage.setItem(
      'chatbot_session_key',
      newSessionKey,
    )

    return newSessionKey
  })

  const [messages, setMessages] = useState([])
  const [message, setMessage] = useState('')
  const [image, setImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [currentStep, setCurrentStep] = useState('GREETING')

  useEffect(() => {
    const loadSession = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/conversations/${sessionKey}/`,
        )

        if (!response.ok) {
          throw new Error(
            'No fue posible recuperar la sesión.',
          )
        }

        const sessionData = await response.json()

        setCurrentStep(sessionData.current_step)
      } catch (requestError) {
          console.error(requestError)
        }
      }
      
    loadSession()
  }, [sessionKey])
  
  const sendRequest = async ({
    message: text = '',
    image: selectedImage = null,
  }) => {
    setLoading(true)
    setError('')

    const formData = new FormData()

    formData.append('session_key', sessionKey)

    if (text) {
      formData.append('message', text)
    }

    if (selectedImage) {
      formData.append('image', selectedImage)
    }

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/conversations/',
        {
          method: 'POST',
          body: formData,
        },
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail ||
            'Ocurrió un error al comunicarse con el servidor.',
        )
      }

      const conversationData = data.data

      setCurrentStep(conversationData.current_step)

      const userMessage = text
        ? text
        : selectedImage
          ? '📷 Recibo enviado'
          : ''

      if (userMessage) {
        setMessages((previousMessages) => [
          ...previousMessages,
          {
            role: 'user',
            content: userMessage,
          },
          {
            role: 'assistant',
            content: conversationData.message,
            data: conversationData.data,
            currentStep: conversationData.current_step,
          },
        ])
      } else {
        setMessages((previousMessages) => [
          ...previousMessages,
          {
            role: 'assistant',
            content: conversationData.message,
            data: conversationData.data,
            currentStep: conversationData.current_step,
          },
        ])
      }
    } catch (requestError) {
      console.error(requestError)

      setError(
        requestError.message ||
          'No fue posible comunicarse con el servidor.',
      )
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async () => {
    const text = message.trim()

    if (!text || loading) {
      return
    }

    setMessage('')

    await sendRequest({
      message: text,
    })
  }

  const sendImage = async () => {
    if (!image || loading) {
      return
    }

    const selectedImage = image

    setImage(null)

    await sendRequest({
      image: selectedImage,
    })
  }

  const sendConfirmation = async (option) => {
    if (loading) {
      return
    }

    await sendRequest({
      message: option,
    })
  }

  const handleKeyDown = (event) => {
    if (
      event.key === 'Enter' &&
      !event.shiftKey
    ) {
      event.preventDefault()
      sendMessage()
    }
  }

  const isConfirming =
    currentStep === 'CONFIRMING'

  const isDone =
    currentStep === 'DONE'

  return (
    <main className="chat-page">
      <section className="chat-container">

        <header className="chat-header">
          <div className="assistant-icon">
            🤖
          </div>

          <div>
            <h1>Asistente de Gastos</h1>

            <p>
              Registro de gastos mediante conversación
            </p>
          </div>
        </header>

        <section className="messages-container">

          {messages.length === 0 && (
            <div className="welcome-message">

              <div className="welcome-icon">
                🤖
              </div>

              <h2>
                Bienvenido
              </h2>

              <p>
                Escribe <strong>Hola</strong> para comenzar.
              </p>

            </div>
          )}

          {messages.map((item, index) => (
            <div
              className={`message-row ${item.role}`}
              key={`${item.role}-${index}`}
            >

              <div className="message-bubble">

                <span className="message-role">
                  {item.role === 'user'
                    ? 'Tú'
                    : 'Asistente'}
                </span>

                <p>
                  {item.content}
                </p>

                {item.data?.expense_id && (
                  <div className="expense-card">

                    <h3>
                      Datos del gasto
                    </h3>

                    <div>
                      <strong>NIT:</strong>{' '}
                      {item.data.nit ||
                        'No disponible'}
                    </div>

                    <div>
                      <strong>Comercio:</strong>{' '}
                      {item.data.merchant_name ||
                        'No disponible'}
                    </div>

                    <div>
                      <strong>Monto:</strong>{' '}
                      {item.data.amount
                        ? `$${Number(
                            item.data.amount,
                          ).toLocaleString(
                            'es-CO',
                          )}`
                        : 'No disponible'}
                    </div>

                    <div>
                      <strong>
                        Descripción:
                      </strong>{' '}
                      {item.data.description ||
                        'No disponible'}
                    </div>

                    <div>
                      <strong>Fecha:</strong>{' '}
                      {item.data.expense_date ||
                        'No disponible'}
                    </div>

                  </div>
                )}

              </div>

            </div>
          ))}

          {loading && (
            <div className="message-row assistant">

              <div className="message-bubble">

                <span className="message-role">
                  Asistente
                </span>

                <p>
                  Procesando...
                </p>

              </div>

            </div>
          )}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

        </section>

        {isConfirming && !loading && (
          <div className="confirmation-container">

            <p>
              ¿La información del gasto es correcta?
            </p>

            <div className="confirmation-actions">

              <button
                type="button"
                className="confirm-button"
                onClick={() =>
                  sendConfirmation('1')
                }
              >
                ✓ Sí, confirmar
              </button>

              <button
                type="button"
                className="reject-button"
                onClick={() =>
                  sendConfirmation('2')
                }
              >
                ↻ No, tomar otra foto
              </button>

            </div>

          </div>
        )}

        {!isDone && !isConfirming && (
          <footer className="chat-input-container">

            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Escribe tu mensaje..."
              disabled={loading}
              rows={2}
            />

            <div className="input-actions">

              <label className="file-button">

                📎 Recibo

                <input
                  type="file"
                  accept="image/*"
                  onChange={(event) => {
                    setImage(
                      event.target.files?.[0] ||
                        null,
                    )
                  }}
                  disabled={loading}
                />

              </label>

              {image && (
                <span className="selected-file">
                  {image.name}
                </span>
              )}

              {image ? (
                <button
                  type="button"
                  onClick={sendImage}
                  disabled={loading}
                >
                  Enviar recibo
                </button>
              ) : (
                <button
                  type="button"
                  onClick={sendMessage}
                  disabled={
                    loading ||
                    !message.trim()
                  }
                >
                  Enviar
                </button>
              )}

            </div>

          </footer>
        )}

        {isDone && (
          <div className="completed-message">

            <div>
              ✓
            </div>

            <strong>
              Conversación finalizada
            </strong>

            <p>
              Gracias por utilizar el asistente.
            </p>

          </div>
        )}

      </section>
    </main>
  )
}

export default App