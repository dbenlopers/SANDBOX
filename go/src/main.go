package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w, http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "This is a website server bu a go HTTP server.")
	})
	http.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello World! I'm a HTTP server!")
	})

	fs := http.FileServer(http.Dir("static/"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	http.ListenAndServe(":3001", nil)
}