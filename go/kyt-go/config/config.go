package config

import (
	"embed"
	"fmt"
	"github.com/labstack/gommon/log"
	"gopkg.in/yaml.v3"
	"os"
)

type DatabaseModule struct {
	Server   Server
	Database Database
}

type Server struct {
	Port int    `yaml:"port"`
	Host string `yaml:"host"`
}

type Database struct {
	Host     string `yaml:"host"`
	Port     int    `yaml:"port"`
	Username string `yaml:"username"`
	Password string `yaml:"password"`
}

type EnvName struct {
	EnvName string `yaml:"env_name"`
}

const (
	FILE_PATH = "resource/application_%s.yaml"
)

func LoadConfig(yamlFile embed.FS) (*DatabaseModule, error) {
	envName := os.Getenv("ENV_NAME")

	file, err := os.ReadFile(fmt.Sprintf(FILE_PATH, envName))
	if err != nil {
		log.Infof("读取文件失败：%v", err.Error())
		return nil, err
	}
	var database DatabaseModule
	err = yaml.Unmarshal(file, &database)
	if err != nil {
		fmt.Printf("解析文件失败:%v", err.Error())
		return nil, err
	}
	return &database, nil
}
