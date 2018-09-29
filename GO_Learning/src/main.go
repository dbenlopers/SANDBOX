package main

import (
	"bufio"
	"fmt"
	"net/http"

	// "net/http"
	"os"
)

func httpserver() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("Req: %s %s\n", r.Host, r.URL.Path)
		fmt.Fprint(w, "This is a website server bu a go HTTP server.")
	})
	http.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("Req: %s %s\n", r.Host, r.URL.Path)
		fmt.Fprintf(w, "Hello World! I'm a HTTP server!")
	})

	fs := http.FileServer(http.Dir("static/"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	http.ListenAndServe(":3001", nil)
}

func countLines(f *os.File, counts map[string]int) {
	input := bufio.NewScanner(f)
	for input.Scan() {
		counts[input.Text()]++
	}
}

func incrPtr(p *int) int {
	*p++ // increment what p points to; does not change p
	return *p
}

func main() {
	//httpserver()
	/* for i, arg := range os.Args[1:] {
		fmt.Println(i, arg)
	}
	fmt.Println(strings.Join(os.Args[1:], " "))
	fmt.Println(os.Args[0:]) */

	// Dup
	/* counts := make(map[string]int)
	files := os.Args[1:]
	if len(files) == 0 {
		countLines(os.Stdin, counts)
	} else {
		for _, arg := range files {
			f, err := os.Open(arg)
			if err != nil {
				fmt.Fprintf(os.Stderr, "dup: %s \n", err)
				continue
			}
			countLines(f, counts)
			f.Close()
		}
	}
	for line, n := range counts {
		if n > 1 {
			fmt.Printf("%d\t%s\n", n, line)
		}
	} */
	/* counts := make(map[string]int)
	for _, filename := range os.Args[1:] {
		data, err := ioutil.ReadFile(filename)
		if err != nil {
			fmt.Fprintf(os.Stderr, "dup: %v\n", err)
			continue
		}
		for _, line := range strings.Split(string(data), "\n") {
			counts[line]++
		}
	}
	for line, n := range counts {
		if n > 1 {
			fmt.Printf("%d\t%s\n", n, line)
		}
	} */
	x := 1
	p := &x
	fmt.Println(*p) // 1
	fmt.Println(x)  // 1
	*p = 2
	fmt.Println(x) // 2
	fmt.Println(p) // adrss

	v := 1
	incrPtr(&v)
	fmt.Println(v)
	fmt.Println(incrPtr(&v))
}
