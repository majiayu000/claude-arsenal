// internal/handlers/user.go
package handlers

import (
	"github.com/gin-gonic/gin"
	"github.com/yourname/myapp/internal/services"
	"github.com/yourname/myapp/pkg/errors"
	"github.com/yourname/myapp/pkg/response"
)

// UserHandler handles user-related HTTP requests
type UserHandler struct {
	service services.UserService
}

// NewUserHandler creates a new UserHandler
func NewUserHandler(service services.UserService) *UserHandler {
	return &UserHandler{service: service}
}

// Create handles POST /users
func (h *UserHandler) Create(c *gin.Context) {
	var input services.CreateUserInput
	if err := c.ShouldBindJSON(&input); err != nil {
		response.Error(c, errors.ErrInvalidParams)
		return
	}

	user, err := h.service.Create(c.Request.Context(), input)
	if err != nil {
		response.Error(c, err)
		return
	}

	response.Created(c, user)
}

// Get handles GET /users/:id
func (h *UserHandler) Get(c *gin.Context) {
	id := c.Param("id")

	user, err := h.service.GetByID(c.Request.Context(), id)
	if err != nil {
		response.Error(c, err)
		return
	}

	response.Success(c, user)
}

// Update handles PUT /users/:id
func (h *UserHandler) Update(c *gin.Context) {
	id := c.Param("id")

	var input services.UpdateUserInput
	if err := c.ShouldBindJSON(&input); err != nil {
		response.Error(c, errors.ErrInvalidParams)
		return
	}

	user, err := h.service.Update(c.Request.Context(), id, input)
	if err != nil {
		response.Error(c, err)
		return
	}

	response.Success(c, user)
}

// Delete handles DELETE /users/:id
func (h *UserHandler) Delete(c *gin.Context) {
	id := c.Param("id")

	if err := h.service.Delete(c.Request.Context(), id); err != nil {
		response.Error(c, err)
		return
	}

	response.NoContent(c)
}
