package service

import (
	"kyt-go/logs"
	"kyt-go/models"
	"kyt-go/utils"
)

func RegisterPre(dto *models.TransferAmlReqDto) (int64, error) {
	id, err2 := utils.GetId()
	if err2 != nil {
		return 0, err2
	}
	logs.Logger.Infof("%+v", dto)

	var trustFormer ThirdRegisterReq
	var chainanlysis ThirdRegisterReq

	trustFormer.RegisterTo()
	chainanlysis.RegisterTo()

	return id, nil
}
