package logs

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/sirupsen/logrus"
	"os"
	"time"
)

var Logger = logrus.New()

func init() {
	Logger.SetOutput(os.Stdout)
	Logger.SetLevel(logrus.InfoLevel)
	Logger.SetFormatter(&CustomJSONFormatter{})
}

type CustomTextFormatter struct{}

// Format 实现 Formatter 接口的 Format 方法
func (f *CustomTextFormatter) Format(entry *logrus.Entry) ([]byte, error) {
	var b *bytes.Buffer
	if entry.Buffer != nil {
		b = entry.Buffer
	} else {
		b = &bytes.Buffer{}
	}

	// 自定义时间戳格式
	timestamp := entry.Time.Format(time.RFC3339)
	// 自定义日志级别格式
	levelColor := getLevelColor(entry.Level)
	level := fmt.Sprintf("\x1b[%dm%s\x1b[0m", levelColor, entry.Level.String())
	// 自定义日志消息格式
	msg := fmt.Sprintf("[%s] [%s] %s\n", timestamp, level, entry.Message)
	b.WriteString(msg)

	return b.Bytes(), nil
}

// getLevelColor 根据日志级别返回对应的 ANSI 颜色代码
func getLevelColor(level logrus.Level) int {
	switch level {
	case logrus.DebugLevel:
		return 36 // 青色
	case logrus.InfoLevel:
		return 32 // 绿色
	case logrus.WarnLevel:
		return 33 // 黄色
	case logrus.ErrorLevel:
		return 31 // 红色
	case logrus.FatalLevel:
		return 35 // 紫色
	case logrus.PanicLevel:
		return 31 // 红色
	default:
		return 37 // 白色
	}
}

type CustomJSONFormatter struct{}

// Format 实现 Formatter 接口的 Format 方法
func (f *CustomJSONFormatter) Format(entry *logrus.Entry) ([]byte, error) {
	data := make(logrus.Fields, len(entry.Data)+3)
	for k, v := range entry.Data {
		data[k] = v
	}
	// 自定义时间戳格式
	timestamp := entry.Time.Format("2006-01-02 15:04:05.000")
	data["timestamp"] = timestamp
	data["level"] = entry.Level.String()

	marshal, err := json.Marshal(entry.Message)
	if err != nil {
		fmt.Errorf("转换json出错 %v", err)
		return nil, err
	}
	data["message"] = string(marshal)

	// 编码为 JSON 格式
	serialized, err := json.Marshal(data)
	if err != nil {
		return nil, fmt.Errorf("Failed to marshal fields to JSON, %v", err)
	}
	return append(serialized, '\n'), nil
}
