// internal/models/user.go
package models

import "time"

// User represents a user in the system
type User struct {
	ID        string    `json:"id" gorm:"primaryKey"`
	Email     string    `json:"email" gorm:"uniqueIndex"`
	Name      string    `json:"name"`
	Password  string    `json:"-"` // Never expose password
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// TableName returns the table name for GORM
func (User) TableName() string {
	return "users"
}
