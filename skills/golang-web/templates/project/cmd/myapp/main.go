// cmd/myapp/main.go
package main

import (
	"log/slog"
	"os"

	"github.com/yourname/myapp/configs"
	"github.com/yourname/myapp/internal/handlers"
	"github.com/yourname/myapp/internal/repositories"
	"github.com/yourname/myapp/internal/router"
	"github.com/yourname/myapp/internal/services"
	"github.com/yourname/myapp/pkg/database"
	"github.com/yourname/myapp/pkg/server"
)

func main() {
	// Initialize logger
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	}))
	slog.SetDefault(logger)

	// Load configuration
	cfg := configs.Load()

	// Initialize database
	db, err := database.New(cfg.Database)
	if err != nil {
		slog.Error("failed to connect to database", "error", err)
		os.Exit(1)
	}
	defer db.Close()

	// Initialize repositories
	userRepo := repositories.NewUserRepository(db.DB())

	// Initialize services
	userService := services.NewUserService(userRepo)

	// Initialize handlers
	userHandler := handlers.NewUserHandler(userService)

	// Setup router
	r := router.Setup(cfg, userHandler)

	// Start server
	srv := server.New(r,
		server.WithPort(cfg.Server.Port),
		server.WithReadTimeout(cfg.Server.ReadTimeout),
		server.WithWriteTimeout(cfg.Server.WriteTimeout),
	)

	if err := srv.Run(); err != nil {
		slog.Error("server error", "error", err)
		os.Exit(1)
	}
}
