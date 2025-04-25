package models

type TransferAmlReqDto struct {
	BusinessId    string `json:"businessId"`
	Chain         string `json:"chain"`
	Asset         string `json:"asset"`
	TxHash        string `json:"txHash"`
	OutputAddress string `json:"outputAddress"`
	Amount        string `json:"amount"`
}
