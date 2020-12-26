package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Specify input file")
	}

	s := readFile(os.Args[1])
	fmt.Printf("%v\n", s)

	c := map[int]bool{}

	var v1, v2, v3 int

	for _, v := range s {
		n, err := strconv.Atoi(v)
		if err != nil {
			log.Fatalf("%s is not a int", v)
		}
		c[n] = true

		if _, ok := c[2020-n]; ok {
			v1 = n
		}

		for m := range c {
			if _, ok := c[2020-n-m]; ok {
				v2 = n
				v3 = m
			}
		}
	}

	fmt.Printf("v1: %d\n", 2020-v1)
	fmt.Printf("v2: %d\n", 2020-v2-v3)
}

func readFile(fileName string) []string {
	var s []string
	file, err := os.Open("test.data")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		s = append(s, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return s
}
