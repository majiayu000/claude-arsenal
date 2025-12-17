// pkg/errors/errors.go
package errors

import "fmt"

// AppError represents an application error with code and message
type AppError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
	Cause   error  `json:"-"`
}

func (e *AppError) Error() string {
	if e.Cause != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.Cause)
	}
	return e.Message
}

func (e *AppError) Unwrap() error {
	return e.Cause
}

// HTTPStatus returns the HTTP status code for this error
func (e *AppError) HTTPStatus() int {
	switch {
	case e.Code >= 500:
		return 500
	case e.Code >= 400:
		return e.Code
	default:
		return 500
	}
}

// New creates a new AppError
func New(code int, message string) *AppError {
	return &AppError{
		Code:    code,
		Message: message,
	}
}

// Wrap wraps an existing error with additional context
func Wrap(err error, code int, message string) *AppError {
	if err == nil {
		return nil
	}
	return &AppError{
		Code:    code,
		Message: message,
		Cause:   err,
	}
}

// Wrapf wraps an error with formatted message
func Wrapf(err error, code int, format string, args ...interface{}) *AppError {
	if err == nil {
		return nil
	}
	return &AppError{
		Code:    code,
		Message: fmt.Sprintf(format, args...),
		Cause:   err,
	}
}

// Predefined errors
var (
	ErrInternal      = New(500, "internal server error")
	ErrInvalidParams = New(400, "invalid parameters")
	ErrNotFound      = New(404, "resource not found")
	ErrUnauthorized  = New(401, "unauthorized")
	ErrForbidden     = New(403, "forbidden")
	ErrConflict      = New(409, "resource already exists")
)

// Specific errors
var (
	ErrUserNotFound = New(404, "user not found")
	ErrUserExists   = New(409, "user already exists")
	ErrInvalidToken = New(401, "invalid token")
)
