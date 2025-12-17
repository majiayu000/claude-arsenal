// pkg/server/server.go
package server

import (
	"context"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

// Server represents an HTTP server with graceful shutdown
type Server struct {
	port         int
	readTimeout  time.Duration
	writeTimeout time.Duration
	handler      http.Handler
}

// Option is a functional option for Server
type Option func(*Server)

// WithPort sets the server port
func WithPort(port int) Option {
	return func(s *Server) {
		s.port = port
	}
}

// WithReadTimeout sets the read timeout
func WithReadTimeout(d time.Duration) Option {
	return func(s *Server) {
		s.readTimeout = d
	}
}

// WithWriteTimeout sets the write timeout
func WithWriteTimeout(d time.Duration) Option {
	return func(s *Server) {
		s.writeTimeout = d
	}
}

// New creates a new Server with options
func New(handler http.Handler, opts ...Option) *Server {
	s := &Server{
		port:         8080,
		readTimeout:  30 * time.Second,
		writeTimeout: 30 * time.Second,
		handler:      handler,
	}

	for _, opt := range opts {
		opt(s)
	}

	return s
}

// Run starts the server with graceful shutdown
func (s *Server) Run() error {
	srv := &http.Server{
		Addr:         fmt.Sprintf(":%d", s.port),
		Handler:      s.handler,
		ReadTimeout:  s.readTimeout,
		WriteTimeout: s.writeTimeout,
	}

	// Channel for server errors
	errChan := make(chan error, 1)

	go func() {
		slog.Info("server starting", "port", s.port)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			errChan <- err
		}
	}()

	// Channel for OS signals
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

	// Block until signal or error
	select {
	case err := <-errChan:
		return fmt.Errorf("server error: %w", err)
	case sig := <-quit:
		slog.Info("shutdown signal received", "signal", sig)
	}

	// Graceful shutdown
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		return fmt.Errorf("server shutdown error: %w", err)
	}

	slog.Info("server stopped gracefully")
	return nil
}
