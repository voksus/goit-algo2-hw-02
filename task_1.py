import random as rnd

# Очищаємо консоль перед запуском
print("\033c", end="")

# Кольори
RESET  = '\033[0m'
BOLD   = '\033[1m'
DIM    = '\033[2m'
ITALIC = '\033[3m'
GREEN  = '\033[1;38;2;0;160;40m'
ORANGE = '\033[1;38;2;180;90;0m'
TITLE1 = '\033[1;34;48;2;0;64;128m'
TITLE2 = '\033[1;48;2;8;56;32;38;2;220;220;220m'

def min_max_recursive(numbers: list, low: int, high: int) -> tuple[int, int]:
    # Базовий випадок (1 елемент)
    if low == high:
        return numbers[low], numbers[low]

    if high == low + 1:
        if numbers[low] < numbers[high]:
            return numbers[low], numbers[high]
        else:
            return numbers[high], numbers[low]

    mid = (low + high) // 2

    min_left, max_left = min_max_recursive(numbers, low, mid)

    min_right, max_right = min_max_recursive(numbers, mid + 1, high)

    # Загальний мінімум (серед лівого та правого мінімумів)
    overall_min = min_left if min_left < min_right else min_right
    
    # Загальний максимум (серед лівого та правого максимумів)
    overall_max = max_left if max_left > max_right else max_right
    
    return overall_min, overall_max

# Основна функція, що викликається (відповідає сигнатурі завдання)
def find_min_max_dc(numbers: list[int]) -> tuple[int | None, int | None]:
    if not numbers:
        return None, None
    
    # Виклик рекурсивної функції
    return min_max_recursive(numbers, 0, len(numbers) - 1)

def view_and_highlight(arr: list[int], min_val: int, max_val: int) -> str:
    highlighted = []
    for num in arr:
        if num == min_val:
            highlighted.append(f'{GREEN}{num}{RESET}')  # Зелений для min
        elif num == max_val:
            highlighted.append(f'{ORANGE}{num}{RESET}')  # Помаранчевий для max
        else:
            highlighted.append(str(num))
    return '[' + ', '.join(highlighted) + ']'

# Приклад використання
print(f'{TITLE1} --= Перевірка реалізації алгоритму =-- {RESET}')
arr = [10, 5, 11, 3, 29, 15, 26, 4]
_min, _max = find_min_max_dc(arr)
print(f'Тест 0:  {DIM+ITALIC}({_min:2}, {_max:3}){RESET}  ->  {view_and_highlight(arr, _min, _max)}\n') # Очікуваний результат: (3, 29)

# Додаткові тести на випадкових масивах
print(f'{TITLE2}  Додаткові тести : {RESET}')
for i in range(10):
    arr = [rnd.randint(0, 256) for _ in range(rnd.randint(5, 20))]
    _min, _max = find_min_max_dc(arr)
    print(f'Тест {i+1:2}:  {DIM+ITALIC}({_min:3}, {_max:3}){RESET}  ->  {view_and_highlight(arr, _min, _max)}')
print()