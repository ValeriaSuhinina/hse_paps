# Лабораторная работа №6
**Тема:**  Использование шаблонов проектирования
 
**Цель работы:** Получить опыт применения шаблонов проектирования при написании кода программной системы

## Порождающие шаблоны
### Фабричный метод (Factory Method):
**Описание:** Позволяет создавать объекты без указания конкретных классов создаваемых объектов.

**Применение для системы строительного контроля:** Можно использовать для создания экземпляров различных типов нарушений, не привязываясь к конкретным классам.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/bc715fa3-b802-47fd-bd8d-e89287ead485)

**Конечный код:**
```python
from abc import ABC, abstractmethod

class ViolationFactory(ABC):
    @abstractmethod
    def create_violation(self):
        pass

class SafetyViolationFactory(ViolationFactory):
    def create_violation(self):
        return SafetyViolation()

class AnotherViolationFactory(ViolationFactory):
    def create_violation(self):
        return AnotherViolation()

class Violation(ABC):
    pass

class SafetyViolation(Violation):
    pass

class AnotherViolation(Violation):
    pass
````

### Абстрактная фабрика (Abstract Factory):
**Описание:** Позволяет создавать семейства связанных объектов без указания их конкретных классов.

**Применение для системы строительного контроля:** Можно использовать для создания экземпляров различных типов нарушений, не привязываясь к конкретным классам.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/f8b2fe3c-3621-43b1-96d5-5176b33c3562)

**Конечный код:**
```python
from abc import ABC, abstractmethod

# Абстрактные классы
class Violation(ABC):
    def __init__(self, description):
        self.description = description

class SafetyViolation(Violation):
    pass

class AnotherViolation(Violation):
    pass

class ViolationClassifier(ABC):
    @abstractmethod
    def classifyViolation(self, violation: Violation) -> str:
        pass

class SafetyClassifier(ViolationClassifier):
    def classifyViolation(self, violation: Violation) -> str:
        if isinstance(violation, SafetyViolation):
            return "Safety Violation Classified"
        else:
            return "Unknown Violation"

class AnotherViolationClassifier(ViolationClassifier):
    def classifyViolation(self, violation: Violation) -> str:
        if isinstance(violation, AnotherViolation):
            return "Another Violation Classified"
        else:
            return "Unknown Violation"

# Фабрики
class ViolationFactory(ABC):
    @abstractmethod
    def createViolation(self) -> Violation:
        pass

    @abstractmethod
    def createViolationClassifier(self) -> ViolationClassifier:
        pass

class SimpleViolationFactory(ViolationFactory):
    def createViolation(self) -> Violation:
        return SafetyViolation("Simple Safety Violation")

    def createViolationClassifier(self) -> ViolationClassifier:
        return SafetyClassifier()

class FancyViolationFactory(ViolationFactory):
    def createViolation(self) -> Violation:
        return AnotherViolation("Fancy Another Violation")

    def createViolationClassifier(self) -> ViolationClassifier:
        return AnotherViolationClassifier()

# Пример использования
simple_factory = SimpleViolationFactory()
violation = simple_factory.createViolation()
classifier = simple_factory.createViolationClassifier()
print(violation.description)
print(classifier.classifyViolation(violation))

fancy_factory = FancyViolationFactory()
violation = fancy_factory.createViolation()
classifier = fancy_factory.createViolationClassifier()
print(violation.description)
print(classifier.classifyViolation(violation))
```
### Одиночка (Singleton):
**Описание:** Гарантирует, что у класса есть только один экземпляр, и предоставляет глобальную точку доступа к этому экземпляру.

**Применение для системы строительного контроля:** Можно использовать для создания единственного экземпляра сервиса управления нарушениями, чтобы все части системы имели доступ к единому источнику данных о нарушениях.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/8b44b89f-1ae9-44d5-896f-375e2348e097)

**Конечный код:**
```python
class ViolationServiceSingleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.violations = []

    def add_violation(self, violation):
        self.violations.append(violation)

    def get_all_violations(self):
        return self.violations
```
## Структурные шаблоны
### Шаблон "Адаптер" (Adapter):
**Описание:** Шаблон "Адаптер" используется для преобразования интерфейса одного класса в интерфейс другого, ожидаемого клиентом.

**Применение для системы строительного контроля:** Можно  применить шаблон "Адаптер", чтобы адаптировать различные источники данных о нарушениях или подрядчиках к общему интерфейсу, который использует система строительного контроля.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/f67ce54f-9761-4334-b637-a36fce775e13)

**Конечный код:**
```python
// Класс для взаимодействия с внешним сервисом контроля нарушений
class ExternalViolationControlService {
    func fetchViolations() -> [[String: Any]] {
        // Симуляция получения информации о нарушениях от внешнего сервиса
        return [
            ["description": "Нарушение 1", "date": "01/01/2023"],
            ["description": "Нарушение 2", "date": "02/01/2023"],
            ["description": "Нарушение 3", "date": "03/01/2023"]
        ]
    }
}

// Поставщик внешнего сервиса контроля нарушений
class ExternalViolationControlServiceProvider {
    func getExternalViolationControlService() -> ExternalViolationControlService {
        return ExternalViolationControlService()
    }
}

// Абстрактный класс для представления нарушения
class Violation {
    func processViolation() {
        // Базовая реализация обработки нарушения
    }
}

// Адаптер нарушения, приспосабливающий внешний сервис контроля нарушений
class ViolationAdapter: Violation {
    let externalService: ExternalViolationControlService

    init(externalService: ExternalViolationControlService) {
        self.externalService = externalService
    }

    override func processViolation() {
        let violations = externalService.fetchViolations()
        for violation in violations {
            print("Обработка нарушения: \(violation["description"] ?? ""), \(violation["date"] ?? "")")
            // Дополнительная логика для адаптации информации о внешнем нарушении
        }
    }
}

// Использование адаптера нарушения
let externalViolationControlServiceProvider = ExternalViolationControlServiceProvider()
let externalViolationControlService = externalViolationControlServiceProvider.getExternalViolationControlService()

let violationAdapter = ViolationAdapter(externalService: externalViolationControlService)
violationAdapter.processViolation()
```
### Шаблон "Мост" (Bridge):
**Описание:** Шаблон "Мост" позволяет отделить абстракцию от реализации, чтобы они могли изменяться независимо друг от друга.

**Применение для системы строительного контроля:** Шаблон "Мост" можно применить для отделения абстракции от реализации классов нарушений и их классификаторов.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/662bae96-37a0-4323-b5ef-70fae798698e)

**Конечный код:**
```python
from abc import ABC, abstractmethod

class Violation(ABC):
    @abstractmethod
    def classify(self):
        pass

class ConcreteViolation(Violation):
    def __init__(self, classifier):
        self.classifier = classifier

    def classify(self):
        self.classifier.classify(self)

class ViolationClassifier(ABC):
    @abstractmethod
    def classify(self, violation):
        pass

class ConcreteClassifierA(ViolationClassifier):
    def classify(self, violation):
        print("Classifying violation A")

class ConcreteClassifierB(ViolationClassifier):
    def classify(self, violation):
        print("Classifying violation B")

# Использование шаблона "Мост"
classifier_a = ConcreteClassifierA()
violation_a = ConcreteViolation(classifier_a)
violation_a.classify()

classifier_b = ConcreteClassifierB()
violation_b = ConcreteViolation(classifier_b)
violation_b.classify()
```
### Шаблон "Компоновщик" (Composite):
**Описание:** Шаблон "Компоновщик" объединяет объекты в древовидную структуру для представления иерархии частей-целого.

**Применение для системы строительного контроля:** Шаблон "Компоновщик" можно использовать для представления иерархии объектов недвижимости, где здания могут состоять из комнат, этажей и других элементов.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/c40c2835-604d-4266-a94e-146d399c06bf)

**Конечный код:**
```python
class Component(ABC):
    @abstractmethod
    def operation(self):
        pass

class ConcreteComponent(Component):
    def operation(self):
        print("Leaf operation")

class Composite(Component):
    def __init__(self):
        self.children = []

    def add(self, component):
        self.children.append(component)

    def operation(self):
        for child in self.children:
            child.operation()

# Использование компоновщика
leaf1 = ConcreteComponent()
leaf2 = ConcreteComponent()
composite = Composite()
composite.add(leaf1)
composite.add(leaf2)
composite.operation()
```
### Шаблон "Декоратор" (Decorator):
**Описание:** Шаблон "Декоратор" позволяет добавлять новые функциональные возможности объектам динамически, не изменяя их структуру.

**Применение для системы строительного контроля:** Шаблон "Декоратор" можно использовать, чтобы добавить дополнительную функциональность к объектам нарушений, такую как логирование или дополнительные проверки.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/07caf410-6f95-4154-a043-7ea0d5121275)

**Конечный код:**
```python
class ViolationDecorator:
    def __init__(self, violation):
        self.violation = violation

    def get_description(self):
        return self.violation.get_description()

class LoggingDecorator(ViolationDecorator):
    def get_description(self):
        description
```
## Поведенческие шаблоны
### Наблюдатель (Observer):
**Описание:** Шаблон "Наблюдатель" устанавливает отношение "один-ко-многим" между объектами таким образом, что при изменении состояния одного объекта все зависящие от него объекты автоматически уведомляются и обновляются.

**Применение для системы строительного контроля:** Шаблон "Наблюдатель" можно использовать для реализации механизма уведомлений о новых нарушениях или изменениях в состоянии объектов.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/83f1cf77-72d4-4d59-a0bb-60ffd94950d5)

**Конечный код:**
```python
class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()

class ConcreteSubject(Subject):
    def some_business_logic(self):
        self.notify()

class Observer:
    def update(self):
        pass

class ConcreteObserver(Observer):
    def update(self):
        print("ConcreteObserver: Reacted to the event")

# Пример использования
subject = ConcreteSubject()
observer1 = ConcreteObserver()
observer2 = ConcreteObserver()

subject.attach(observer1)
subject.attach(observer2)

subject.some_business_logic()

subject.detach(observer2)

subject.some_business_logic()
```
### Стратегия (Strategy):
**Описание:** Шаблон "Стратегия" определяет семейство алгоритмов, инкапсулирует каждый из них и обеспечивает их взаимозаменяемость. Он позволяет алгоритмы изменяться независимо от клиентов, которые их используют.

**Применение для системы строительного контроля:** Шаблон "Стратегия" для выбора различных алгоритмов классификации или обработки нарушений в зависимости от их типа или других параметров.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/d57214db-b108-4a60-b10f-092c6702c6df)

**Конечный код:**
```python
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def algorithm_interface(self):
        pass

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_operation(self):
        self.strategy.algorithm_interface()

class ConcreteStrategyA(Strategy):
    def algorithm_interface(self):
        print("Executing Algorithm A")

class ConcreteStrategyB(Strategy):
    def algorithm_interface(self):
        print("Executing Algorithm B")

# Пример использования
context = Context(ConcreteStrategyA())
context.execute_operation()

context.set_strategy(ConcreteStrategyB())
context.execute_operation()
```
###  Состояние (State):
**Описание:** Шаблон "Состояние" позволяет объекту изменять свое поведение при изменении его внутреннего состояния. Он превращает поведение объекта в отдельные классы, что делает его состояние независимым от контекста.

**Применение для системы строительного контроля:** Шаблон "Состояние" можно применить для моделирования различных состояний процесса устранения нарушений, таких как "в ожидании проверки", "в процессе устранения", "завершено" и т. д.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/03214f49-3a10-4a44-8521-b64670dece6f)

**Конечный код:**
```python
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def handle(self):
        pass

class Context:
    def __init__(self, state):
        self.state = state

    def request(self):
        self.state.handle()

class ConcreteStateA(State):
    def handle(self):
        print("Handling request in State A")

class ConcreteStateB(State):
    def handle(self):
        print("Handling request in State B")

# Пример использования
context = Context(ConcreteStateA())
context.request()

context.state = ConcreteStateB()
context.request()
```
###  Команда (Command):
**Описание:** Шаблон "Команда" инкапсулирует запрос в виде объекта, позволяя клиентам параметризовать клиентские запросы, последовательно записывать операции и поддерживать отмену операций.

**Применение для системы строительного контроля:** Шаблон "Команда" можно применить для инкапсуляции операций управления нарушениями, такими как создание, редактирование и удаление нарушений, что позволит легко расширять систему с новыми операциями и поддерживать отмену операций.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/203d42c3-a817-4f24-8e75-37022f1ba9d8)

**Конечный код:**
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class ConcreteCommandA(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.action()

    def undo(self):
        pass

class ConcreteCommandB(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.action()

    def undo(self):
        pass

class Invoker:
    def __init__(self):
        self.commands = []

    def store_command(self, command):
        self.commands.append(command)

    def execute_commands(self):
        for command in self.commands:
            command.execute()

class Receiver(ABC):
    @abstractmethod
    def action(self):
        pass

class ReceiverA(Receiver):
    def action(self):
        print("Receiver A: Performing action")

class ReceiverB(Receiver):
    def action(self):
        print("Receiver B: Performing action")

# Пример использования
receiver_a = ReceiverA()
command_a = ConcreteCommandA(receiver_a)
receiver_b = ReceiverB()
command_b = ConcreteCommandB(receiver_b)

invoker = Invoker()
invoker.store_command(command_a)
invoker.store_command(command_b)

invoker.execute_commands()
```
###  Итератор (Iterator):
**Описание:** Шаблон "Итератор" предоставляет способ последовательного доступа к элементам коллекции без раскрытия внутренней структуры коллекции. Он позволяет клиентам обходить элементы коллекции без необходимости знания о ее внутренней реализации.

**Применение для системы строительного контроля:** Шаблон "Итератор" можно использовать для перебора списка нарушений, связанных с конкретным объектом недвижимости, без прямого доступа к его внутреннему представлению.

![image](https://github.com/ValeriaSuhinina/hse_paps/assets/126563738/f0c6e472-22c3-493c-b61d-e69fa3ca5715)

**Конечный код:**
```python
from abc import ABC, abstractmethod

class Iterator(ABC):
    @abstractmethod
    def first(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def is_done(self):
        pass

    @abstractmethod
    def current_item(self):
        pass

class Aggregate(ABC):
    @abstractmethod
    def create_iterator(self):
        pass

class ConcreteIterator(Iterator):
    def __init__(self, aggregate):
        self.aggregate = aggregate
        self.index = 0

    def first(self):
        self.index = 0

    def next(self):
        self.index += 1

    def is_done(self):
        return self.index >= len(self.aggregate.items)

    def current_item(self):
        if not self.is_done():
            return self.aggregate.items[self.index]
        else:
            return None

class ConcreteAggregate(Aggregate):
    def __init__(self):
        self.items = []

    def create_iterator(self):
        return ConcreteIterator(self)

# Пример использования
aggregate = ConcreteAggregate()
aggregate.items = [1, 2, 3, 4, 5]

iterator = aggregate.create_iterator()
iterator.first()

while not iterator.is_done():
    print(iterator.current_item())
    iterator.next()
```
