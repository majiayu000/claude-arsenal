// internal/services/user.go
package services

import (
	"context"
	"time"

	"github.com/google/uuid"
	"github.com/yourname/myapp/internal/models"
	"github.com/yourname/myapp/internal/repositories"
	"github.com/yourname/myapp/pkg/errors"
)

// CreateUserInput represents input for creating a user
type CreateUserInput struct {
	Email string `json:"email" binding:"required,email"`
	Name  string `json:"name" binding:"required,min=2,max=100"`
}

// UpdateUserInput represents input for updating a user
type UpdateUserInput struct {
	Name string `json:"name" binding:"omitempty,min=2,max=100"`
}

// UserService defines the interface for user business logic
type UserService interface {
	Create(ctx context.Context, input CreateUserInput) (*models.User, error)
	GetByID(ctx context.Context, id string) (*models.User, error)
	Update(ctx context.Context, id string, input UpdateUserInput) (*models.User, error)
	Delete(ctx context.Context, id string) error
}

type userService struct {
	repo repositories.UserRepository
}

// NewUserService creates a new UserService
func NewUserService(repo repositories.UserRepository) UserService {
	return &userService{repo: repo}
}

func (s *userService) Create(ctx context.Context, input CreateUserInput) (*models.User, error) {
	// Check if email already exists
	existing, err := s.repo.FindByEmail(ctx, input.Email)
	if err != nil {
		return nil, errors.Wrap(err, 500, "failed to check email")
	}
	if existing != nil {
		return nil, errors.ErrUserExists
	}

	user := &models.User{
		ID:        uuid.New().String(),
		Email:     input.Email,
		Name:      input.Name,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	saved, err := s.repo.Save(ctx, user)
	if err != nil {
		return nil, errors.Wrap(err, 500, "failed to save user")
	}

	return saved, nil
}

func (s *userService) GetByID(ctx context.Context, id string) (*models.User, error) {
	user, err := s.repo.FindByID(ctx, id)
	if err != nil {
		return nil, errors.Wrap(err, 500, "failed to get user")
	}
	if user == nil {
		return nil, errors.ErrUserNotFound
	}
	return user, nil
}

func (s *userService) Update(ctx context.Context, id string, input UpdateUserInput) (*models.User, error) {
	user, err := s.repo.FindByID(ctx, id)
	if err != nil {
		return nil, errors.Wrap(err, 500, "failed to get user")
	}
	if user == nil {
		return nil, errors.ErrUserNotFound
	}

	if input.Name != "" {
		user.Name = input.Name
	}
	user.UpdatedAt = time.Now()

	saved, err := s.repo.Save(ctx, user)
	if err != nil {
		return nil, errors.Wrap(err, 500, "failed to update user")
	}

	return saved, nil
}

func (s *userService) Delete(ctx context.Context, id string) error {
	user, err := s.repo.FindByID(ctx, id)
	if err != nil {
		return errors.Wrap(err, 500, "failed to get user")
	}
	if user == nil {
		return errors.ErrUserNotFound
	}

	if err := s.repo.Delete(ctx, id); err != nil {
		return errors.Wrap(err, 500, "failed to delete user")
	}

	return nil
}
