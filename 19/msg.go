package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
	"sync"
)

// Rule contains one or more rulesets
type Rule struct {
	ruleSets []*RuleSet
}

// NewRule create new RuleSet
func NewRule() *Rule {
	ruleSets := make([]*RuleSet, 0, 2)
	return &Rule{ruleSets}
}

// RuleSet contains set of rules
type RuleSet struct {
	rules []string
}

// NewRuleSet create new RuleSet
func NewRuleSet(rules []string) *RuleSet {
	return &RuleSet{rules}
}

// AddRuleSet add RuleSet to Rule
func (rule *Rule) AddRuleSet(ruleSet *RuleSet) {
	rule.ruleSets = append(rule.ruleSets, ruleSet)
}

var rules map[string]*Rule
var msgs []string
var cache sync.Map

func main() {
	rules = make(map[string]*Rule)
	lines := readFile(os.Args)
	parse(lines)

	fmt.Printf("Messages: %d\n", len(msgs))
	fmt.Printf("Part 1: %d\n", countMatches())

	rules["8"].AddRuleSet(NewRuleSet([]string{"42", "8"}))
	rules["11"].AddRuleSet(NewRuleSet([]string{"42", "11", "31"}))

	cache = sync.Map{}
	fmt.Printf("Part 2: %d\n", countMatches())
}

func countMatches() int {
	cnt := 0
	c := make(chan map[string]bool, len(msgs))
	// c := make(chan map[string]bool, 16)

	// run
	for _, msg := range msgs {
		go consume(msg, "0", c)
	}

	// collect
	for range msgs {
		rests := <-c
		for rest := range rests {
			if len(rest) == 0 {
				cnt++
			}
		}
	}
	return cnt
}

func consume(msg string, n string, c chan map[string]bool) {
	if matches, ok := cache.Load(n + msg); ok {
		c <- matches.(map[string]bool)
		return
	}

	matches := make(map[string]bool)

	// msg is consumed but rules left
	if len(msg) == 0 {
		c <- matches
		return
	}

	// check tail
	s := rules[n].ruleSets[0].rules[0]
	if s == "a" || s == "b" {
		if s == msg[0:1] {
			matches[msg[1:]] = true
			c <- matches
			return
		}
		c <- matches
		return

	}

	for _, ruleSet := range rules[n].ruleSets {
		rests := matchRuleSet(ruleSet, msg)
		for rest := range rests {
			matches[rest] = true
		}
	}

	cache.Store(n+msg, matches)
	c <- matches
}

func matchRuleSet(ruleSet *RuleSet, line string) map[string]bool {
	matches := make(map[string]bool)
	matches[line] = true

	for _, n := range ruleSet.rules {
		c := make(chan map[string]bool, len(matches))
		subMatches := map[string]bool{}

		// run
		for m := range matches {
			go consume(m, n, c)
		}
		// collect
		for range matches {
			rests := <-c
			for rest := range rests {
				subMatches[rest] = true
			}
		}

		matches = subMatches
		if len(matches) == 0 {
			return matches
		}
	}
	return matches
}

func parse(lines []string) {
	head := true
	for _, line := range lines {
		if line == "" {
			head = false
			continue
		}
		if head {
			rule := NewRule()
			lparts := strings.Split(line, ": ")
			rparts := strings.Split((lparts[1]), " | ")
			for _, rpart := range rparts {
				rpart = strings.Trim(rpart, " ")
				rpart = strings.Trim(rpart, "\"")
				ruleSet := NewRuleSet(strings.Split(rpart, " "))
				rule.AddRuleSet(ruleSet)
			}
			rules[lparts[0]] = rule
		} else {
			msgs = append(msgs, line)
		}
	}
}

func readFile(args []string) []string {
	if len(args) < 2 {
		log.Fatal("Specify input file")
	}

	var lines []string
	file, err := os.Open(args[1])
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return lines
}
