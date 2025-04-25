package controllers

import (
	"github.com/labstack/echo/v4"
	"kyt-go/logs"
	"kyt-go/models"
	"kyt-go/service"
	"net/http"
)

func TransferRegister() echo.HandlerFunc {
	return func(c echo.Context) error {
		var transfer models.TransferAmlReqDto
		if err := c.Bind(&transfer); err != nil {
			return c.JSON(http.StatusUnprocessableEntity, err.Error())
		}
		logs.Logger.Infof("param ：%+v", &transfer)
		register, err := service.RegisterPre(&transfer)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, err.Error())
		}
		return c.JSON(http.StatusOK, register)
	}
}

func GetResult() echo.HandlerFunc {
	return nil
}

func AddressRegister() echo.HandlerFunc {
	return nil
}
