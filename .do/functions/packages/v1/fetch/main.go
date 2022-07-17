package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/google/go-github/v45/github"
)

type Request struct {
	Name string `json:"name"`
}

type Body struct {
	Content []byte `json:"content"`
	Error   string `json:"error"`
}

type Response struct {
	StatusCode int               `json:"statusCode,omitempty"`
	Headers    map[string]string `json:"headers,omitempty"`
	Body       Body              `json:"body,omitempty"`
}

// func main() {
// 	resp, err := Main(Request{Name: "alexpovel"})
// 	if err != nil {
// 		fmt.Println(err)
// 	}
// 	b, err := json.Marshal(resp.Body.Content)
// 	fmt.Println(string(b))
// 	fmt.Println(string(resp.Body.Content))
// }

func Main(in Request) (*Response, error) {
	filename := "resume.json"

	resp := Response{
		Body: Body{
			Error: fmt.Sprintf("No file '%s' found in any gists of user %s.", filename, in.Name),
		},
	}

	client := github.NewClient(nil)
	gists, _, err := client.Gists.List(context.Background(), in.Name, nil)

	if err != nil {
		resp.Body.Error = fmt.Sprintf("GitHub API error: %s", err)
	} else {
		for _, gist := range gists {
			file, ok := gist.Files[github.GistFilename(filename)]

			if !ok {
				continue
			}

			raw_resp, err := http.Get(*file.RawURL)
			if err != nil {
				resp.Body.Error = fmt.Sprintf("Error retrieving gist: %s", err)
				break
			}

			content, err := ioutil.ReadAll(raw_resp.Body)
			if err != nil {
				resp.Body.Error = fmt.Sprintf("Error reading gist: %s", err)
				break
			}

			resp.Body.Content = content
			resp.Body.Error = ""
			break
		}
	}
	return &resp, err
}
