package main

import (
	"fmt"
	"strings"
)

// Функция для проверки, соответствует ли строка правилам первой популяции
func A(input string) (string, bool) {
	input = strings.TrimSpace(input)
	inputB, isRuleB := B(input)
	if !isRuleB {
		return "", false
	}
	return D(inputB)
}

// Функция для проверки правила 2 первой популяции
func B(input string) (string, bool) {
	input = strings.TrimSpace(input)
	inputB, isRuleB := C(input)
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

// Функция для проверки правила 2 первой популяции
func D(input string) (string, bool) {
	input = strings.TrimSpace(input)
	if strings.HasPrefix(input, "ay") {
		inputA, isRuleA := A(strings.TrimPrefix(input, "ay"))
		if !isRuleA {
			return "", true
		}

		return inputA, true
	}

	return "", true
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

	return "", true
}

// Функция для проверки, соответствует ли строка правилам второй популяции
func checkSecondPopulation(input string) bool {
	input = strings.TrimSpace(input)
	if strings.HasPrefix(input, "ой ") {
		parts := strings.SplitN(input, " ой ", 2)
		if len(parts) == 2 && strings.Contains(parts[1], " ай ") {
			innerParts := strings.SplitN(parts[1], " ай ", 2)
			return checkSecondPopulationRule2(parts[0]) && checkSecondPopulationRule3(innerParts[1])
		}
	}
	if input == "ну" || strings.HasPrefix(input, "ну ") {
		return checkSecondPopulationRule2(input)
	}
	if strings.HasPrefix(input, "хо ") {
		return checkSecondPopulationRule3(input)
	}
	return false
}

// Функция для проверки правила 2 второй популяции
func checkSecondPopulationRule2(input string) bool {
	input = strings.TrimSpace(input)
	if input == "ну" {
		return true
	}
	if strings.HasPrefix(input, "ну ") {
		return checkSecondPopulationRule2(strings.TrimPrefix(input, "ну "))
	}
	return false
}

// Функция для проверки правила 3 второй популяции
func checkSecondPopulationRule3(input string) bool {
	input = strings.TrimSpace(input)
	if input == "ух-ты" {
		return true
	}
	if strings.HasPrefix(input, "хо ") {
		return checkSecondPopulationRule3(strings.TrimPrefix(input, "хо "))
	}
	return false
}

func classifyMonkey(input string) string {
	_, isRule := A(input)
	if isRule {
		return "Первая популяция"
	} else if checkSecondPopulation(input) {
		return "Вторая популяция"
	}
	return "Неместная обезьяна"
}

func main() {
	var input string
	fmt.Println("Введите монолог обезьяны:")
	fmt.Scanln(&input)

	result := classifyMonkey(input)
	fmt.Println(result)
}
