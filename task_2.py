from typing import List, Dict
from dataclasses import dataclass

# Очищаємо консоль перед запуском
print('\033c', end='')

# Кольори
RESET  = '\033[0m'
BOLD   = '\033[1m'
DIM    = '\033[2m'
UN_BD  = '\033[22m'
ITALIC = '\033[3m'
TITLE0 = '\033[1;104m'
TITLE1 = '\033[1;48;2;64;40;8;38;2;220;220;220m'
TITLE2 = '\033[1;48;2;8;40;64;38;2;220;220;220m'
TITLE3 = '\033[1;48;2;8;56;32;38;2;220;220;220m'

@dataclass
class PrintJob:
    id         : str
    volume     : float
    priority   : int
    print_time : int

@dataclass
class PrinterConstraints:
    max_volume : float
    max_items  : int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    '''
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    '''
    # Застосована конвертацію вхідних словників у `dataclass` об'єкти
    # (перевірка правильності вхідних даних опущена для простоти)
    job_objects: List[PrintJob] = [PrintJob(**job) for job in print_jobs]
    
    # Об'єкт з обмеженнями (умовна спацифікація принтера)
    constraint_obj = PrinterConstraints(**constraints)

    # (1) Сортування за пріоритетом в першу чергу (1 - найвищий, 3 - найнижчий)
    # Також сортуємо за id (для стабільності)
    job_objects.sort(key=lambda job: (job.priority, job.id))

    # Список включає списки, які представляють групи друку
    print_order: List[List[str]] = []
    total_time: float = 0
    current_job_index: int = 0
    N: int = len(job_objects) # Загальна кількість завдань

    # (2) Ітеративне формування груп завдань для друку
    while current_job_index < N:
        current_group: List[PrintJob] = []
        current_volume: float = 0
        current_max_time: float = 0

        # Створюємо завдання для друку (групу)
        current_job: PrintJob = job_objects[current_job_index]

        # Перевірка завдання на відповідність обмеженням
        if (current_job.volume > constraint_obj.max_volume or constraint_obj.max_items < 1):
            current_group.append(current_job)
            current_volume = current_job.volume
            current_max_time = current_job.print_time
            current_job_index += 1
        else:
            # Намагаємося зібрати максимальну групу, починаючи з поточного завдання
            for i in range(current_job_index, N):
                next_job: PrintJob = job_objects[i]
                
                # Перевіряємо обмеження перед додаванням (групування)
                if (current_volume + next_job.volume <= constraint_obj.max_volume and 
                    len(current_group) + 1 <= constraint_obj.max_items):
                    
                    current_group.append(next_job)
                    current_volume += next_job.volume
                    
                    # Оновлюємо час друку для групи (максимальний показник у групі)
                    current_max_time = max(current_max_time, next_job.print_time)
                else:
                    # Виняток для ситуації, коли навіть одне завдання не може бути додане
                    break
            
            # Індекс для наступної групи (залежить від кількості доданих завдань)
            current_job_index += len(current_group)

        # Якщо групу сформовано, додаємо її до порядку друку
        if current_group:
            group_ids: List[str] = [job.id for job in current_group]
            print_order.append(group_ids)
            total_time += current_max_time

    return {
        'print_order' : print_order,
        'total_time'  : total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {'id' : 'M1', 'volume' : 100, 'priority' : 1, 'print_time' : 120},
        {'id' : 'M2', 'volume' : 150, 'priority' : 1, 'print_time' :  90},
        {'id' : 'M3', 'volume' : 120, 'priority' : 1, 'print_time' : 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {'id' : 'M1', 'volume' : 100, 'priority' : 2, 'print_time' : 120},  # лабораторна
        {'id' : 'M2', 'volume' : 150, 'priority' : 1, 'print_time' :  90},  # дипломна
        {'id' : 'M3', 'volume' : 120, 'priority' : 3, 'print_time' : 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {'id' : 'M1', 'volume' : 250, 'priority' : 1, 'print_time' : 180},
        {'id' : 'M2', 'volume' : 200, 'priority' : 1, 'print_time' : 150},
        {'id' : 'M3', 'volume' : 180, 'priority' : 2, 'print_time' : 120}
    ]

    constraints = {
        'max_volume' : 300,
        'max_items'  : 2
    }

    print(f'{TITLE0} --= Тестування оптимізації черги 3D-друку =-- {RESET}')
    print(f'{ITALIC+DIM} (групування списком у списку для наочності){RESET}\n')

    print(f'{TITLE1} Тест 1 {UN_BD+DIM+ITALIC}(однаковий пріоритет) {RESET}')
    result1 = optimize_printing(test1_jobs, constraints)
    print(f'\tПорядок друку: {result1["print_order"]}')
    print(f'\tЗагальний час: {result1["total_time"]} хвилин\n')

    print(f'{TITLE2} Тест 2 {UN_BD+DIM+ITALIC}(різні пріоритети) {RESET}')
    result2 = optimize_printing(test2_jobs, constraints)
    print(f'\tПорядок друку: {result2["print_order"]}')
    print(f'\tЗагальний час: {result2["total_time"]} хвилин\n')

    print(f'{TITLE3} Тест 3 {UN_BD+DIM+ITALIC}(перевищення обмежень) {RESET}')
    result3 = optimize_printing(test3_jobs, constraints)
    print(f'\tПорядок друку: {result3["print_order"]}')
    print(f'\tЗагальний час: {result3["total_time"]} хвилин\n')

if __name__ == '__main__':
    test_printing_optimization()