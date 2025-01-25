package main

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/websocket"
	"time"
)

type Message struct {
	Action string        `json:"action"`
	Params MessageParams `json:"params"`
	Echo   string        `json:"echo"`
}

type NoticeMessage struct {
	Action string       `json:"action"`
	Params NoticeParams `json:"params"`
	Echo   string       `json:"echo"`
}

type MessageParams struct {
	GroupId int    `json:"group_id"`
	Message string `json:"message"`
}

type NoticeParams struct {
	GroupId int    `json:"group_id"`
	Content string `json:"message"`
}

func connect(WebSocketURL string) (*websocket.Conn, error) {

	// 连接到 QQ 机器人的 WebSocket 服务器
	ws, _, err := websocket.DefaultDialer.Dial(WebSocketURL, nil) // 替换为实际 QQ 机器人的 WebSocket 地址
	if err != nil {
		fmt.Println("Dial Error:", err)
		return nil, err
	}
	return ws, nil
}
func sendMessage(ws *websocket.Conn, groupID int, body string) error {
	msg := Message{
		Action: "send_group_msg",
		Params: MessageParams{
			GroupId: groupID,
			Message: body,
		},
		Echo: "send_msg",
	}

	jsonData, err := json.Marshal(msg)

	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return err
	}

	// 发送请求
	if err := ws.WriteMessage(websocket.TextMessage, jsonData); err != nil {
		fmt.Println("Error setting essence message:", err)
		return err
	}

	fmt.Println("send successfully!")
	// 保持连接 1 秒
	time.Sleep(1 * time.Second)

	return nil
}

func setGroupNotice(ws *websocket.Conn, groupID int, body string) error {
	msg := NoticeMessage{
		Action: "_send_group_notice",
		Params: NoticeParams{
			GroupId: groupID,
			Content: body,
		},
		Echo: "send_notice",
	}

	jsonData, err := json.Marshal(msg)

	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return err
	}

	// 发送请求
	if err := ws.WriteMessage(websocket.TextMessage, jsonData); err != nil {
		fmt.Println("Error setting essence message:", err)
		return err
	}

	fmt.Println("Essence set successfully!")

	// 保持连接 1 秒
	time.Sleep(1 * time.Second)

	return nil
}

func main() {
	// 连接 napcat
	// 把一条要发送的消息包装成napcat可以接收的格式
	// 消息发送给napcat
	// napcat接收这个消息然后发送到群里面
	groupID := 2166024261
	body := "hello, world"
	wsUrl := "ws://localhost:3001/"
	// http://
	ws, err := connect(wsUrl)
	defer ws.Close()
	if err != nil {
		fmt.Printf("connet failed : %v", err)
	}
	if err := sendMessage(ws, groupID, body); err != nil {
		fmt.Printf("send message failed : %v", err)
	}
	if err := setGroupNotice(ws, groupID, body); err != nil {
		fmt.Printf("set group notice failed : %v", err)
	}
}
