// configs/config.go
package configs

import (
	"strings"
	"time"

	"github.com/spf13/viper"
)

type Config struct {
	Server   ServerConfig   `mapstructure:"server"`
	Database DatabaseConfig `mapstructure:"database"`
	Log      LogConfig      `mapstructure:"log"`
	LLM      LLMConfig      `mapstructure:"llm"`
}

type ServerConfig struct {
	Port         int           `mapstructure:"port"`
	Mode         string        `mapstructure:"mode"`
	ReadTimeout  time.Duration `mapstructure:"read_timeout"`
	WriteTimeout time.Duration `mapstructure:"write_timeout"`
}

type DatabaseConfig struct {
	Driver   string `mapstructure:"driver"`
	Host     string `mapstructure:"host"`
	Port     int    `mapstructure:"port"`
	Username string `mapstructure:"username"`
	Password string `mapstructure:"password"`
	Database string `mapstructure:"database"`
	SSLMode  string `mapstructure:"ssl_mode"`
}

type LogConfig struct {
	Level  string `mapstructure:"level"`
	Format string `mapstructure:"format"`
}

type LLMConfig struct {
	BaseURL      string `mapstructure:"base_url"`
	APIKey       string `mapstructure:"api_key"`
	DefaultModel string `mapstructure:"default_model"`
}

func Load() *Config {
	viper.SetConfigFile("config.yaml")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")

	// Environment variables
	viper.AutomaticEnv()
	viper.SetEnvPrefix("APP")
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

	// Defaults
	viper.SetDefault("server.port", 8080)
	viper.SetDefault("server.mode", "debug")
	viper.SetDefault("server.read_timeout", 30*time.Second)
	viper.SetDefault("server.write_timeout", 30*time.Second)

	viper.SetDefault("database.driver", "sqlite")
	viper.SetDefault("database.database", "data/app.db")

	viper.SetDefault("log.level", "info")
	viper.SetDefault("log.format", "json")

	viper.SetDefault("llm.base_url", "http://localhost:4000")
	viper.SetDefault("llm.default_model", "gpt-4o")

	// Read config file (optional)
	_ = viper.ReadInConfig()

	var cfg Config
	if err := viper.Unmarshal(&cfg); err != nil {
		panic("failed to unmarshal config: " + err.Error())
	}

	return &cfg
}
