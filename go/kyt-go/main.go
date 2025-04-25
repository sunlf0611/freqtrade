package main

import (
	"embed"
	"fmt"
	"kyt-go/logs"
	"os"
)

//go:embed resource/application_*.yaml
var yamlFile embed.FS

var defaultEnvName = map[string]string{
	"prod": "prod",
	"test": "test",
	"dev":  "dev",
}

//
//func main() {
//	e := echo.New()
//	loadEnvName()
//	loadConfig, err := config.LoadConfig(yamlFile)
//	if err != nil {
//		logs.Logger.Errorf("启动出错，加载配置异常 %v\n\n", err)
//	}
//	route.RegisterRoutes(e)
//
//	var address = loadConfig.Server.Host + ":" + strconv.Itoa(loadConfig.Server.Port)
//	if err := e.Start(address); err != nil {
//		logs.Logger.Errorf("服务启动失败 %s", err)
//	}
//}

func loadEnvName() {
	envName := os.Getenv("ENV_NAME")
	if envName == "" {
		logs.Logger.Infof("读取到环境变量为空，设置默认环境变量为 dev")
		envName = defaultEnvName["dev"]
		err := os.Setenv("ENV_NAME", envName)
		if err != nil {
			logs.Logger.Errorf("设置环境变量出错，系统退出")
			os.Exit(1)
		}
	} else {
		s := defaultEnvName[envName]
		if s == "" {
			logs.Logger.Errorf("加载环境变量失败，非法的环境变量值：%s", s)
			os.Exit(1)
		}
	}

}

type People interface {
	Speak(string) string
}

type Student struct{}

func (stu Student) Speak(think string) (talk string) {
	if think == "sb" {
		talk = "你是个大帅比"
	} else {
		talk = "您好"
	}
	return talk
}

type Mover interface {
	move()
}

type dog struct{}

func (d dog) move() {
	fmt.Println("狗会动")
}
func main() {
	var x Mover
	var wangcai = dog{} // 旺财是dog类型
	x = wangcai         // x可以接收dog类型
	var fugui = &dog{}  // 富贵是*dog类型
	x = fugui           // x可以接收*dog类型
	x.move()
}
