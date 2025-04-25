package service

import (
	"kyt-go/logs"
)

// ThirdRegisterReq 定义一个接口
type ThirdRegisterReq interface {
	RegisterTo()
}

type TrustFormer struct{}

func (t TrustFormer) RegisterTo() {
	logs.Logger.Errorf("")
}

type ChainAnalysis struct{}

func (c ChainAnalysis) RegisterTo() {
	logs.Logger.Errorf("")
}
