package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func S(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if strings.HasPrefix(input, "start") {
		inputA, isRuleA := A(strings.TrimPrefix(input, "start"))

		if isRuleA {
			if strings.HasPrefix(inputA, "stop") {
				return strings.TrimSpace(strings.TrimPrefix(input, "stop")), true
			}
		}
	}

	return "", false
}

func A(input string) (string, bool) {
	input = strings.TrimSpace(input)

	inputC, isRuleC := C(input)
	if isRuleC {
		inputZ, isRuleZ := Z(inputC)
		if isRuleZ {
			inputY, isRuleY := Y(inputZ)
			if isRuleY {
				return strings.TrimSpace(inputY), true
			}
		}
	}

	return "", false
}

func C(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if strings.HasPrefix(input, "left") {
		return strings.TrimSpace(strings.TrimPrefix(input, "left")), true
	}

	if strings.HasPrefix(input, "right") {
		return strings.TrimSpace(strings.TrimPrefix(input, "right")), true
	}

	if strings.HasPrefix(input, "on45") {
		return C(strings.TrimPrefix(input, "on45"))
	}

	if strings.HasPrefix(input, "hands_up") {
		inputA, isRuleA := A(strings.TrimPrefix(input, "hands_up"))

		if isRuleA {
			if strings.HasPrefix(inputA, "hands_down") {
				return strings.TrimSpace(strings.TrimPrefix(inputA, "hands_down")), true
			}
		}
	}

	return "", false
}

func Z(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if strings.HasPrefix(input, "turn_head") {
		inputC, isRuleC := C(strings.TrimPrefix(input, "turn_head"))
		if isRuleC {
			return strings.TrimSpace(inputC), true
		}
	}

	return input, true
}

func Y(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if strings.HasPrefix(input, "step_(") {
		input = strings.TrimPrefix(input, "step_(")

		inputF, isRuleF := F(input)
		if isRuleF {
			input = strings.TrimPrefix(inputF, ")")
			input = strings.TrimSpace(input)

			inputY, isRuleY := Y(input)
			if isRuleY {
				inputC, isRuleC := C(strings.TrimSpace(inputY))

				if isRuleC {
					return Y(inputC)
				}
			}

			return "", false
		}
	}

	return input, true
}

func F(input string) (string, bool) {
	input = strings.TrimSpace(input)

	if input[0] >= '0' && input[0] <= '9' {
		input = input[1:]

		return X(input)
	}

	return "", false
}

func X(input string) (string, bool) {
	input = strings.TrimSpace(input)

	inputF, isRuleF := F(input)
	if isRuleF {
		return strings.TrimSpace(inputF), true
	}

	return input, true
}

func classifyRobot(input string) string {
	input = strings.ToLower(input)

	_, isRule := S(input)
	if isRule {
		return "OK"
	}
	return "ERROR"
}

func main() {
	fmt.Println("Введите команды:")

	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\n')

	result := classifyRobot(input)
	fmt.Println(result)
}
