package Fetcher

import (
	"fmt"
	"time"
)

// TODO: make table in database for logging messages

type MessageState int

const (
	Success MessageState = iota
	Failure
	Pending
)

var MessageStatus = map[string]MessageState{
	/*
		Enum for message status

		Attritbutes:
			Success: 0,
			Failure: 1,
			Pending: 2
	*/
	"Success": Success,
	"Failure": Failure,
	"Pending": Pending,
}

type Message struct {
	Id        uint64 `json:"id"`
	Sender    string `json:"sender"`
	Receiver  string `json:"receiver"`
	Status    string `json:"status"`
	Timestamp string `json:"timestamp"`
	Content   any    `json:"content"`
}

func New(options ...func(*Message)) *Message {
	/*
		Create a new instance of Message

		Arguments:
			options: This function is builder type function, provide given options to build a class

		Returns:
			Message object.
	*/

	base := Message{}
	for _, option := range options {
		option(&base)
	}
	return &base
}

func WithId(id uint64) func(*Message) {
	return func(message *Message) {
		message.Id = id
	}
}

func WithSender(sender string) func(*Message) {
	return func(message *Message) {
		message.Sender = sender
	}
}

func WithReceiver(receiver string) func(*Message) {
	return func(message *Message) {
		message.Receiver = receiver
	}
}

func WithTimestamp() func(*Message) {
	return func(message *Message) {
		message.Timestamp = fmt.Sprintf("%v", time.Now().Format("2006-01-02T15:04:05"))
	}
}

func WithContent(content any) func(*Message) {
	return func(message *Message) {
		message.Content = content
	}
}

func (self *Message) IntoResponse(content any) {
	/*
		Turn this message into response message.

		Arguments:
			content: The content of the response.

		Returns:
			Modified request message.
	*/
	// WARNING: Make sure that it can be consumed safely and there are no other
	//					references to the old request.
	self.Id = self.Id + 1
	self.Sender, self.Receiver = self.Receiver, self.Sender

	fnTimestamp := WithTimestamp()
	fnTimestamp(self)

	self.Content = content
}

func (self *Message) Validate() bool {
	// TODO: Placeholder
	return self.Sender != "" && self.Receiver != "" && self.Content != nil

}
