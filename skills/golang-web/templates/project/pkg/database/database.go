// pkg/database/database.go
package database

import (
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// Config holds database configuration
type Config struct {
	Driver   string
	Host     string
	Port     int
	Username string
	Password string
	Database string
	SSLMode  string
}

// Database wraps gorm.DB
type Database struct {
	db *gorm.DB
}

// New creates a new database connection
func New(cfg Config) (*Database, error) {
	var dialector gorm.Dialector

	switch cfg.Driver {
	case "postgres":
		dsn := fmt.Sprintf(
			"host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
			cfg.Host, cfg.Port, cfg.Username, cfg.Password, cfg.Database, cfg.SSLMode,
		)
		dialector = postgres.Open(dsn)
	case "sqlite":
		dialector = sqlite.Open(cfg.Database)
	default:
		return nil, fmt.Errorf("unsupported database driver: %s", cfg.Driver)
	}

	db, err := gorm.Open(dialector, &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

	return &Database{db: db}, nil
}

// DB returns the underlying gorm.DB
func (d *Database) DB() *gorm.DB {
	return d.db
}

// Close closes the database connection
func (d *Database) Close() error {
	sqlDB, err := d.db.DB()
	if err != nil {
		return err
	}
	return sqlDB.Close()
}

// AutoMigrate runs auto migration for given models
func (d *Database) AutoMigrate(models ...interface{}) error {
	return d.db.AutoMigrate(models...)
}
