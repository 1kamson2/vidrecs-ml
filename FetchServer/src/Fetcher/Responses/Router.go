package Responses

import (
	"Fetcher"
	"Service"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func New(service *Service.Service) *gin.Engine {
	router := gin.Default()

	router.GET("/api/", func(ctx *gin.Context) {
		ctx.JSON(
			http.StatusForbidden,
			gin.H{
				"content": "You haven't specified the API call.",
			})
	})

	router.GET("/api/sync", func(ctx *gin.Context) {
		ctx.JSON(
			http.StatusForbidden,
			gin.H{
				"content": "Not implemented.",
			})
	})

	router.POST("/api/search", func(ctx *gin.Context) {
		/*
			Get server request to search content on the YouTube.

			Returns:
				Videos matching the keywords in the title limited to the
				maxResults variable.
		*/
		/* WARNING: Use only if the content is not available in the database.*/

		var form Service.GameForm

		var message *Fetcher.Message = Fetcher.New(Fetcher.WithContent(&form))
		err := json.NewDecoder(ctx.Request.Body).Decode(message)
		fmt.Println(message)
		fmt.Println(form)

		if err != nil {
			message.IntoResponse(err)
			ctx.JSON(
				http.StatusBadRequest,
				message,
			)
		}

		if !message.Validate() {
			message.IntoResponse(err)
			ctx.JSON(
				http.StatusBadRequest,
				message,
			)
		}

		query := form.Request
		fmt.Println(query)

		videos, err := service.Search(query)

		if err != nil {
			message.IntoResponse(err)
			ctx.JSON(
				http.StatusForbidden,
				message,
			)
		}

		fmt.Println(videos)

		message.IntoResponse(videos)
		fmt.Println(message)
		ctx.JSON(
			http.StatusOK,
			message,
		)
	})

	// router.GET("/api/test_cats", func(ctx *gin.Context) {
	// 	content, err := service.Search("cute cats")
	//
	// 	if err != nil {
	// 		ctx.JSON(
	// 			http.StatusForbidden,
	//
	// 			gin.H{
	// 				"error": err,
	// 			})
	// 	}
	//
	// 	message := Fetcher.New(
	// 		Fetcher.WithId(1),
	// 		Fetcher.WithSender("localhost"),
	// 		Fetcher.WithReceiver(ctx.ClientIP()),
	// 		Fetcher.WithContent(content),
	// 	)
	//
	// 	ctx.JSON(
	// 		http.StatusOK,
	// 		gin.H{
	// 			"content": message,
	// 		})
	// })

	return router
}
