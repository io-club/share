package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	r := gin.Default()

	r.POST("/webhook", getjson)

	r.Run()
}

func getjson(c *gin.Context) {
	var payload map[string]interface{}
	if err := c.ShouldBindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	//fmt.Print(payload)
	// 处理 Webhook 数据（如提取 Issue 信息）// payload["key"]
	action, _ := payload["action"].(string)
	issue, _ := payload["issue"].(map[string]interface{})
	title, _ := issue["title"].(string)
	user, _ := issue["user"].(map[string]interface{})
	username, _ := user["login"].(string)
	body, _ := issue["body"].(string)
	url, _ := issue["html_url"].(string)
	fmt.Printf("action: %s, title: %s, username: %s, body: %s, url: %s\n", action, title, username, body, url)
}
