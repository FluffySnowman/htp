package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
    fmt.Println("starting backend...")

	router := http.NewServeMux()
	router.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("processing htp request...")
		fmt.Printf("--- request data ---\nHost:%s\nUser agent:%s\n", r.Host, r.UserAgent())
		w.Write([]byte("htp yeet"))
	})

	// shit to print request body and header
	router.HandleFunc("POST /", DoSomeShitWithRequestBody)
	// test whether the login token gets saved
	router.HandleFunc("POST /login", DoLoginShit)
	// test json response field filter
	router.HandleFunc("POST /jsonshit", DoJsonResponse)
	// test whether the auth header is sent with the get requests
	router.HandleFunc("GET /doshit", DoGetShit)

	http.ListenAndServe(":8888", router)
}

type BodyShit struct {
	Username    string `json:"username"`
	UserID      string `json:"user_id"`
	FileNumber  string `json:"file_number"`
	Title       string `json:"title"`
	Description string `json:"description"`
}

type LoginShit struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func DoSomeShitWithRequestBody(w http.ResponseWriter, req *http.Request) {

	// print req header to test if this shit works
	fmt.Println("user auth token -> ", req.Header.Get("Authorization"))

	decoder := json.NewDecoder(req.Body)
	var requestBodyShit BodyShit
	err := decoder.Decode(&requestBodyShit)
	if err != nil {
		fmt.Printf("\033[31m[ ERROR ] \033[97;40m%v\033[0m\n", err)
		w.Write([]byte("something went wrong"))
		return
	}

	fmt.Printf("------\nrequest body shit -> \n%s\n%s\n%s\n%s\n%s\n------",
		requestBodyShit.Username, requestBodyShit.UserID,
		requestBodyShit.FileNumber, requestBodyShit.Title,
		requestBodyShit.Description,
	)

	fmt.Println(requestBodyShit.Description)
	w.Write([]byte(requestBodyShit.Username))

}

func DoLoginShit(w http.ResponseWriter, req *http.Request) {

	decoder := json.NewDecoder(req.Body)
	var requestBodyShit LoginShit
	err := decoder.Decode(&requestBodyShit)
	if err != nil {
		fmt.Printf("\033[31m[ ERROR ] \033[97;40m%v\033[0m\n", err)
		w.Write([]byte("something went wrong"))
		return
	}

	w.Header().Add("Authorization", "thisisanauthtoken")

	w.Write([]byte(requestBodyShit.Username))

}

func DoGetShit(w http.ResponseWriter, req *http.Request) {

	fmt.Println("user auth token -> ", req.Header.Get("Authorization"))
	w.Write([]byte(fmt.Sprintf("auth token sent -> %v", req.Header.Get("Authorization"))))

}

func DoJsonResponse(w http.ResponseWriter, req *http.Request) {

	fmt.Println("[ BACKEND ] DoJsonResponse is doing the json response")

	jsonData := map[string]interface{}{
		"username": "fluffy",
		"password": "totallysecurepassword",
		"user_id":  42069,
	}

	err := json.NewEncoder(w).Encode(jsonData)

	if err != nil {
		fmt.Printf("\033[31m[ ERROR ] \033[97;40m%v\033[0m\n", err)
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("shit failed"))
	}

}
