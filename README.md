# **Drzewa czerwono-czarne**

<br>
<div style="text-align: right"><b>Paweł Nykiel</b></div>

## **1. Wstęp**

Program zrealizowany jako projekt zaliczeniowy z przedmiotu Python. Implementuje drzewo czerwono-czarne — rodzaj zbalansowanego drzewa binarnego poszukiwań, zapewniający logarytmiczną wysokość, nawet przy wielu wstawieniach i usunięciach.

Drzewo czerwono-czarne ma zastosowania w strukturach takich jak mapy, zbiory czy bazy danych.

----------
<br>

## **2. Właściwości drzewa czerwono-czarnego**

Drzewa czerwono-czarne zdefiniowane są przez następujące reguły:
1. Każdy węzeł jest albo czerwony, albo czarny.
2. Korzeń drzewa jest zawsze czarny.
3. Czerwony węzeł nie może mieć czerwonych dzieci (brak "czerwonych łańcuchów").
4. Każda ścieżka od korzenia (ROOT) do "pustego liścia" (NULL) zawiera tę samą liczbę czarnych węzłów.

Powyższe reguły pozwalają na utrzymanie logarytmicznej wysokości drzewa i efektywność operacji wstawiania, usuwania i wyszukiwania.

----------
<br>

## **3. Kluczowe operacje drzewa**

Program implementuje następujące funkcjonalności:
1. **Wstawianie elementów** z automatycznym zachowaniem własności drzewa czerwono-czarnego.
2. **Usuwanie elementów** z zachowaniem struktury drzewa.
3. **Wyszukiwanie elementów** w drzewie.
4. **Przeglądanie drzewa** w różnych porządkach (inorder, preorder, postorder).
5. **Walidacja drzewa**, sprawdzająca zgodność z regułami drzewa czerwono-czarnego.
6. **Wizualizacja drzewa** w formie grafu zapisującego się jako plik graficzny (PNG).
7. **Obliczanie wysokości** drzewa oraz liczby węzłów.
8. **Czyszczenie drzewa**.

----------
<br>

## **4. Struktura programu**

Aplikacja składa się z dwóch podstawowych klas:
- `Node` (Węzeł): Reprezentuje pojedynczy element drzewa, zawierający wartość, kolor (czerwony lub czarny) oraz wskaźniki na dzieci, rodzica i inne, np. dziadka czy wujka.
- `RBTree` (Drzewo czerwono-czarne): Klasa zarządzająca strukturą drzewa oraz implementująca wszystkie operacje wymagane na tej strukturze.

----------
<br>

## **5. Opis operacji**

Pniższy rozdział zawiera krótkie przedstawienie najistotniejszych operacji wraz z najciekawszymi fragmentami kodu

### **Wstawianie elementów (Insert)**
Wstawianie nowego elementu do drzewa czerwono-czarnego przebiega w dwóch etapach:
1. **Dodanie węzła** zgodnie z metodą wstawiania w drzewie binarnym. Nowy węzeł domyślnie jest czerwony:
``` python
def insert(self, value):
    new = Node(value)
    if self.root is None:  # Jeśli drzewo jest puste, nowy węzeł staje się korzeniem
        self.root = new
        self.root.color = 'black'
    else:
        inserted = self.insert_node(self.root, new)  # Rekurencyjna metoda wstawiania nowego węzła do drzewa BST
        if inserted:
            self.fix_insert(new)  # Naprawa struktury drzewa
```
2. **Naprawa drzewa** po wstawieniu wywoływana jest metoda, która koryguje potencjalne naruszenia reguł drzewa czerwono-czarnego. Wykorzystuje rotacje i zmiany kolorów:
``` python
def fix_insert(self, node):
    while node != self.root and node.parent.color == 'red':
        grandparent = node.grandparent()
        if node.parent == grandparent.left:
            uncle = grandparent.right
            if uncle and uncle.color == 'red':  # Przypadek 1: Wujek jest czerwony
                node.parent.color = 'black'
                uncle.color = 'black'
                grandparent.color = 'red'
                node = grandparent
            else:
                if node == node.parent.right:  # Przypadek 2: Rotacja w lewo
                    node = node.parent
                    self.left_rotate(node)
                node.parent.color = 'black'  # Przypadek 3: Rekolorowanie i rotacja
                grandparent.color = 'red'
                self.right_rotate(grandparent)
        else:
            # Analogiczne przypadki dla rodzica będącego prawym dzieckiem
    self.root.color = 'black'
```

### **Usuwanie elementów (Delete)**
Usunięcie węzła może prowadzić do naruszenia struktury drzewa. W takim przypadku stosuje się mechanizmy naprawcze, takie jak "podwójna czerń" (double black).

Przykładowy fragment:
``` python
def delete(self, value):
    node = self.search(value)
    if node is None:
        print(f"Value {value} not found in the tree.")
        return
    self.delete_node(node)
    print(f"Deleted {value} from the tree.")
    
...

# Fragment obsługi podwójnej czerni
while node != self.root and node.color == 'black':
    if node == node.parent.left:
        sibling = node.parent.right
        if sibling.color == 'red':
            sibling.color = 'black'
            node.parent.color = 'red'
            self.left_rotate(node.parent)
        # Inne przypadki dla rodzeństwa czarnego
    node.color = 'black'
```
Operacja usuwania obejmuje:
1. Znalezienie węzła do usunięcia.
2. Usunięcie go z drzewa.
3. Naprawę problemów.


### **Wizualizacja drzewa**
Metoda wizualizuje strukturę drzewa w formie grafu przy użyciu biblioteki `graphviz`. Każdy węzeł jest oznaczony kolorem odpowiadającym jego kolorowi w drzewie.

```python
def visualize(self, filename="red_black_tree"):
    def add_edges(graph, node):
        if not node:
            return
        color = "black" if node.color == "black" else "red"
        graph.node(str(node.value), str(node.value),
                   fillcolor=color, style="filled", fontcolor="white")
        if node.left:
            graph.edge(str(node.value), str(node.left.value))
            add_edges(graph, node.left)
        if node.right:
            graph.edge(str(node.value), str(node.right.value))
            add_edges(graph, node.right)

    graph = Digraph(comment="Red-Black Tree")
    graph.attr("node", shape="circle", fontcolor="white", style="filled")
    if self.root:
        add_edges(graph, self.root)
    graph.render(filename, format="png", cleanup=True)
```

### **Walidacja drzewa**
Metoda sprawdza, czy drzewo spełnia wszystkie zasady drzewa czerwono-czarnego.
Zawiera rekurencyjną metodę check_properties, która sprawdza każdy węzeł.

```python
def is_valid(self):
    
    def check_properties(node):
           
        if node is None:  # Base case: Every NULL leaf has black height 1
            return 1, True
    
        left_black_height, left_valid = check_properties(node.left)
        right_black_height, right_valid = check_properties(node.right)
    
        # Check for both subtrees validity
        if not left_valid or not right_valid:
            return 0, False
    
        # Rule 4: Both sides must have the same black height
        if left_black_height != right_black_height:
            return 0, False
    
        # Rule 3: Red nodes cannot have red children
        if node.color == "red":
            if (node.left and node.left.color == "red") or (node.right and node.right.color == "red"):
                return 0, False
    
        # Increment the black height for black nodes
        return (left_black_height + 1 if node.color == "black" else left_black_height), True
    
    # Rule 2: The root must be black
    if self.root and self.root.color != "black":
        return False
    
    # Validate all other properties
    _, is_valid_tree = check_properties(self.root)
    return is_valid_tree
```

### **Obliczanie własności drzewa**
Metody pozwalają na rekurencyjne obliczanie wysokości drzewa i liczby węzłów:

```python
def height(self, node=None):
    if node is None:
        node = self.root
    if node is None:
        return -1
    return 1 + max(self.height(node.left), self.height(node.right))

def count_nodes(self, node=None):
    if node is None:
        node = self.root
    if node is None:
        return 0
    return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)
```

----------
<br>

## **6. Złożoność implementacji**

### **Złożoność pamięciowa**

Drzewo czerwono-czarne wymaga przechowywania następujących informacji dla każdego węzła:
 - Wartość węzła (klucz).
 - Kolor węzła (czerwony lub czarny).
 - Wskaźniki na rodzica, lewe i prawe dziecko.

Całkowita pamięć zajmowana przez drzewo to **O(n)**, gdzie n to liczba węzłów.
### **Złożoność czasowa**

#### Wstawianie

Złożoność czasowa to **O(log n)**. Proces obejmuje:
- Znalezienie odpowiedniego miejsca dla nowego węzła (O(log n)).
- Naprawę drzewa za pomocą rekolorowania i rotacji (maksymalnie O(log n)).

#### Usuwanie

Złożoność czasowa to **O(log n)**. Proces obejmuje:
- Znalezienie i usunięcie węzła (O(log n)).
- Naprawę potencjalnych naruszeń drzewa (O(log n)).

#### Wyszukiwanie
Złożoność czasowa to **O(log n)**, wynikająca z wysokości drzewa.
- Przeglądanie drzewa
- Przeglądanie w dowolnym porządku (inorder, preorder, postorder) ma złożoność O(n), ponieważ każdy węzeł jest odwiedzany raz.

#### Walidacja drzewa
Złożoność to **O(n)**, ponieważ każdy węzeł musi zostać sprawdzony pod kątem zgodności z zasadami drzewa czerwono-czarnego.
<br>

----------
<br>

## **7. Sposób uruchomienia**
1. Zainstaluj bibliotekę `graphviz`,  za pomocą:<br>
`pip install graphvix`
2. Uruchom program testujący:<br>
`python test_RB_Tree.py` lub `python3 test_RB_Tree.py`<br>

----------
<br>

## **8. Literatura**

Strona Pana Profesora Kapanowskiego: <br>
https://ufkapano.github.io/ <br>
oraz<br>
https://en.wikipedia.org/wiki/Red-black_tree
<br>
https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree
<br>
https://en.wikipedia.org/wiki/Binary_search_tree
<br>
https://graphviz.org/documentation/

----------
<br>

## **11. Wymagania**

**Python** - testowane na wersji **3.11**<br>