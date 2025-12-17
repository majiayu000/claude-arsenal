// pkg/response/response.go
package response

import (
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
	apperrors "github.com/yourname/myapp/pkg/errors"
)

// Response represents a unified API response
type Response struct {
	Code    int         `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"data,omitempty"`
}

// Success sends a success response
func Success(c *gin.Context, data interface{}) {
	c.JSON(http.StatusOK, Response{
		Code:    0,
		Message: "success",
		Data:    data,
	})
}

// Created sends a 201 created response
func Created(c *gin.Context, data interface{}) {
	c.JSON(http.StatusCreated, Response{
		Code:    0,
		Message: "created",
		Data:    data,
	})
}

// NoContent sends a 204 no content response
func NoContent(c *gin.Context) {
	c.Status(http.StatusNoContent)
}

// Error sends an error response
func Error(c *gin.Context, err error) {
	var appErr *apperrors.AppError
	if errors.As(err, &appErr) {
		c.JSON(appErr.HTTPStatus(), Response{
			Code:    appErr.Code,
			Message: appErr.Message,
		})
		return
	}

	// Unknown error
	c.JSON(http.StatusInternalServerError, Response{
		Code:    500,
		Message: "internal server error",
	})
}

// ErrorWithMessage sends an error response with custom message
func ErrorWithMessage(c *gin.Context, status int, code int, message string) {
	c.JSON(status, Response{
		Code:    code,
		Message: message,
	})
}

// BadRequest sends a 400 bad request response
func BadRequest(c *gin.Context, message string) {
	c.JSON(http.StatusBadRequest, Response{
		Code:    400,
		Message: message,
	})
}

// Unauthorized sends a 401 unauthorized response
func Unauthorized(c *gin.Context, message string) {
	c.JSON(http.StatusUnauthorized, Response{
		Code:    401,
		Message: message,
	})
}

// NotFound sends a 404 not found response
func NotFound(c *gin.Context, message string) {
	c.JSON(http.StatusNotFound, Response{
		Code:    404,
		Message: message,
	})
}
