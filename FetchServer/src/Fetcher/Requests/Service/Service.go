package Service

import (
	"fmt"
	"net/http"
	"strings"

	"google.golang.org/api/googleapi"
	"google.golang.org/api/googleapi/transport"
	"google.golang.org/api/youtube/v3"
)

type Service struct {
	Client     *youtube.Service
	MaxResults int64
}

type Video struct {
	Id          string `json:"id"`
	ChannelId   string `json:"channelid"`
	PublishedAt string `json:"published"`
	Title       string `json:"title"`
	Views       uint64 `json:"views"`
	Description string `json:"description"`
	Likes       uint64 `json:"likes"`
	Dislikes    uint64 `json:"dislikes"`
	Thumbnail   string `json:"thumbnail"`
}

type GameForm struct {
	Request string `json:"request"`
	Token   string `json:"token"`
}

func New(apiKey string) Service {
	/*
		Build the YouTube service client.

		Arguments:
			apiKey: API Key used for connections to YouTube servers.

		Returns:
			YouTube service client.
	*/

	client := &http.Client{
		Transport: &transport.APIKey{Key: apiKey},
	}

	service, err := youtube.New(client)
	if err != nil {
		panic(fmt.Sprintf("YouTube service couldn't be built: %v", err))
	}

	return Service{
		Client:     service,
		MaxResults: 10,
	}
}

func (self *Service) FetchVideosId(query *string) ([]string, error) {
	// Make the API call to YouTube.
	call := self.Client.Search.List([]string{"id"}).
		Q(*query).
		MaxResults(self.MaxResults)

	resp, err := call.Do()
	if err != nil {
		return nil, err
	}

	if resp.Items == nil {
		return nil, nil
	}

	ids := []string{}

	for _, vid := range resp.Items {
		if vid.Id.VideoId == "" {
			continue
		}
		ids = append(ids, vid.Id.VideoId)
	}

	return ids, nil
}

func (self *Service) FetchVideos(ids []string) ([]*Video, error) {
	// TODO: add validation later
	query := self.Client.Videos.List([]string{"id", "snippet", "statistics"})
	videos_info, err := query.Do(
		googleapi.QueryParameter("id", ids...),
	)

	if err != nil {
		return nil, err
	}

	videos := []*Video{}
	for _, video := range videos_info.Items {
		snippet := video.Snippet
		stats := video.Statistics
		videos = append(videos, &Video{
			Id:          video.Id,
			ChannelId:   snippet.ChannelId,
			PublishedAt: strings.Trim(snippet.PublishedAt, "Z"),
			Title:       snippet.Title,
			Views:       stats.ViewCount,
			Description: snippet.Description,
			Likes:       stats.LikeCount,
			Dislikes:    stats.DislikeCount,
			Thumbnail:   snippet.Thumbnails.Default.Url,
		})
	}
	return videos, nil
}

func (self *Service) Search(query string) ([]*Video, error) {
	// TODO: Verify token here or earlier
	content, err := self.FetchVideosId(&query)

	if err != nil {
		return nil, err
	}

	if content == nil {
		return nil, nil
	}

	resp, err := self.FetchVideos(content)

	if err != nil {
		return nil, err
	}

	return resp, nil
}
