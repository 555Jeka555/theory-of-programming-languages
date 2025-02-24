package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func A(input string) (string, bool) {
	input = strings.TrimSpace(input)
	inputB, isRuleB := B(input)
	inputB = strings.TrimSpace(inputB)

	if !isRuleB {
		return "", false
	}

	return D(inputB)
}

func B(input string) (string, bool) {
	input = strings.TrimSpace(input)
	inputB, isRuleB := C(input)
	inputB = strings.TrimSpace(inputB)

	if !isRuleB {
		return "", false
	}
	return E(inputB)
}

func C(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if strings.HasPrefix(input, "ух-ты") {
		return strings.TrimPrefix(input, "ух-ты"), true
	}

	if strings.HasPrefix(input, "хо") {
		return C(strings.TrimPrefix(input, "хо"))
	}

	if strings.HasPrefix(input, "ну") {
		inputA, isRuleA := A(strings.TrimPrefix(input, "ну"))
		inputA = strings.TrimSpace(inputA)

		if isRuleA {
			if strings.HasPrefix(inputA, "и ну") {
				return strings.TrimPrefix(inputA, "и ну"), true
			}
		}
	}

	return "", false
}

func D(input string) (string, bool) {
	input = strings.TrimSpace(input)
	if strings.HasPrefix(input, "ау") {
		inputA, isRuleA := A(strings.TrimPrefix(input, "ау"))
		if !isRuleA {
			return "", true
		}

		return inputA, true
	}

	return input, true
}

func E(input string) (string, bool) {
	input = strings.TrimSpace(input)
	if strings.HasPrefix(input, "ку") {
		inputB, isRuleB := B(strings.TrimPrefix(input, "ку"))
		if !isRuleB {
			return "", true
		}

		return inputB, true
	}

	return input, true
}

func A2(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if strings.HasPrefix(input, "ой") {
		inputB2, isRuleB2 := B2(strings.TrimPrefix(input, "ой"))
		inputB2 = strings.TrimSpace(inputB2)

		if isRuleB2 {
			if strings.HasPrefix(inputB2, "ай") {
				return C2(strings.TrimPrefix(inputB2, "ай"))
			}
		}
	}

	return "", false
}

func B2(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if strings.HasPrefix(input, "ну") {
		inputB2, isRule2 := B2(strings.TrimPrefix(input, "ну"))
		inputB2 = strings.TrimSpace(inputB2)

		if !isRule2 {
			return strings.TrimPrefix(input, "ну"), true
		}
		return inputB2, true
	}

	return "", false
}

func C2(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if strings.HasPrefix(input, "хо") {
		inputC2, isRuleC2 := C2(strings.TrimPrefix(input, "хо"))
		inputC2 = strings.TrimSpace(inputC2)

		if isRuleC2 {
			if strings.HasPrefix(input, "хо") {
				return strings.TrimPrefix(inputC2, "хо"), true
			}
		}
	}

	if strings.HasPrefix(input, "ух-ты") {
		return strings.TrimPrefix(input, "ух-ты"), true
	}

	return "", false
}

func classifyMonkey(input string) string {
	input = strings.ToLower(input)

	in, isRule := A(input)
	if isRule && in == "" {
		return "Первая популяция"
	}

	in, isRule2 := A2(input)
	if isRule2 && in == "" {
		return "Вторая популяция"
	}
	return "Неместная обезьяна"
}

func main() {
	fmt.Println("Введите монолог обезьяны:")

	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\n')

	result := classifyMonkey(input)
	fmt.Println(result)
}
