package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()

	r.GET("/ping", func(c *gin.Context) {
		c.String(200, "hello world")
	})

	r.Run(":8002")
}
