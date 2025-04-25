package route

import (
	"github.com/labstack/echo/v4"
	"kyt-go/controllers"
)

func RegisterRoutes(e *echo.Echo) {
	e.POST("mpc-kyt/aml/transfer/register", controllers.TransferRegister())
	e.GET("mpc-kyt/aml/result", controllers.GetResult())
	e.POST("mpc-kyt/aml/address/register", controllers.AddressRegister())
}
