// internal/repositories/user.go
package repositories

import (
	"context"
	"errors"

	"github.com/yourname/myapp/internal/models"
	"gorm.io/gorm"
)

// UserRepository defines the interface for user data access
type UserRepository interface {
	FindByID(ctx context.Context, id string) (*models.User, error)
	FindByEmail(ctx context.Context, email string) (*models.User, error)
	Save(ctx context.Context, user *models.User) (*models.User, error)
	Delete(ctx context.Context, id string) error
}

type userRepository struct {
	db *gorm.DB
}

// NewUserRepository creates a new UserRepository
func NewUserRepository(db *gorm.DB) UserRepository {
	return &userRepository{db: db}
}

func (r *userRepository) FindByID(ctx context.Context, id string) (*models.User, error) {
	var user models.User
	if err := r.db.WithContext(ctx).First(&user, "id = ?", id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return &user, nil
}

func (r *userRepository) FindByEmail(ctx context.Context, email string) (*models.User, error) {
	var user models.User
	if err := r.db.WithContext(ctx).First(&user, "email = ?", email).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return &user, nil
}

func (r *userRepository) Save(ctx context.Context, user *models.User) (*models.User, error) {
	if err := r.db.WithContext(ctx).Save(user).Error; err != nil {
		return nil, err
	}
	return user, nil
}

func (r *userRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&models.User{}, "id = ?", id).Error
}
