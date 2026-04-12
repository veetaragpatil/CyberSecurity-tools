package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"
)


type Tool struct {
	Name        string
	Description string
	Command     string
	Args        []string
}

// Available tools in our CLI


func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	toolName := os.Args[1]
	tool, exists := tools[toolName]
	if !exists {
		fmt.Printf("Error: Tool '%s' not found\n", toolName)
		printUsage()
		os.Exit(1)
	}

	// Pass additional arguments to the tool
	if len(os.Args) > 2 {
		tool.Args = append(tool.Args, os.Args[2:]...)
	}

	fmt.Printf("Running %s...\n", tool.Name)
	fmt.Printf("Command: %s %s\n\n", tool.Command, strings.Join(tool.Args, " "))

	output, err := runTool(tool)
	if err != nil {
		log.Fatalf("Error running %s: %v", tool.Name, err)
	}

	fmt.Println("Output:")
	fmt.Println(output)
}

// runTool executes the specified tool and returns its output
func runTool(tool Tool) (string, error) {
	cmd := exec.Command(tool.Command, tool.Args...)
	
	// Capture both stdout and stderr
	output, err := cmd.CombinedOutput()
	if err != nil {
		return string(output), fmt.Errorf("command failed: %w", err)
	}
	
	return string(output), nil
}

// printUsage displays available commands and usage information
func printUsage() {
	fmt.Println("Security Tools CLI")
	fmt.Println("==================")
	fmt.Println("\nUsage:")
	fmt.Println("  ./security-cli <tool> [options]")
	fmt.Println("\nAvailable tools:")
	for name, tool := range tools {
		fmt.Printf("  %-12s %s\n", name, tool.Description)
	}
	fmt.Println("\nExamples:")
	fmt.Println("  ./security-cli subfinder -d example.com")
	fmt.Println("  ./security-cli nmap -sV -p 80,443 example.com")
}
