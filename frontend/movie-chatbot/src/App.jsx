"use client"

import { useState, useEffect, useRef } from "react"
import "./App.css"

// npm install lucide-react

import { Send, Star, Calendar, TrendingUp, ExternalLink } from "lucide-react"

function App() {
  const [messages, setMessages] = useState([
    {
      type: "bot",
      content:
        "Hi! I'm your movie recommendation assistant. Tell me what kind of movies you're in the mood for, and I'll suggest some great options!",
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false) //use to prevent clicking during loading 

  const messagesEndRef = useRef(null)

  const handleSubmit = async (e) => {
    e.preventDefault() //prevent browser refresh
    if (!input.trim() || isLoading) return //dont perform if laoding or no input

    const userMessage = input.trim()
    setInput("") //clear input after user submits 

    // Add user message, use prev state to prevent some messages not going through on doubel clicks 
    setMessages((prev) => [...prev, { type: "user", content: userMessage }])
    setIsLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: userMessage }),
      })

      if (!response.ok) {
        throw new Error("Failed to get recommendations")
      }

      const movies = await response.json()

      // Add bot response with movies
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          content: `Here are some great movie recommendations based on "${userMessage}":`,
          movies,
        },
      ])
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          content: "Sorry, I couldn't get recommendations right now. Please try again later.",
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const getStreamingLinks = (title) => {
    return [
      { name: "XPrime.tv", url: `https://xprime.tv/search?query=${encodeURIComponent(title)}` },
      { name: "Mapple.tv", url: `https://mapple.tv/search?q=${encodeURIComponent(title)}`},
      { name: "Netflix", url: `https://www.netflix.com/search?q=${encodeURIComponent(title)}` },
      { name: "Prime Video", url: `https://www.amazon.com/s?k=${encodeURIComponent(title)}&i=prime-video` },
      { name: "Hulu", url: `https://www.hulu.com/search?q=${encodeURIComponent(title)}` },
      { name: "Disney+", url: `https://www.disneyplus.com/search?q=${encodeURIComponent(title)}` },
    ]
  }

  const formatGenres = (genres) => {
    try {
      const parsed = JSON.parse(genres.replace(/'/g, '"'))
      return parsed.map((g) => g.name).join(", ")
    } catch {
      return genres
    }
  }

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <div className="header">
          <h1>Film Prescriber</h1>
          <p>Discover your next favorite movie with Embedding-powered recommendations</p>
        </div>

        {/* Chat Messages */}
        <div className="chat-container">
          <div className="messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.type}`}> {/* index needed here to be able to update messages, also discerns if bot or user message*/}
                <div className="message-content">
                  <p>{message.content}</p>

                  {/* Movie Cards */}
                  {message.movies && (
                    <div className="movie-grid">
                      {message.movies.map((movie, movieIndex) => (
                        <div key={movieIndex} className="movie-card">
                          <div className="movie-poster">
                            <img
                              src={
                                movie.poster_path
                        
                                  ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` 
                                  : `https://via.placeholder.com/300x450/374151/ffffff?text=${encodeURIComponent(movie.title)}`
                              } 
                              alt={movie.title}
                            />
                            <div className="rating">
                              <Star size={12} />
                              <span>{movie.vote_average.toFixed(1)}</span>
                            </div>
                          </div>

                          <div className="movie-info">
                            <h3>{movie.title}</h3>

                            <div className="movie-meta">
                              <div className="meta-item">
                                <Calendar size={12} />
                                <span>{new Date(movie["release date"]).getFullYear()}</span>
                              </div>
                              <div className="meta-item">
                                <TrendingUp size={12} />
                                <span>{Math.round(movie.popularity)}</span>
                              </div>
                            </div>

                            <div className="genres">
                              <span className="genre-badge">{formatGenres(movie.genres)}</span>
                            </div>

                            <p className="overview">{movie.overview}</p>

                            <div className="streaming-links">
                              <p className="watch-label">Watch on:</p>
                              <div className="links">
                                {getStreamingLinks(movie.title).map((link, linkIndex) => (
                                  <button
                                    key={linkIndex}
                                    className="streaming-btn"
                                    onClick={() => window.open(link.url, "_blank")}
                                  >
                                    {link.name}
                                    <ExternalLink size={12} />
                                  </button>
                                ))}
                              </div>
                            </div>

                            <div className="match-score">
                              <span>Match: {(movie.score * 100).toFixed(1)}%</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message bot">
                <div className="message-content">
                  <div className="loading">
                    <div className="spinner"></div>
                    <span>Finding perfect movies for you...</span>
                  </div>
                </div>
              </div>
            )}

            {/* Auto-scroll target */}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)} //update on every keystroke
            placeholder="What kind of movies are you in the mood for? (e.g., 'action movies with superheroes', 'romantic comedies', 'sci-fi thrillers')"
            disabled={isLoading}
            className="message-input"
          />
          <button type="submit" disabled={isLoading || !input.trim()} className="send-btn">
            <Send size={16} />
          </button>
        </form>

        {/* Example Queries */}
        <div className="examples">
          <div className="example-buttons">
            {[
              "Fight Club",
              "Lonely movies like Bladerunner 2049",
              "Drive, heist",
              "Pulp Fiction",
            ].map((example, index) => (
              <button key={index} className="example-btn" onClick={() => setInput(example)} disabled={isLoading}>
                {example}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
