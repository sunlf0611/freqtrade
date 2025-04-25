package utils

import (
	"github.com/bwmarrin/snowflake"
	"kyt-go/logs"
)

var node, err = snowflake.NewNode(1)

func GetId() (int64, error) {
	if node == nil {
		logs.Logger.Errorf("Snowflake node is nil : %v", err)
		return 0, err
	}
	id := node.Generate()
	return id.Int64(), nil
}
