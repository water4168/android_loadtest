package main

import "github.com/myzhan/boomer"

import (
	"time"
	"net/http"
	"log"
	"encoding/json"
	"math/rand"
	"fmt"
	"bytes"
)


func now() int64 {
	return time.Now().UnixNano() / int64(time.Millisecond)
}


func get_random_addr() string {
	s := make([]string, 4)
	s[0] = "0xAB2DFA9682B4800f560F5ffA1561Ae6959a23c0a"
	s[1] = "0x2F289B7D632A3efe715dF9c3e69d0b8bb56265C8"
	s[2] = "0x63c095eb76771439d50a0c9a26de661c7a025568"
	s[3] = "0xa0f2627520169c91fcb18e2e57e7454b778611a3"
	return  s[rand.Intn(4)]

}

func test_ethbalance() {
	/*
	一个常规的 HTTP GET 操作，实际使用时，这里放业务自身的处理过程
	只要将处理结果，通过 boomer 暴露出来的函数汇报就行了
	请求成功，类似 Locust 的 events.request_success.fire
	boomer.Events.Publish("request_success", type, name, 处理时间, 响应耗时)
	请求失败，类似 Locust 的 events.request_failure.fire
	boomer.Events.Publish("request_failure", type, name, 处理时间, 错误信息)
	 */
	startTime := now()
	body :=map[string]string{
		"address": get_random_addr(),
	}

	bytesData, err := json.Marshal(body)
	if err != nil {
		fmt.Println(err.Error() )
		return
	}
	reader := bytes.NewReader(bytesData)

	client := &http.Client{}
	req, err := http.NewRequest("POST","http://47.254.26.164:80/api/wallet/eth_getBalance",  reader)
	if err != nil {
		fmt.Println(err.Error())
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer eyJhbGciOiJIUzUxMiJ9.eyJyYW5kb21LZXkiOiJveDc1NDUiLCJzdWIiOiIxNSIsImlhdCI6MTUyMjU3Mzg5Mn0.hPwsslcNvRbqsYIGGW68wv1_Q5U1UR7nHEhpK1z5x2MAN-Yre0xREbKPnCBAG2iKF2Ev0jcfl41fAb_rptkzcA")
	req.Header.Set("User-Agent", "Project/1.0 (m-chain-001; build:1; iOS 10.2.1) Alamofire/4.7.0")

	resp, err := client.Do(req)
	defer resp.Body.Close()

	endTime := now()
	log.Println(float64(endTime - startTime))
	if err != nil {
		boomer.Events.Publish("request_failure", "demo", "http", 0.0, err.Error())
	}else {
		boomer.Events.Publish("request_success", "demo", "http", float64(endTime - startTime), resp.ContentLength)
	}
}


func main() {

	task := &boomer.Task{
		// Weight 权重，和 Locust 的 task 权重类似，在有多个 task 的时候生效
		// FIXED: 之前误写为Weith
		Weight: 10,
		// Fn 类似于 Locust 的 task
		Fn: test_ethbalance,
	}

	/*
	通知 boomer 去执行自定义函数，支持多个
	boomer.Run(task1, task2, task3)
	*/

	boomer.Run(task)

}

//https://www.cnblogs.com/hitfire/articles/6427033.html