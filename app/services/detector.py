import re
from typing import List, Tuple, Optional, Dict, Set
import pymorphy3 as pymorphy2

class RailwayTrashDetector:
    def __init__(self, max_distance: int = 15, min_confidence: float = 0.7):
        """
        max_distance: максимальное количество слов между словами из разных словарей
        min_confidence: минимальный порог уверенности для определения мусора у ЖД
        """
        self.max_distance = max_distance
        self.min_confidence = min_confidence

        # Инициализируем морфологический анализатор
        self.morph = pymorphy2.MorphAnalyzer()

        # Словарь станций (ваш существующий список)
        self.stations = [
            "смоленск-сортировочный", "смоленск", "ельня", "гнездово", "гусино",
            "красное", "красный бор", "голынки", "рудня", "кардымово", "ярцево",
            "милохово", "сафоново", "азотная", "игоревская", "издешково", "семлево",
            "сычевка", "новодугинская", "вязьма-новоторжская", "вязьма",
            "вязьма-брянская", "волоста-пятница", "угра", "туманово", "гагарин",
            "уваровка", "бородино", "валутино", "тычинино", "новосмоленская",
            "рябцево", "починок", "энгельгардтовская", "стодолище", "козловка",
            "рославль 1", "рославль", "понятовка", "аселье", "сещинская", "дубровка",
            "жуковка", "клетня", "тростна", "ржаница", "сельцо", "орджоникидзеград",
            "бекасово-сортировочное", "бекасово", "акулово", "очаково 1", "очаково",
            "солнечная", "внуково", "аэропорт", "толстопальцево", "крекшино",
            "апрелевка", "селятино", "сандарово", "кресты", "фили", "кунцево 2",
            "кунцево", "усово", "одинцово", "голицыно", "звенигород", "петелино",
            "кубинка 1", "кубинка", "кубинка 2", "тучково", "дорохово", "можайск",
            "нара", "латышская", "ворсино", "балабаново", "обнинское", "шемякино",
            "малоярославец", "суходрев", "тихонова пустынь", "калуга-сергиев скит",
            "калуга", "воротынск", "бабынино", "шаня", "полотняный завод",
            "говардово", "мятлевская", "износки", "темкино", "люблино-сортировочное",
            "люблино", "серпухов", "серпухов-ветка", "шарапова охота", "чехов",
            "столбовая", "детково", "гривно", "подольск", "силикатная", "щербинка",
            "красный строитель", "кашира-пассажирская", "кашира-товарная", "кашира",
            "акри", "ступино", "жилево", "непецино", "сотниково", "михнево", "малино",
            "усады-окружные", "барыбино", "белые столбы", "домодедово", "авиационная",
            "космос", "чертаново", "бирюлево-товарная", "бирюлево", "коломенское",
            "перово", "москва-пассажирская-казанская", "москва-казанская",
            "казанский", "казанский вокзал", "москва-пассажирская-ярославская",
            "москва-ярославская", "ярославский", "ярославский вокзал",
            "москва-пассажирская-киевская", "москва-киевская", "киевский",
            "киевский вокзал", "москва-товарная-смоленская", "москва-смоленская",
            "смоленский", "смоленский вокзал", "москва-сортировочная-киевская",
            "москва-бутырская", "савёловский", "савёловский вокзал", "москва",
            "люберцы 1", "люберцы", "люберцы 2", "мальчики", "яничкино", "овражки",
            "гжель", "быково", "раменское", "бронницы", "фаустово", "виноградово",
            "лосиноостровская", "бескудниково", "подмосковная", "тушино", "павшино",
            "нахабино", "дедовск", "снегири", "манихино 1", "манихино", "лукино",
            "новоиерусалимская", "холщевики", "румянцево", "чисмена", "волоколамск",
            "шаховская", "пресня", "лефортово", "новопролетарская", "брянск-льговский",
            "брянск-орловский", "брянск-восточный", "брянск", "белые берега",
            "карачев", "хотынец", "нарышкино", "полпинская", "фокино", "любохна",
            "дятьково", "злынка", "свень", "выгоничи", "пильшино", "почеп", "унеча",
            "клинцы", "новозыбков", "климов", "сураж", "ипуть", "стародуб", "жеча",
            "погар", "навля", "алтухово", "кокоревка", "холмечи", "суземка", "погребы",
            "брасово", "комаричи", "дерюгино", "дмитриев-льговский", "дмитриев",
            "арбузово", "остапово", "михайловский рудник", "курбакинская", "кромы",
            "лужки-орловские", "конышевка", "шерекино", "льгов-киевский", "льгов",
            "суджа", "сосновый бор", "псел", "глушково", "коренево", "сеймская",
            "рыльск", "блохино", "лукашевка", "дьяконово", "рышково", "курск",
            "ноздрачево", "отрешково", "охочевка", "колпны", "щигры", "удобрительная",
            "черемисиново", "мармыжи", "кшень", "плеханово", "тула-лихвинская",
            "тула 1-курская", "тула 1", "тула", "тула-вяземская", "хомяково",
            "ревякино", "ясногорск", "тарусская", "некрасово", "обидимо", "суходол",
            "алексин", "энергетик", "средняя", "криволучье", "присады", "дедилово",
            "берники", "упа", "ханино", "збродово", "черепеть", "шепелево", "тупик",
            "слаговищи", "белев", "арсеньево", "ясная поляна", "казначеевка", "щекино",
            "лазарево", "плавск", "горбачево", "скуратово", "чернь", "мценск",
            "думчино", "отрада", "стальной конь", "орел", "кромская", "цон", "саханская",
            "становой колодезь", "еропкино", "змиевка", "глазуновка", "малоархангельск",
            "поныри", "возы", "золотухино", "свобода", "моховая", "залегощь", "верховье"
        ]

        # Приводим все станции к нормальной форме
        self.stations_normalized: Set[str] = set()
        for station in self.stations:
            words = station.split()
            normalized_words = []
            for word in words:
                if word.isdigit():
                    normalized_words.append(word)
                else:
                    try:
                        lemma = self.morph.parse(word)[0].normal_form
                        normalized_words.append(lemma)
                    except:
                        normalized_words.append(word.lower())
            normalized_station = ' '.join(normalized_words)
            self.stations_normalized.add(normalized_station)
            self.stations_normalized.add(station.lower())

        # Словарь мусорных слов
        self.trash_words = [
            "мусор", "свалка", "отход", "хлам", "бутылка", "банка",
            "пакет", "куча", "замусорить", "грязь", "бытовка", "тко",
            "твердый бытовой", "незаконный свалка", "стихийный свалка",
            "мешок", "коробка", "очистка", "уборка", "завал"
        ]

        # Приводим мусорные слова к нормальной форме
        self.trash_normalized: Set[str] = set()
        for word in self.trash_words:
            words = word.split()
            for w in words:
                try:
                    lemma = self.morph.parse(w)[0].normal_form
                    self.trash_normalized.add(lemma)
                except:
                    self.trash_normalized.add(w.lower())
            self.trash_normalized.add(word.lower())

        # Словарь ЖД маркеров (ОБЯЗАТЕЛЬНЫЕ для высокого confidence)
        self.railway_markers = [
            "жд", "ж/д", "железнодорожный", "путь", "рельс", "шпала",
            "электричка", "поезд", "платформа", "вокзал", "переезд",
            "станция", "полустанок", "депо", "тупик", "ветка", "перрон",
            "локомотив", "состав", "вагон", "тамбур"
        ]

        # Приводим маркеры к нормальной форме
        self.markers_normalized: Set[str] = set()
        for marker in self.railway_markers:
            words = marker.split()
            for w in words:
                try:
                    lemma = self.morph.parse(w)[0].normal_form
                    self.markers_normalized.add(lemma)
                except:
                    self.markers_normalized.add(w.lower())
            self.markers_normalized.add(marker.lower())

        # Конфликтующие локации (если они ближе - то это НЕ ЖД мусор)
        self.conflicting_locations = [
            "парк", "лес", "двор", "улица", "город", "деревня", "поселок",
            "река", "озеро", "пруд", "море", "пляж", "берег", "сквер",
            "аллея", "бульвар", "площадь", "дорожка", "тротуар", "газон",
            "клумба", "дача", "огород", "поле", "луг", "болото", "овраг",
            "карьер", "стройка", "мусорка", "полигон", "квартал", "микрорайон",
            "школа", "больница", "магазин", "жилой комплекс"
        ]

        # Приводим локации к нормальной форме
        self.conflicting_normalized: Set[str] = set()
        self.conflicting_weights: Dict[str, float] = {}

        for loc in self.conflicting_locations:
            words = loc.split()
            for w in words:
                try:
                    lemma = self.morph.parse(w)[0].normal_form
                    self.conflicting_normalized.add(lemma)
                    # Сильные конфликты
                    if lemma in ["парк", "лес", "двор", "квартал", "река", "озеро"]:
                        self.conflicting_weights[lemma] = 3.0
                    else:
                        self.conflicting_weights[lemma] = 2.0
                except:
                    self.conflicting_normalized.add(w.lower())
            self.conflicting_normalized.add(loc.lower())
            if loc in ["парк", "лес", "двор", "квартал", "река", "озеро"]:
                self.conflicting_weights[loc] = 3.0

        # Железнодорожные исключения (слова, которые НЕ считаем конфликтом в ЖД контексте)
        self.railway_exceptions = {
            "парк": ["железнодорожный", "локомотивный", "вагонный", "депо"],
            "город": ["спутник", "ж/д", "железнодорожный", "москва"],
            "двор": ["локомотивный", "вагонный", "депо"]
        }

        # Ложные мусорные слова (метафоры и т.д.)
        self.false_trash_patterns = [
            ("куча", ["машин", "народу", "людей", "свободных", "денег", "поездов", "мест"]),
            ("кучу", ["машин", "народу", "людей", "свободных", "денег", "названий", "мест"]),
            ("кучи", ["машин", "народу", "людей", "свободных", "денег", "мест"]),
            ("грязь", ["водопровод", "авария", "ремонт", "лужа", "поток", "снег"]),
        ]

        # Слова, которые НЕ считаем мусором в ЖД-контексте
        self.not_trash_context = {
            "субботник": 0.2,
            "озеленение": 0.1,
            "благоустройство": 0.2,
            "покос": 0.1,
            "посадка": 0.1,
            "асфальтирование": 0.1,
            "ремонт дорог": 0.1,
            "яма": 0.1,
            "выбоина": 0.1
        }

    def lemmatize_token(self, token: str) -> str:
        """Приводит слово к нормальной форме (лемме)"""
        try:
            return self.morph.parse(token)[0].normal_form
        except:
            return token.lower()

    def tokenize_and_lemmatize(self, text: str) -> List[Tuple[str, str, int]]:
        """
        Разбивает текст на токены и возвращает (оригинал, лемма, позиция)
        """
        tokens = re.findall(r'\b[а-яё\w]+\b', text.lower())
        return [(token, self.lemmatize_token(token), i) for i, token in enumerate(tokens)]

    def _is_railway_exception(self, tokens_with_lemmas: List[Tuple[str, str, int]],
                              position: int, lemma: str) -> bool:
        """
        Проверяет, является ли слово железнодорожным исключением
        """
        if lemma not in self.railway_exceptions:
            return False

        # Проверяем предыдущие слова
        context_window = max(0, position - 2)
        for i in range(context_window, position):
            _, prev_lemma, _ = tokens_with_lemmas[i]
            if prev_lemma in self.railway_exceptions[lemma]:
                return True

        # Проверяем следующее слово
        if position + 1 < len(tokens_with_lemmas):
            _, next_lemma, _ = tokens_with_lemmas[position + 1]
            if next_lemma in self.railway_exceptions[lemma]:
                return True

        return False

    def _is_false_positive_trash(self, tokens_with_lemmas: List[Tuple[str, str, int]],
                                  position: int, lemma: str) -> bool:
        """
        Проверяет, является ли мусорное слово ложным срабатыванием
        """
        # Проверяем метафорические паттерны
        for false_word, false_contexts in self.false_trash_patterns:
            if lemma == false_word or false_word in lemma:
                # Смотрим следующие слова
                for i in range(position + 1, min(position + 4, len(tokens_with_lemmas))):
                    _, next_lemma, _ = tokens_with_lemmas[i]
                    if any(context in next_lemma for context in false_contexts):
                        return True

        # "Уборка" без ЖД контекста
        if lemma in ["уборка", "уборку", "уборки"]:
            has_railway = False
            start = max(0, position - 5)
            end = min(len(tokens_with_lemmas), position + 5)
            for i in range(start, end):
                if i != position:
                    _, check_lemma, _ = tokens_with_lemmas[i]
                    if check_lemma in self.markers_normalized:
                        has_railway = True
                        break
            if not has_railway:
                return True

        # "Москва" в названиях организаций
        if lemma == "москва" and position > 0:
            prev_word, prev_lemma, _ = tokens_with_lemmas[position - 1]
            org_words = ["департамент", "префектура", "управа", "правительство",
                        "мэрия", "гбу", "гу", "джкх", "прокуратура", "министерство",
                        "московский", "государственный", "федеральный"]
            if prev_lemma in org_words or prev_word in org_words:
                return True

        # Проверка на not-trash контекст
        if lemma in self.not_trash_context:
            return True

        return False

    def _get_conflict_weight(self, lemma: str) -> float:
        """Получает вес конфликтующей локации"""
        return self.conflicting_weights.get(lemma, 2.0)

    def check_word_distance(self, text: str) -> Tuple[bool, float]:
        """
        Проверяет наличие мусора в ЖД-контексте с семантическим анализом
        Возвращает: (найден_ли_мусор, сила_сигнала)
        """
        tokens_with_lemmas = self.tokenize_and_lemmatize(text)

        station_indices = []
        trash_indices = []
        marker_indices = []
        conflict_indices = []  # (позиция, вес)

        for original, lemma, pos in tokens_with_lemmas:
            # Проверка станций (исключаем "Москва" без контекста)
            if lemma in self.stations_normalized or original in self.stations_normalized:
                if lemma == "москва":
                    # Проверяем, есть ли ЖД контекст рядом
                    has_railway_nearby = False
                    start = max(0, pos - 3)
                    end = min(len(tokens_with_lemmas), pos + 3)
                    for i in range(start, end):
                        if i != pos:
                            _, check_lemma, _ = tokens_with_lemmas[i]
                            if check_lemma in self.markers_normalized:
                                has_railway_nearby = True
                                break
                    if not has_railway_nearby:
                        continue
                station_indices.append(pos)

            # Проверка мусора
            if lemma in self.trash_normalized or original in self.trash_normalized:
                # Фильтруем ложные срабатывания
                if not self._is_false_positive_trash(tokens_with_lemmas, pos, lemma):
                    trash_indices.append(pos)

            # Проверка маркеров
            if lemma in self.markers_normalized or original in self.markers_normalized:
                marker_indices.append(pos)

            # Проверка конфликтующих локаций
            if lemma in self.conflicting_normalized:
                if not self._is_railway_exception(tokens_with_lemmas, pos, lemma):
                    weight = self._get_conflict_weight(lemma)
                    conflict_indices.append((pos, weight))

        # Если нет мусора - сразу false
        if not trash_indices:
            return False, 0.0

        # Важное правило: если нет ни одного ЖД маркера - снижаем уверенность
        has_markers = len(marker_indices) > 0

        # Оцениваем силу сигнала для каждого мусора
        signal_strength_total = 0.0

        for t_pos in trash_indices:
            # Находим все ЖД объекты рядом с мусором
            railway_signals = []

            for s_pos in station_indices:
                distance = abs(s_pos - t_pos)
                if distance <= self.max_distance:
                    # Станции дают вес 2.0, уменьшаем линейно с расстоянием
                    weight = 2.0 * (1.0 - distance / (self.max_distance * 1.5))
                    railway_signals.append(('station', distance, weight))

            for m_pos in marker_indices:
                distance = abs(m_pos - t_pos)
                if distance <= self.max_distance:
                    # Маркеры дают вес 1.0
                    weight = 1.0 * (1.0 - distance / (self.max_distance * 1.5))
                    railway_signals.append(('marker', distance, weight))

            if not railway_signals:
                continue

            # Берем ближайший ЖД сигнал
            closest_railway = min(railway_signals, key=lambda x: x[1])

            # Проверяем конфликты
            conflicts = []
            for c_pos, c_weight in conflict_indices:
                distance = abs(c_pos - t_pos)
                # Конфликт должен быть ближе, чем ЖД сигнал
                if distance < closest_railway[1]:
                    conflicts.append((distance, c_weight))

            if not conflicts:
                # Нет конфликтов - хороший сигнал
                signal_strength = closest_railway[2]
                # Бонус за наличие маркеров
                if has_markers:
                    signal_strength *= 1.2
            else:
                # Есть конфликты, вычитаем их влияние
                closest_conflict = min(conflicts, key=lambda x: x[0])
                conflict_distance, conflict_weight = closest_conflict

                if conflict_distance < 2:
                    # Конфликт слишком близко - игнорируем
                    signal_strength = 0
                elif conflict_distance * 1.2 < closest_railway[1]:
                    # Конфликт значительно ближе
                    signal_strength = 0
                else:
                    # Вычитаем вес конфликта
                    penalty = conflict_weight / (conflict_distance + 1)
                    signal_strength = max(0, closest_railway[2] - penalty)

            signal_strength_total += signal_strength

        # Финальное решение
        has_trash = signal_strength_total >= self.min_confidence
        confidence = min(1.0, signal_strength_total / 1.5)

        return has_trash, confidence

    def detect(self, text: str) -> dict:
        """
        Основной метод детекции
        """
        tokens_with_lemmas = self.tokenize_and_lemmatize(text)

        stations_found = set()
        trash_found = set()
        markers_found = set()
        conflicts_found = set()

        for original, lemma, pos in tokens_with_lemmas:
            if lemma in self.stations_normalized or original in self.stations_normalized:
                # Фильтр для Москвы
                if lemma == "москва":
                    has_context = False
                    start = max(0, pos - 3)
                    end = min(len(tokens_with_lemmas), pos + 3)
                    for i in range(start, end):
                        if i != pos:
                            _, check_lemma, _ = tokens_with_lemmas[i]
                            if check_lemma in self.markers_normalized:
                                has_context = True
                                break
                    if not has_context:
                        continue
                stations_found.add(original)

            if lemma in self.trash_normalized or original in self.trash_normalized:
                if not self._is_false_positive_trash(tokens_with_lemmas, pos, lemma):
                    trash_found.add(original)

            if lemma in self.markers_normalized or original in self.markers_normalized:
                markers_found.add(original)

            if lemma in self.conflicting_normalized:
                if not self._is_railway_exception(tokens_with_lemmas, pos, lemma):
                    conflicts_found.add(original)

        # Основная проверка
        has_pair, confidence = self.check_word_distance(text)

        # Дополнительная пост-обработка
        if has_pair:
            # Если только уборка и нет маркеров - снижаем
            if trash_found and all(t in ["уборка", "уборку", "уборки"] for t in trash_found):
                if not markers_found:
                    has_pair = False
                    confidence = 0.2

            # Если только Москва как станция и нет других
            if stations_found and all(s in ["москва", "москвы"] for s in stations_found):
                if not markers_found:
                    has_pair = False
                    confidence = 0.2

            # Если есть сильный конфликт, который перебивает
            strong_conflicts = ["парк", "лес", "двор", "квартал"]
            if any(c in conflicts_found for c in strong_conflicts):
                if not markers_found or confidence < 0.8:
                    has_pair = False
                    confidence = max(0.1, confidence - 0.3)

        return {
            'has_trash_near_railway': has_pair,
            'stations_found': list(stations_found),
            'trash_found': list(trash_found),
            'railway_markers_found': list(markers_found),
            'conflicting_locations': list(conflicts_found),
            'confidence': confidence
        }
    

import pandas as pd
from tqdm import tqdm
from collections import Counter

# Загружаем данные
print("Загрузка данных...")
df = pd.read_csv('source/posts_raw.csv')

# Создаем детектор (убедитесь, что класс RailwayTrashDetector уже определен выше)
detector = RailwayTrashDetector(max_distance=10, min_confidence=0.7)

# Функция для анализа одного сообщения
def analyze_message(text):
    """Анализирует одно сообщение и возвращает результат"""
    if pd.isna(text) or not isinstance(text, str):
        return None

    result = detector.detect(text)
    return {
        'has_trash': result['has_trash_near_railway'],
        'confidence': result['confidence'],
        'stations': result['stations_found'],
        'trash': result['trash_found'],
        'markers': result['railway_markers_found'],
        'conflicts': result['conflicting_locations']
    }

# Применяем анализ ко всем сообщениям
print("Анализ сообщений...")
tqdm.pandas()
df['analysis'] = df['text'].progress_apply(analyze_message)

# Разворачиваем результаты в отдельные колонки
df['has_trash'] = df['analysis'].apply(lambda x: x['has_trash'] if x else False)
df['confidence'] = df['analysis'].apply(lambda x: x['confidence'] if x else 0)
df['stations_found'] = df['analysis'].apply(lambda x: x['stations'] if x else [])
df['trash_found'] = df['analysis'].apply(lambda x: x['trash'] if x else [])
df['markers_found'] = df['analysis'].apply(lambda x: x['markers'] if x else [])
df['conflicts_found'] = df['analysis'].apply(lambda x: x['conflicts'] if x else [])

# Статистика
print("\n" + "="*80)
print("СТАТИСТИКА АНАЛИЗА")
print("="*80)

total_messages = len(df)
messages_with_trash = df['has_trash'].sum()
messages_without_trash = total_messages - messages_with_trash

print(f"📊 Всего сообщений: {total_messages}")
print(f"🗑️ Сообщений с мусором у ЖД: {messages_with_trash} ({messages_with_trash/total_messages*100:.2f}%)")
print(f"✅ Сообщений без мусора у ЖД: {messages_without_trash} ({messages_without_trash/total_messages*100:.2f}%)")
print(f"📈 Средняя уверенность: {df['confidence'].mean():.3f}")
print(f"📈 Медианная уверенность: {df['confidence'].median():.3f}")

# Анализ найденных станций
all_stations = []
df['stations_found'].apply(lambda x: all_stations.extend(x))
station_counts = Counter(all_stations)

print(f"\n🚉 Топ-15 станций с упоминанием мусора:")
for station, count in station_counts.most_common(15):
    print(f"   {station}: {count} раз(а)")

# Анализ мусорных слов
all_trash = []
df['trash_found'].apply(lambda x: all_trash.extend(x))
trash_counts = Counter(all_trash)

print(f"\n🗑️ Топ-15 мусорных слов:")
for trash, count in trash_counts.most_common(15):
    print(f"   {trash}: {count} раз(а)")

# Анализ ЖД маркеров
all_markers = []
df['markers_found'].apply(lambda x: all_markers.extend(x))
marker_counts = Counter(all_markers)

print(f"\n🛤️ Топ-10 ЖД маркеров:")
for marker, count in marker_counts.most_common(10):
    print(f"   {marker}: {count} раз(а)")

# Анализ конфликтующих локаций
all_conflicts = []
df['conflicts_found'].apply(lambda x: all_conflicts.extend(x))
conflict_counts = Counter(all_conflicts)

print(f"\n⚠️ Топ-10 конфликтующих локаций:")
for conflict, count in conflict_counts.most_common(10):
    print(f"   {conflict}: {count} раз(а)")

# Распределение по уверенности
print(f"\n📊 Распределение по уровню уверенности:")
confidence_bins = [0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0]
for i in range(len(confidence_bins)-1):
    low = confidence_bins[i]
    high = confidence_bins[i+1]
    count = df[(df['confidence'] > low) & (df['confidence'] <= high)].shape[0]
    print(f"   {low:.1f}-{high:.1f}: {count} сообщений")

# Сохраняем результаты
output_file = 'improved_analysis_results.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n💾 Полные результаты сохранены в {output_file}")

# Сохраняем только сообщения с мусором
problematic = df[df['has_trash'] == True].copy()
problematic_file = 'improved_problematic_messages.csv'
problematic.to_csv(problematic_file, index=False, encoding='utf-8-sig')
print(f"⚠️ {len(problematic)} сообщений с мусором сохранено в {problematic_file}")

# Сохраняем сообщения с высокой уверенностью (для проверки качества)
high_confidence = df[(df['has_trash'] == True) & (df['confidence'] >= 0.8)].copy()
high_confidence_file = 'high_confidence_messages.csv'
high_confidence.to_csv(high_confidence_file, index=False, encoding='utf-8-sig')
print(f"🎯 {len(high_confidence)} сообщений с высокой уверенностью (≥0.8) сохранено в {high_confidence_file}")

# Сохраняем сообщения с низкой уверенностью (пограничные случаи)
low_confidence = df[(df['has_trash'] == True) & (df['confidence'] < 0.7)].copy()
low_confidence_file = 'low_confidence_messages.csv'
low_confidence.to_csv(low_confidence_file, index=False, encoding='utf-8-sig')
print(f"⚠️ {len(low_confidence)} сообщений с низкой уверенностью (<0.7) сохранено в {low_confidence_file}")

# Выводим примеры сообщений с мусором (первые 10)
print("\n" + "="*80)
print("ПРИМЕРЫ СООБЩЕНИЙ С МУСОРОМ У ЖД")
print("="*80)

examples = df[df['has_trash'] == True].head(10)
for idx, row in examples.iterrows():
    print(f"\n📝 ID {row.get('id', idx)}: {row['text'][:100]}...")
    print(f"   🚉 Станции: {', '.join(row['stations_found'][:3]) if row['stations_found'] else 'нет'}")
    print(f"   🗑️ Мусор: {', '.join(row['trash_found'][:3]) if row['trash_found'] else 'нет'}")
    print(f"   🛤️ Маркеры: {', '.join(row['markers_found'][:3]) if row['markers_found'] else 'нет'}")
    print(f"   ⚠️ Конфликты: {', '.join(row['conflicts_found'][:3]) if row['conflicts_found'] else 'нет'}")
    print(f"   📊 Уверенность: {row['confidence']:.2f}")