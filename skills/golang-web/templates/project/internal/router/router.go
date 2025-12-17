// internal/router/router.go
package router

import (
	"github.com/gin-gonic/gin"
	"github.com/yourname/myapp/configs"
	"github.com/yourname/myapp/internal/handlers"
)

// Setup configures and returns the router
func Setup(cfg *configs.Config, userHandler *handlers.UserHandler) *gin.Engine {
	// Set Gin mode
	if cfg.Server.Mode == "release" {
		gin.SetMode(gin.ReleaseMode)
	}

	r := gin.New()

	// Middleware
	r.Use(gin.Recovery())
	r.Use(gin.Logger())

	// Health check
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})

	// API v1
	v1 := r.Group("/api/v1")
	{
		// Users
		users := v1.Group("/users")
		{
			users.POST("", userHandler.Create)
			users.GET("/:id", userHandler.Get)
			users.PUT("/:id", userHandler.Update)
			users.DELETE("/:id", userHandler.Delete)
		}
	}

	return r
}
